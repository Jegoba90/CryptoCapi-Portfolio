"""
Verifica un recibo del historial de señales de CryptoCapi contra su anclaje en
Bitcoin, sin confiar en nada de CryptoCapi más que en los archivos.

Es la herramienta de la receta: docs/SIGNAL_HISTORY.md en el repo público
(CryptoCapi-Portfolio) y docs/anclaje/RECETA_VERIFICACION.md en el del
proyecto. Sigue el formato v1 y es una implementación independiente: no
comparte código con el backend, que arma los manifiestos en TypeScript. Solo
usa la biblioteca estándar.

Uso:
    python verificar_recibo.py <fila.json> <manifiesto.txt> <manifiesto.txt.ots>
    python verificar_recibo.py --dia AAAA-MM-DD [<fila.json>] [--api URL]

- fila.json: el recibo, un objeto JSON con las 17 columnas de signal_ledger en
  texto, tal como las imprime Postgres (los números como texto, recorded_at con
  seis decimales en UTC).
- manifiesto.txt: el manifiesto del día del recibo, byte por byte.
- manifiesto.txt.ots: la prueba de OpenTimestamps de ese manifiesto.

Con --dia, el manifiesto y la prueba se bajan de la API pública
(GET /v1/history/anchors), y la fila es opcional: sin ella se verifica el día
entero, y con ella, además, el recibo. --api cambia la API (por defecto,
https://api.cryptocapi.com).

Comprueba todo lo que se puede comprobar sin confiar en CryptoCapi: la hoja del
recibo, su línea en el manifiesto, la forma del manifiesto, y que el .ots
certifique la huella del manifiesto y traiga la atestación de un bloque de
Bitcoin. Con --dia, también que la lista publicada diga lo mismo que los
archivos. Qué bloque es, y que ese bloque exista, lo dice opentimestamps.org con
los dos archivos (o el cliente `ots verify`).
"""

import hashlib
import io
import json
import math
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

COLUMNS = sorted(
    [
        "algorithm_id",
        "body_sha256",
        "calculated_at",
        "coin_id",
        "confidence",
        "data_quality",
        "engine",
        "engine_version",
        "id",
        "insight_id",
        "market_regime",
        "protocol_hash",
        "recorded_at",
        "seal_type",
        "sentiment",
        "signal",
        "z_score",
    ]
)
INT_COLUMNS = {"id", "insight_id"}
FLOAT_COLUMNS = {"z_score", "confidence"}
PG_FLOAT = re.compile(r"-?[0-9]+(\.[0-9]+)?(e[+-][0-9]+)?|NaN|-?Infinity")
HEADER = re.compile(r"cryptocapi-signal-ledger v1 day=([0-9]{4}-[0-9]{2}-[0-9]{2}) rows=([0-9]+)")
LINE = re.compile(r"([0-9]+) ([0-9a-f]{64})")

# Una prueba .ots de archivo con SHA-256 empieza con la magia de OpenTimestamps,
# la versión 1 y la operación 0x08; siguen los 32 bytes de la huella.
OTS_FILE_SHA256_HEADER = bytes.fromhex("004f70656e54696d657374616d7073000050726f6f6600bf89e2e884e892940108")
# La etiqueta con que el formato .ots marca la atestación de un bloque de Bitcoin.
OTS_BITCOIN_ATTESTATION = bytes.fromhex("0588960d73d71901")

# El único día anclado fuera de v1: sus líneas van en orden de id como texto,
# por un bug corregido el 2026-10-13 («La excepción del 2026-09-30», en la
# receta). Va escrito acá y no se toma de la API: quien verifica no le cree a
# CryptoCapi cuál es la excepción.
TEXT_ORDER_DAY = "2026-09-30"

DAY = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
DEFAULT_API = "https://api.cryptocapi.com"
ANCHORS_PATH = "/v1/history/anchors"


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str = ""


def ecmascript_number(x: float) -> str:
    """El número como lo escribe ECMAScript, que es lo que pide JCS (RFC 8785)."""
    if x == 0:
        return "0"  # también -0
    if x < 0:
        return "-" + ecmascript_number(-x)
    _, digits_t, exp = Decimal(repr(x)).normalize().as_tuple()
    assert isinstance(exp, int)
    digits = "".join(map(str, digits_t))
    k = len(digits)
    n = k + exp  # valor = 0.d1d2…dk × 10^n
    if k <= n <= 21:
        return digits + "0" * (n - k)
    if 0 < n <= 21:
        return digits[:n] + "." + digits[n:]
    if -6 < n <= 0:
        return "0." + "0" * (-n) + digits
    e = n - 1
    e_str = ("+" if e > 0 else "-") + str(abs(e))
    return (digits if k == 1 else digits[0] + "." + digits[1:]) + "e" + e_str


