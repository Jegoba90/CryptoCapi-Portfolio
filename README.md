<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo-white.png">
  <img src="assets/logo-navy.png" alt="CryptoCapi" width="120"/>
</picture>

# CryptoCapi · Análisis Cuantitativo Sin Alucinaciones



Plataforma de análisis de criptomonedas con tres motores especializados, dos puramente matemáticos y uno con IA auditada por Python, para que los números nunca mientan. Sobre ellos, Market Scan rankea el universo con las señales de Quant Plus.

<br/>

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-5FA04E?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Cloud_Run-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

<br/>

![Estado](https://img.shields.io/badge/estado-en_producción-success?style=flat-square)
![Type Safe](https://img.shields.io/badge/type--safe-strict-blue?style=flat-square)
![CI](https://img.shields.io/badge/CI-quality--gate-blueviolet?style=flat-square)
![Tests](https://img.shields.io/badge/tests-Jest_·_Vitest_·_Pytest_·_Playwright-orange?style=flat-square)

</div>

---

## 📋 Tabla de Contenidos

- [El problema que resolvemos](#-el-problema-que-resolvemos)
- [Arquitectura · Tres Motores y Market Scan](#-arquitectura--tres-motores-y-market-scan)
- [Pipeline Anti-Alucinación · Defensa en 4 Capas](#️-pipeline-anti-alucinación--defensa-en-4-capas)
- [Probalo ahora](#-probalo-ahora)
- [Stack Tecnológico Completo](#️-stack-tecnológico-completo)
- [Principios de Ingeniería](#️-principios-de-ingeniería)
- [Outputs de ejemplo · Qué devuelve cada motor](#-outputs-de-ejemplo--qué-devuelve-cada-motor)
- [Nativo para agentes](#-nativo-para-agentes)
- [Documentación API](#-documentación-api)
- [Filosofía](#-filosofía)

---

## 🎯 El problema que resolvemos

> Los modelos de lenguaje **alucinan**. En finanzas, una alucinación cuesta dinero real.

CryptoCapi resuelve esto con una arquitectura donde la **IA solo interpreta narrativa** (noticias, sentimiento)
y **toda decisión numérica la calcula matemática verificable**: Z-Scores, filtros de Kalman y confluencia
de indicadores técnicos, sobre cierres diarios de Yahoo Finance y velas de Binance.

<div align="center">

**No te decimos qué comprar. Te damos la matemática pura para que decidas vos.**

</div>

---

## 🧠 Arquitectura · Tres Motores y Market Scan

| Motor | Rol | Tecnología clave |
|:---|:---|:---|
| 📡 **Motor Radar** | Ingesta cinco fuentes RSS verificadas (CoinDesk, The Block, Decrypt, CryptoSlate, Bitcoin Magazine) y genera sentimiento + resúmenes ejecutivos sin sensacionalismo. Cada fuente entra con su tier de credibilidad, y la matemática determinista valida o invalida la narrativa antes de publicarla. | `Python` · `LLM engine (multi-model)` · `feedparser` · `BeautifulSoup` |
| 📊 **Motor Quant PRO** | Señal cuantitativa on-demand sobre cualquier par de Binance: filtro de Kalman adaptativo para reducir ruido, cinco indicadores técnicos y Matriz de Intercepción de Régimen (MIR) dual-timeframe 1D/4H. | `NumPy` · `SciPy` · `Pandas` · `TA-Lib` · `Binance REST` |
| 📈 **Motor Quant Plus** | Señales estadísticas pre-computadas sobre 51 cierres diarios: el retorno logarítmico del último día contra los 49 anteriores, con umbral t-Student (α=0.001 del modelo; con precios reales de cripto se cruza cerca de 1 de cada 75 días por moneda), e insight accionable con sello SHA-256 reproducible. En BTC y ETH suma contexto on-chain (congestión de red, actividad de ballenas), que se informa aparte y no mueve la señal. | `NumPy` · `SciPy` · `Pydantic` · `Mempool RPC` |
| 🧭 **Market Scan** (capa, no motor) | Ranking del universo curado por fuerza de señal, armado sobre las señales de Quant Plus: no corre modelo propio, y se vende aparte, con su propio pase. Deja fuera a las stablecoins mientras aguantan la paridad: si una se despega, vuelve al ranking, porque un *depeg* es una señal. | `TypeScript` · `PostgreSQL` |

### Cobertura por motor

| Motor | Universo de activos | Ejecución | Latencia típica |
|:---|:---|:---|:---|
| 📡 Radar | ~15 monedas curadas | Pre-computado (scheduler) | < 100 ms |
| 📊 Quant PRO | Cualquier par USDT de Binance | On-demand por request | ~2-3 s |
| 📈 Quant Plus | ~15 monedas curadas | Pre-computado (scheduler) | < 100 ms |
| 🧭 Market Scan | Universo curado de Quant Plus | Lee las señales de Quant Plus | < 100 ms |

> Las ~15 monedas curadas incluyen 10 fijas (BTC, ETH, SOL, BNB, XRP, DOGE, TRX, USDT, USDC, LEO) más hasta 5 adicionales seleccionadas dinámicamente por volatilidad ≥ 5% en 24h del top 20 por market cap.

---

## 🛡️ Pipeline Anti-Alucinación · Defensa en 4 Capas

> El LLM redacta la narrativa. **Python certifica los números y vigila las palabras.** La IA nunca tiene la última palabra sobre una cifra.

| Capa | Qué hace |
|:---|:---|
| **1 · Determinista** | Python calcula *todos* los valores numéricos (Bandas de Bollinger, Z-Score logarítmico, régimen de mercado) **antes** de invocar al LLM. |
| **2 · Narrativa** | Los valores deterministas se inyectan en el prompt como contexto *no negociable*; el LLM solo escribe texto sobre cifras ya fijadas. |
| **3 · Override numérico** | Tras la respuesta del LLM, Python **sobrescribe** métricas, sentiment y confidence con los valores deterministas. |
| **4 · Filtrado léxico** | Filtros deterministas eliminan frases alucinadas que sobrevivieron al prompt, usando *gates* basados en Z-Score y sentiment. |

**Umbrales fijos y a la vista:** cambios de volatilidad extrema o rupturas de bandas estadísticas disparan alertas automáticas. Una anomalía se declara cuando el Z-Score cruza el valor crítico de la t de Student (3,5051 con 48 grados de libertad), y ese umbral viaja en cada respuesta PRO como `z_score_threshold`.

La resiliencia de IA se apoya en **cadenas de fallback multi-modelo sobre buckets de cuota independientes** con *backoff* exponencial, de modo que ningún motor agote la capacidad de otro.

---

## 🚀 Probalo ahora

**Sin key.** La vista pulse de Radar es pública, siempre que pases `view=pulse` en la URL (sin el parámetro, la ruta pide key):

```bash
curl "https://api.cryptocapi.com/v1/market/insights/bitcoin?view=pulse"
```

**Sin registro.** La demo key pública (limitada a BTC y ETH, 30 req/hora por IP) devuelve el payload Alpha completo, sello `audit_trail` incluido:

```bash
curl -H "x-api-key: demo_btc_eth_public" \
  "https://api.cryptocapi.com/v1/market/insights/bitcoin?view=alpha"
```

**En tu terminal.** El agente open source [anti-hallucination-crypto-agent](https://github.com/Jegoba90/anti-hallucination-crypto-agent) consume esta API en vivo, muestra qué eliminó o sobrescribió el pipeline sobre la salida de la IA (`filters_applied`, `fields_overridden`) y te enseña a verificar el `protocol_hash` por tu cuenta. Viene con la demo key precargada: clonar y ejecutar.

**Trial PRO de 14 días, sin tarjeta,** para el resto de monedas y los motores Quant: [cryptocapi.com](https://www.cryptocapi.com)

---

## 🛠️ Stack Tecnológico Completo

### 🎨 Frontend
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=threedotjs&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-DD2C00?style=for-the-badge&logo=firebase&logoColor=white)
![Zod](https://img.shields.io/badge/Zod-3E67B1?style=for-the-badge&logo=zod&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-5A0FC8?style=for-the-badge&logo=pwa&logoColor=white)

> `Prism.js` · `DOMPurify` (sanitización XSS) · `Temporal API`

### ⚙️ Backend / API
![Node.js](https://img.shields.io/badge/Node.js-5FA04E?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express_5-000000?style=for-the-badge&logo=express&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Swagger](https://img.shields.io/badge/OpenAPI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![Sentry](https://img.shields.io/badge/Sentry-362D59?style=for-the-badge&logo=sentry&logoColor=white)

> `Helmet` · `CORS` · `express-rate-limit` · `compression` · `bcryptjs` · `Pino` (logging) · `email transaccional` · `Zod` (validación end-to-end)

### 🐍 Motor Cuantitativo (Python · Data Science)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

> `TA-Lib` (análisis técnico) · `LLM engine (multi-model)` · `feedparser` · `BeautifulSoup4` · `cloudscraper` · `WebSockets` · `APScheduler`

### 🗄️ Datos & Persistencia
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-FF4438?style=for-the-badge&logo=redis&logoColor=white)

> PostgreSQL serverless · Redis gestionado · arquitectura cache-first con TTL

### ☁️ DevOps & Infraestructura
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Cloud_Run-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![Cloud Build](https://img.shields.io/badge/Cloud_Build-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase_Hosting-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

> Despliegue multi-servicio containerizado · `Docker Compose` (dev/staging/prod) · Container Registry

### ✅ Calidad & Testing
![Jest](https://img.shields.io/badge/Jest-C21325?style=for-the-badge&logo=jest&logoColor=white)
![Vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![ESLint](https://img.shields.io/badge/ESLint-4B32C3?style=for-the-badge&logo=eslint&logoColor=white)
![Prettier](https://img.shields.io/badge/Prettier-F7B93E?style=for-the-badge&logo=prettier&logoColor=black)
![Ruff](https://img.shields.io/badge/Ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=black)

> Tipado estricto verificado con `Mypy` · `Pyright` · `type-coverage` · análisis de código muerto con `knip` · duplicación y complejidad con `jscpd` y `SonarJS`, que frenan el código nuevo en el CI

---

## 📂 Estructura del Proyecto

El monorepo está organizado de forma clara y modular, separando la interfaz de usuario (Vite), la API (Node) y los servicios de recopilación/análisis cuantitativo (Python).

Conocé la distribución detallada de archivos y carpetas de cada módulo en el mapa de directorios:
👉 **[Mapa Detallado de Estructura del Proyecto (docs/project-structure.md)](docs/project-structure.md)**

---

## ⚖️ Principios de Ingeniería

> Reglas constitucionales que todo Pull Request debe cumplir.

- **Zero-Any**: prohibido `any` en TypeScript y Python; lo desconocido es `unknown` + *type guards*.
- **Tipos opacos de dominio**: `CoinId`, `WalletId` y `TransactionId` nunca son `string` planos; el compilador rechaza pasar un ID donde se espera otro, eliminando en compilación la clase entera de bugs "usé el identificador equivocado".
- **Exhaustividad verificada por el compilador**: todo `switch` sobre una unión discriminada cierra con `assertNever`; añadir un caso nuevo y olvidar manejarlo rompe el build señalando archivo y línea, nunca en producción.
- **Arquitectura Hexagonal**: el dominio nunca depende de la infraestructura; cambiar la base de datos no toca la lógica de negocio.
- **Contratos compartidos**: única fuente de verdad de tipos entre frontend y backend; nadie adivina la forma de la API.
- **Cronometría determinista**: `Temporal` API en lugar de `Date` nativo; sin errores de zona horaria/DST en software financiero.
- **Validación paranoica**: `Zod .strict()` por defecto en el backend + `Pydantic` en el collector; `.passthrough()` permitido solo en fronteras de confianza documentadas (engine interno, proveedor externo, config de infraestructura), nunca en entrada de usuario; validación bilateral antes de persistir.
- **Sello criptográfico verificable**: cada motor firma sus resultados con un `protocol_hash` SHA-256 sobre inputs/outputs deterministas; alterar cualquier campo cubierto invalida el sello (*tamper-evidence*). Semántica honesta por motor: `reproducible` (recalculable sin dependencias), `output_seal` (re-verificable contra el origen) y `process_seal` (certifica el proceso, no el texto del LLM).
- **Value Objects**: el dinero nunca es un `number` crudo; se encapsula inmutable para impedir estados inválidos.
- **Gestión explícita de recursos**: `using` / `await using` cierran las conexiones serverless automáticamente y evitan fugas.
- **Cache-First**: Redis gestionado con TTL delante de PostgreSQL en todo `GET` público.
- **Degradación honesta**: en modo *fallback*, la confianza reportada nunca es `HIGH`.
- **Type-safe de extremo a extremo**: verificado con `Mypy`, `Pyright` y `type-coverage`.
- **Quality Gate en CI**: GitHub Actions corre tipos, linters, tests (Jest, Vitest, Pytest), auditoría de dependencias y escaneo de secretos en cada push.
- **Seguridad & observabilidad**: `Helmet`, rate limiting, sanitización XSS (DOMPurify), `bcrypt`; error monitoring y logs estructurados.

---

## 🔬 Outputs de ejemplo · Qué devuelve cada motor

> Respuestas reales del sistema sobre **BTC**, desde producción. Radar, capturado el **2026-10-29** con la demo key pública y el motor `v2.4.0-radar`; Quant Plus, el **2026-10-30**, con `v2.5.0-math`; Quant PRO, el **2026-10-03**, con `v1.2.0-quant`. Quant Plus es además el caso de verificación de [SEAL.md](docs/SEAL.md): su vector trae un precio entero y una docena de empates exactos, así que ejercita la regla canónica de números en vez de suponerla. Cada sello dice su `engine_version`, y SEAL.md explica qué regla aplica a cada versión.

<details>
<summary>📡 Motor Radar · Sentimiento sobre fuentes verificadas · sello audit_trail</summary>

```json
{
  "status": "success",
  "version": "1.0.0",
  "timestamp": "2026-10-29T12:04:32.178Z",
  "data": {
    "engine_used": "radar",
    "asset": { "id": "bitcoin", "symbol": "BTC" },
    "generated_at": "2026-10-29T12:04:32.178Z",
    "summary": "Lateralización de rango.",
    "sentiment": "neutral",
    "statistical_anomaly_detected": false,
    "confidence": {
      "score": 0.62,
      "label": "MEDIUM"
    },
    "math_diagnostics": {
      "z_score": 0.2868,
      "z_score_threshold": 3.5051,
      "bollinger_bandwidth": 0.0525,
      "market_regime": "RANGING_CHOP",
      "extreme_volatility_detected": false,
      "data_quality": "OPTIMAL",
      "data_quality_reason": [],
      "sentiment_override": false,
      "anomaly_details": null,
      "regime_thresholds": {
        "volatility_hard_limit": 0.05,
        "z_score_anomaly_boundary": 3.5051,
        "daily_change_trend_boundary": 0.02
      },
      "audit_trail": {
        "protocol_hash": "0xa4a30c19a7e547155c2a53bf990012be10a2009fee791855e1970338adb65aac",
        "calculated_at": "2026-10-29T12:04:32.107500Z",
        "seal_type": "process_seal",
        "algorithm_id": "Radar 4-Layer Anti-Hallucination Pipeline",
        "engine_version": "v2.4.0-radar",
        "filters_applied": [
          "magnitude inflation"
        ],
        "fields_overridden": [
          "analysis.anomaly_details",
          "analysis.confidence",
          "analysis.detailed_report",
          "analysis.sentiment_score",
          "confidence",
          "is_volatility_alert"
        ],
        "sentiment_override": false
      }
    },
    "analysis": {
      "detailed_report": "Tensión Latente: La reciente divulgación de que una entidad de custodia no puede retirar BTC genera inquietud, pero no constituye un catalizador decisivo. El precio opera en la zona inferior de las Bandas de Bollinger, indicando una posición de rango estable sin señales claras de ruptura. La acción de precio se mantiene dentro de la zona de soporte natural, con poca presión alcista o bajista.",
      "sources_verified": [
        {
          "title": "Bitcoin Treasury Datavault AI Says It Can’t Access Its BTC, Stock Tanks",
          "url": "https://decrypt.co/382116/bitcoin-treasury-datavault-ai-stock-crashes-cant-access-btc",
          "credibility": "Tier 2"
        }
      ],
      "sources_window": "24h"
    }
  }
}
```

> El `audit_trail` declara qué corrigió Python sobre la salida del LLM: `fields_overridden` lista los campos sobrescritos con valores deterministas y `filters_applied`, los filtros léxicos que se dispararon. En esta captura saltó uno, `magnitude inflation`, y el pipeline llegó a reescribir el propio `detailed_report`. Cómo verificar el hash: [SEAL.md](docs/SEAL.md). La respuesta va entera, sin recortar, y está commiteada tal cual en [api/examples/radar-alpha.json](api/examples/radar-alpha.json).

</details>

<details>
<summary>📊 Motor Quant PRO · Análisis cuantitativo multi-timeframe</summary>

```json
{
  "status": "success",
  "version": "1.0.0",
  "timestamp": "2026-10-03T16:55:01.283Z",
  "data": {
    "asset": {
      "id": "btc",
      "symbol": "BTCUSDT"
    },
    "symbol": "BTCUSDT",
    "resolved_signal": "BUY",
    "resolved_score": 65,
    "mir_diagnostics": {
      "base_raw_score": 65,
      "insufficient_data": false,
      "conviction_multiplier": 1,
      "explanation": "Sin contracción de convicción: las dos temporalidades tienen al menos 50 velas."
    },
    "macro_1d": {
      "timeframe": "1d",
      "confluence_score": 65,
      "signal": "BUY",
      "indicators": {
        "ema_cross_score": 30,
        "rsi_score": 20,
        "macd_score": 0,
        "bollinger_score": 0,
        "kalman_score": 15
      },
      "candle_count": 500,
      "timestamp": "2026-10-03T16:55:00.630512Z"
    },
    "micro_4h": {
      "timeframe": "4h",
      "confluence_score": 55,
      "signal": "NEUTRAL_CHOP",
      "indicators": {
        "ema_cross_score": 30,
        "rsi_score": 10,
        "macd_score": 0,
        "bollinger_score": 0,
        "kalman_score": 15
      },
      "candle_count": 1000,
      "timestamp": "2026-10-03T16:55:01.211530Z"
    },
    "version": "v1.2.0-quant",
    "audit_trail": {
      "protocol_hash": "0xbffe1e8746bffdfba216cbff2490d5d077754a2827edddb99656abb90d9e3ab6",
      "calculated_at": "2026-10-03T16:55:01.212238Z",
      "seal_type": "output_seal",
      "algorithm_id": "Kalman-Adaptive + Confluence (Dual-Timeframe MIR)",
      "engine_version": "v1.2.0-quant"
    }
  }
}
```

> `resolved_signal` dice cuántos indicadores coinciden: STRONG es una confluencia alta, no una probabilidad ni un pronóstico. Con menos de 50 velas en alguna temporalidad, `mir_diagnostics.insufficient_data` sale en `true` y la distancia del score a 50 se reduce a la mitad. La respuesta va entera en [api/examples/quant-pro-signal.json](api/examples/quant-pro-signal.json).

</details>

<details>
<summary>📈 Motor Quant Plus · Sello reproducible</summary>

Este es el motor cuyo sello **podés recalcular vos**. El vector de entrada abajo viene abreviado para que se lea; la respuesta completa, con sus 51 precios y sus 51 marcas de tiempo, está commiteada en [`api/examples/quant-plus-signal.json`](api/examples/quant-plus-signal.json), y **ese archivo verifica**: seguí los pasos de [docs/SEAL.md](docs/SEAL.md) y vas a obtener el mismo hash.

```json
{
  "status": "success",
  "version": "1.0.0",
  "timestamp": "2026-10-30T12:03:11.627Z",
  "data": {
    "engine_used": "quant_plus",
    "asset": { "id": "bitcoin", "symbol": "BTC" },
    "generated_at": "2026-10-30T12:03:11.627Z",
    "summary": "Volatilidad inusual con sesgo bajista. Z-Score -2.51, al 72% de su umbral de anomalía (3.51).",
    "sentiment": "bearish",
    "statistical_anomaly_detected": false,
    "confidence": {
      "score": 0.97,
      "label": "HIGH"
    },
    "onchain_stats": {
      "network": "bitcoin-mainnet",
      "network_congestion": "LOW",
      "onchain_confidence_score": 0.9
    },
    "actionable_insight": {
      "signal": "HOLD",
      "risk_level": "MEDIUM"
    },
    "math_diagnostics": {
      "z_score": -2.5118,
      "z_score_threshold": 3.5051,
      "bollinger_bandwidth": 0.0675,
      "market_regime": "UNUSUAL_VOLATILITY",
      "extreme_volatility_detected": false,
      "data_quality": "OPTIMAL",
      "sentiment_override": false,
      "anomaly_details": null,
      "audit_trail": {
        "protocol_hash": "0x333c8f30a7ee653d4ede8b823641a342b51e8bc0b87eaf3739cbc673b7633d98",
        "calculated_at": "2026-10-30T12:03:11.570655Z",
        "seal_type": "reproducible",
        "algorithm_id": "SMA-20 / 2σ / 50-period Z-Score (Returns)",
        "engine_version": "v2.5.0-math",
        "data_source": {
          "vendor": "Yahoo Finance (51 daily closes)",
          "symbol": "BTC-USD",
          "timeframe": "1d (50-period log_returns Z-Score)"
        },
        "input_timestamps": ["2026-09-09T00:00:00Z", "…", "2026-10-29T00:00:00Z"],
        "input_vector": [78259.5234375, "…", 77775.109375],
        "zscore_window_size": 49,
        "daily_change_pct": -4.297503
      }
    },
    "analysis": {
      "detailed_report": "Régimen de mercado: volatilidad inusual. Precio opera por debajo de la banda inferior de Bollinger. Z-Score (-2.51) señala desviación bajista significativa. Ancho de banda en expansión — volatilidad creciente."
    }
  }
}
```

</details>

---

## 📖 Documentación API

| Documento | Descripción |
|:---|:---|
| [AUTHENTICATION.md](docs/AUTHENTICATION.md) | API keys, planes, rate limits y payload shaping por tier |
| [ENGINES.md](docs/ENGINES.md) | Universo de monedas, latencias, endpoints y cuándo usar cada motor |
| [SEAL.md](docs/SEAL.md) | Qué garantiza el sello Math Override Certified y cómo verificarlo |
| [SIGNAL_HISTORY.md](docs/SIGNAL_HISTORY.md) | El historial de señales anclado en Bitcoin: los endpoints públicos, sin clave, y cómo verificar un día con [`tools/verificar_recibo.py`](tools/verificar_recibo.py) |

---

## 🤖 Nativo para agentes

El API está pensado para que lo consuma una máquina, no solo una persona. Y desde 2026 hay tres caminos: el servidor MCP, el sitio legible por agentes y el descubrimiento por catálogos. Ninguno pide que escribas glue code.

### Servidor MCP nativo

Si tu cliente habla **Model Context Protocol**, no hace falta escribir integración: los motores son herramientas nativas.

```json
{
  "mcpServers": {
    "cryptocapi": {
      "command": "npx",
      "args": ["-y", "@cryptocapi/mcp"]
    }
  }
}
```

Ese bloque es el formato de Cursor (`.cursor/mcp.json` en el proyecto, o `~/.cursor/mcp.json` para todos), Windsurf y Claude Desktop. **VS Code (GitHub Copilot) usa otra forma:** el archivo es `.vscode/mcp.json`, la clave es `servers` y no `mcpServers`, y cada servidor lleva `"type": "stdio"`.

```json
{
  "servers": {
    "cryptocapi": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@cryptocapi/mcp"]
    }
  }
}
```

En **Claude Code** y **Codex** es un solo comando. En Claude Code, sin `--scope user` queda solo en el proyecto donde lo corriste.

```bash
claude mcp add --transport stdio cryptocapi -- npx -y @cryptocapi/mcp
codex mcp add cryptocapi -- npx -y @cryptocapi/mcp
```

Eso es todo. Sin key, el paquete cae en la key pública de demostración y `get_insight` responde para bitcoin y ethereum, con su sello incluido. Para usar la tuya, sumá `CRYPTOCAPI_API_KEY` al `env` del bloque, o `--env CRYPTOCAPI_API_KEY=…` al comando (en Claude Code, antes de `--transport`).

| Herramienta | Motor | Qué devuelve |
|:---|:---|:---|
| `get_insight` | Radar o Quant Plus | Análisis de un activo. Con `engine="quant_plus"`, el sello reproducible y su vector de entrada |
| `get_signal` | Quant Pro | Señal de ejecución para un par de trading |
| `batch_signals` | Quant Plus | Señales de varios activos en una llamada |
| `scan_market` | Market Scan | Ranking del universo curado por fuerza de señal |

Cuatro herramientas, y **las cuatro devuelven inteligencia propia**: los tres motores y el ranking de Market Scan. El dato de terceros (precios, macro) se retiró de esta superficie a propósito: por MCP viaja solo lo que nuestros motores firman.

El paquete es un **cliente delgado, no una segunda implementación**. Consume el mismo API público que cualquier otro consumidor y reenvía las respuestas **verbatim**, así que el `protocol_hash` que llega a tu agente es idéntico byte a byte al que sirvió el API. Se publica desde CI con **procedencia npm (SLSA)**, sin ningún token de larga vida: la única vía de publicar es un tag firmado sobre [el repositorio público](https://github.com/Jegoba90/cryptocapi-mcp).

Y cuando un motor no está incluido en tu pase, el error lo dice con nombre propio y con un código que tu agente puede ramificar, en vez de un 403 pelado que lo deje reintentando en círculos.

Está dado de alta en el **registro oficial de MCP** como [`io.github.Jegoba90/cryptocapi`](https://registry.modelcontextprotocol.io/v0/servers?search=cryptocapi), con la propiedad del paquete verificada contra el tarball publicado en npm. Los clientes que leen ese registro lo encuentran sin que nadie les pase una URL.

### El sitio, legible por un agente

El sitio es una SPA renderizada en el cliente: hasta hace poco, cualquier ruta devolvía el mismo cascarón HTML de 44 KB. Un agente sin navegador se llevaba el marco y nada del contenido. Ya no.

**Agregá `.md` a la URL de una página y te devuelve esa página en markdown**, generada desde la página misma en cada despliegue:

```bash
curl https://www.cryptocapi.com/docs/agentes.md
```

| Documento | URL |
|:---|:---|
| Portada | [`/.md`](https://www.cryptocapi.com/.md) |
| Referencia del API | [`/docs/api.md`](https://www.cryptocapi.com/docs/api.md) |
| Guía de IA y agentes | [`/docs/agentes.md`](https://www.cryptocapi.com/docs/agentes.md) |
| Documentación | [`/docs.md`](https://www.cryptocapi.com/docs.md) |
| Metodología y verificación del sello | [`/methodology.md`](https://www.cryptocapi.com/methodology.md) |
| Términos | [`/terms.md`](https://www.cryptocapi.com/terms.md) |
| Privacidad | [`/privacy.md`](https://www.cryptocapi.com/privacy.md) |

> **Ramificá por el `Content-Type`, no por el código de estado.** Una URL `.md` sin espejo devuelve **200 con el cascarón HTML**, así que `text/markdown` es la única señal fiable de que el espejo existe. Es el error más fácil de cometer contra esta superficie, y por eso está escrito acá.

**El dato de mercado no tiene página ni espejo, a propósito.** Precios y resumen de mercado son dato de terceros que sirve el API; publicarlos como páginas convertiría el sitio en un feed gratis de aquello para lo que están los motores. La ausencia es una decisión, no un hueco.

### Descubrimiento: que no haya que adivinar nada

El dominio **anuncia dónde está todo lo legible por máquina** con una cabecera `Link` en cada respuesta, apuntando a dos catálogos:

| Catálogo | Qué es |
|:---|:---|
| [`/.well-known/api-catalog`](https://www.cryptocapi.com/.well-known/api-catalog) | Linkset **RFC 9727**: el documento OpenAPI, la referencia navegable y el endpoint de salud |
| [`/.well-known/ai-catalog.json`](https://www.cryptocapi.com/.well-known/ai-catalog.json) | Enumera todos los recursos legibles por máquina, uno por uno |

Y el contrato **se puede bajar, no solo mirar**: [`/v1/openapi.json`](https://api.cryptocapi.com/v1/openapi.json) sirve el documento OpenAPI en sí, no el Swagger UI. La proyección publicada filtra los servidores de desarrollo, así que un cliente generado no puede terminar apuntando a `localhost`.

Para clientes que no hablan MCP, el archivo [`llms.txt`](https://www.cryptocapi.com/llms.txt) **en vivo** es el índice de entrada: qué hace cada motor, cómo autenticarse, y desde dónde seguir hacia el resto de los documentos.

| Recurso | Para qué sirve |
|:---|:---|
| [`@cryptocapi/mcp` en npm](https://www.npmjs.com/package/@cryptocapi/mcp) | El servidor MCP nativo, con procedencia verificable |
| [Código del servidor MCP](https://github.com/Jegoba90/cryptocapi-mcp) | El fuente, sus pruebas manuales y la tabla de cada herramienta |
| [`llms.txt` en vivo](https://www.cryptocapi.com/llms.txt) | Índice legible por agentes: motores, autenticación y a dónde ir después |
| [Contrato OpenAPI descargable](https://api.cryptocapi.com/v1/openapi.json) | El documento en sí, para generar un cliente |
| [Referencia navegable del API](https://api.cryptocapi.com/v1/docs) | El mismo contrato, para leerlo con ojos humanos |
| [Guía de IA y agentes](https://www.cryptocapi.com/docs/agentes) | Cómo integrar el API dentro de un flujo agéntico |
| [Bot de trading con Claude](https://www.cryptocapi.com/guias/bot-de-trading-con-claude) | Claude analiza con números sellados por MCP, sin inventarlos |
| [Señales para tu bot de trading](https://www.cryptocapi.com/guias/bot-de-trading) | La misma idea desde Python: la señal es nuestra, la orden la manda tu exchange |

**Funciona donde construyas:** Claude Code · Codex · Cursor · VS Code (GitHub Copilot) · LangChain · cualquier cliente REST. ChatGPT no puede lanzar el servidor MCP, porque sus conectores solo llegan a servidores remotos y este corre local.

¿Querés verlo funcionando? El agente open source [anti-hallucination-crypto-agent](https://github.com/Jegoba90/anti-hallucination-crypto-agent) consume este API en vivo y verifica el sello por su cuenta. Es el ejemplo ejecutable de todo lo anterior.

---

<div align="center">

## 💜 Filosofía

> ### *"Nosotros no te decimos qué comprar.*
> ### *Te damos la matemática pura para que decidas vos."*

<br/>

### Hecho con 💜 y matemática pura

**por el equipo de CryptoCapi**

Detrás de cada Z-Score hay gente que cree que los números no deberían mentirle a nadie.

<br/>

**Líder de proyecto:** Jesús González · [@Jegoba90](https://github.com/Jegoba90)

<br/>

![Hecho con](https://img.shields.io/badge/hecho_con-corazón_y_matemática_pura-blueviolet?style=for-the-badge)

<br/>

<a href="https://www.cryptocapi.com">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-white.png">
    <img src="assets/logo-navy.png" alt="CryptoCapi" width="72"/>
  </picture>
</a>

</div>