def encode_value(column: str, text: str | None) -> str:
    if text is None:
        return "null"
    if column in INT_COLUMNS:
        if not re.fullmatch(r"-?[0-9]+", text):
            raise ValueError(f"{column}: no es un entero: {text}")
        n = int(text)
        if abs(n) > 2**53 - 1:
            raise ValueError(f"{column}: fuera de ±(2^53 − 1): {text}")
        return str(n)
    if column in FLOAT_COLUMNS:
        if not PG_FLOAT.fullmatch(text):
            raise ValueError(f"{column}: no es un float8 de Postgres: {text}")
        x = float(text)
        if math.isnan(x):
            return '"NaN"'
        if math.isinf(x):
            return '"Infinity"' if x > 0 else '"-Infinity"'
        return ecmascript_number(x)
    return json.dumps(text, ensure_ascii=False)


def canonical_leaf(row: dict[str, str | None]) -> str:
    """La fila en JSON canónico (JCS): las 17 columnas, ordenadas, sin espacios."""
    if sorted(row) != COLUMNS:
        raise ValueError(f"La fila no tiene las 17 columnas de v1: {sorted(row)}")
    return "{" + ",".join(f"{json.dumps(c)}:{encode_value(c, row[c])}" for c in COLUMNS) + "}"


def leaf_sha256(row: dict[str, str | None]) -> str:
    return hashlib.sha256(canonical_leaf(row).encode("utf-8")).hexdigest()


def parse_row(raw: object) -> dict[str, str | None]:
    """El JSON de la fila, acotado a texto o null por columna."""
    if not isinstance(raw, dict):
        raise ValueError("La fila tiene que ser un objeto JSON")
    row: dict[str, str | None] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or not (value is None or isinstance(value, str)):
            raise ValueError(f"La columna {key!r} tiene que ser texto o null, como la imprime Postgres")
        row[key] = value
    return row


def _ids_in_order(day: str, ids: list[str]) -> tuple[bool, str]:
    if all(int(b) > int(a) for a, b in zip(ids, ids[1:])):
        return True, ""
    if day == TEXT_ORDER_DAY and all(b > a for a, b in zip(ids, ids[1:])):
        return True, "orden de texto: la excepción documentada del 2026-09-30"
    return False, ""


@dataclass(frozen=True)
class Manifest:
    day: str
    body: list[str]


def _manifest_checks(manifest: bytes) -> tuple[list[Check], Manifest]:
    """La forma del manifiesto, sin mirar ninguna fila."""
    checks: list[Check] = []
    text = manifest.decode("utf-8")
    checks.append(Check("el manifiesto termina en LF", text.endswith("\n")))
    lines = text[:-1].split("\n") if text.endswith("\n") else text.split("\n")
    header = HEADER.fullmatch(lines[0])
    checks.append(Check("la cabecera es la de v1", header is not None, lines[0]))
    day = header.group(1) if header else ""
    body = lines[1:]
    matches = [LINE.fullmatch(line) for line in body]
    checks.append(Check("cada línea es «id hoja»", all(matches)))
    checks.append(Check("las líneas son tantas como dice la cabecera", header is not None and int(header.group(2)) == len(body), str(len(body))))
    ids = [m.group(1) for m in matches if m]
    in_order, note = _ids_in_order(day, ids)
    checks.append(Check("los ids van en orden", in_order, note))
    return checks, Manifest(day, body)


def _row_checks(row: dict[str, str | None], leaf: str, manifest: Manifest) -> list[Check]:
    """Que el recibo sea de ese día y que su hoja esté en la línea de su id."""
    recorded = row.get("recorded_at") or ""
    expected = f"{row.get('id')} {leaf}"
    position = manifest.body.index(expected) + 2 if expected in manifest.body else None
    return [
        Check("el recibo es del día del manifiesto", recorded[:10] == manifest.day, f"{recorded} / {manifest.day}"),
        Check("la hoja está en el manifiesto, en la línea de su id", position is not None, f"línea {position}" if position else ""),
    ]


def _ots_checks(manifest: bytes, ots: bytes) -> list[Check]:
    """Que el .ots sea la prueba de ese manifiesto y que ya tenga su bloque."""
    digest = hashlib.sha256(manifest).hexdigest()
    return [
        Check("el .ots es una prueba de archivo con SHA-256", ots[:33] == OTS_FILE_SHA256_HEADER),
        Check("el .ots certifica la huella del manifiesto", ots[33:65].hex() == digest, digest),
        Check(
            "el .ots trae la atestación de un bloque de Bitcoin",
            OTS_BITCOIN_ATTESTATION in ots,
            "" if OTS_BITCOIN_ATTESTATION in ots else "todavía pendiente: actualizalo en opentimestamps.org o con `ots upgrade`",
        ),
    ]


def verify(row: dict[str, str | None], manifest: bytes, ots: bytes) -> list[Check]:
    leaf = leaf_sha256(row)
    manifest_checks, parsed = _manifest_checks(manifest)
    return [
        Check("la fila tiene las 17 columnas de v1", True, f"hoja {leaf}"),
        *manifest_checks,
        *_row_checks(row, leaf, parsed),
        *_ots_checks(manifest, ots),
    ]


def verify_published(
    day: str,
    entry: dict[str, object],
    manifest: bytes,
    ots: bytes,
    row: dict[str, str | None] | None = None,
) -> list[Check]:
    """
    Un día tal como lo publica la API: los dos archivos, la fila si la hay, y
    que la lista diga lo mismo que los archivos. El orden de ids esperado no se
    toma de la lista: sale de TEXT_ORDER_DAY.
    """
    manifest_checks, parsed = _manifest_checks(manifest)
    head: list[Check] = []
    row_part: list[Check] = []
    if row is not None:
        leaf = leaf_sha256(row)
        head = [Check("la fila tiene las 17 columnas de v1", True, f"hoja {leaf}")]
        row_part = _row_checks(row, leaf, parsed)
    digest = hashlib.sha256(manifest).hexdigest()
    expected_order = "text" if day == TEXT_ORDER_DAY else "numeric"
    listed = [
        Check("la lista publica la huella del manifiesto", entry.get("manifest_sha256") == digest, str(entry.get("manifest_sha256"))),
        Check("la lista dice tantas filas como el manifiesto", entry.get("row_count") == len(parsed.body), str(entry.get("row_count"))),
        Check("la lista declara el orden de ids de ese día", entry.get("id_order") == expected_order, str(entry.get("id_order"))),
    ]
    return [
        *head,
        *manifest_checks,
        Check("el manifiesto es del día pedido", parsed.day == day, parsed.day),
        *row_part,
        *listed,
        *_ots_checks(manifest, ots),
    ]


def fetch(url: str) -> bytes:
    """Un GET y nada más. Los tests lo reemplazan para no salir a la red."""
    request = urllib.request.Request(url, headers={"User-Agent": "cryptocapi-verificador/1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        body: bytes = response.read()
    return body


def anchor_entry(listing: object, day: str) -> dict[str, object] | None:
    """La fila del día en la lista publicada (GET /v1/history/anchors), o None si no está."""
    data = listing.get("data") if isinstance(listing, dict) else None
    anchors = data.get("anchors") if isinstance(data, dict) else None
    if not isinstance(anchors, list):
        raise ValueError("la lista no trae data.anchors")
    for entry in anchors:
        if isinstance(entry, dict) and entry.get("day") == day:
            return {str(key): value for key, value in entry.items()}
    return None


def _report(checks: list[Check]) -> int:
    for check in checks:
        print(("OK     " if check.ok else "FALLA  ") + check.name + (f"  | {check.detail}" if check.detail else ""))
    failures = sum(not c.ok for c in checks)
    print(f"\n{len(checks) - failures} de {len(checks)} comprobaciones bien.")
    return failures


def main_dia(args: list[str]) -> int:
    """--dia AAAA-MM-DD [fila.json] [--api URL]: baja el día de la API y lo verifica."""
    api = DEFAULT_API
    if "--api" in args:
        i = args.index("--api")
        if i + 1 >= len(args):
            print(__doc__)
            return 2
        api = args[i + 1].rstrip("/")
        args = args[:i] + args[i + 2 :]
    if not 1 <= len(args) <= 2 or not DAY.fullmatch(args[0]):
        print(__doc__)
        return 2
    day = args[0]
    listing_url = f"{api}{ANCHORS_PATH}"
    manifest_url, ots_url = f"{listing_url}/{day}/manifest", f"{listing_url}/{day}/ots"

    row: dict[str, str | None] | None = None
    if len(args) == 2:
        try:
            row = parse_row(json.loads(Path(args[1]).read_text(encoding="utf-8")))
            leaf_sha256(row)
        except ValueError as e:
            print(f"FALLA  la fila no tiene la forma del formato v1  | {e}")
            return 1

    try:
        entry = anchor_entry(json.loads(fetch(listing_url)), day)
        if entry is None:
            print(f"FALLA  el {day} no está en la lista del historial anclado  | {listing_url}")
            return 1
        manifest = fetch(manifest_url)
        ots = fetch(ots_url)
    except urllib.error.HTTPError as e:
        print(f"FALLA  la API respondió {e.code}  | {e.url}")
        return 1
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"FALLA  no se pudo llegar a la API  | {e}")
        return 1
    except ValueError as e:
        print(f"FALLA  la lista publicada no tiene la forma esperada  | {e}")
        return 1

    try:
        checks = verify_published(day, entry, manifest, ots, row)
    except ValueError as e:
        print(f"FALLA  el manifiesto no es texto UTF-8  | {e}")
        return 1
    if _report(checks):
        return 1
    print(
        f"Falta el último paso: bajá {manifest_url} y {ots_url}, y en https://opentimestamps.org arrastrá "
        f"primero el .ots y después el manifiesto. Tiene que decir el bloque {entry.get('bitcoin_block')}, que es el que publica la lista."
    )
    return 0


def main(argv: list[str]) -> int:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    if argv[:1] == ["--dia"]:
        return main_dia(argv[1:])
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        row = parse_row(json.loads(Path(argv[0]).read_text(encoding="utf-8")))
        checks = verify(row, Path(argv[1]).read_bytes(), Path(argv[2]).read_bytes())
    except ValueError as e:
        print(f"FALLA  la fila no tiene la forma del formato v1  | {e}")
        return 1
    if _report(checks):
        return 1
    print("Falta el último paso: arrastrá el .ots y el manifiesto a https://opentimestamps.org para ver el bloque de Bitcoin.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
