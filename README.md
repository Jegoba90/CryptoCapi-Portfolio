<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo-white.png">
  <img src="assets/logo-navy.png" alt="CryptoCapi" width="120"/>
</picture>

# CryptoCapi · Análisis Cuantitativo Sin Alucinaciones



Plataforma de análisis de criptomonedas con tres motores especializados, dos puramente matemáticos, uno con IA auditada por Python para que los números nunca mientan.

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
- [Arquitectura · Tres Motores Especializados](#-arquitectura--tres-motores-especializados)
- [Pipeline Anti-Alucinación · Defensa en 4 Capas](#️-pipeline-anti-alucinación--defensa-en-4-capas)
- [Pruébalo ahora](#-pruébalo-ahora)
- [Stack Tecnológico Completo](#️-stack-tecnológico-completo)
- [Flujo de Datos](#-flujo-de-datos)
- [Principios de Ingeniería](#️-principios-de-ingeniería)
- [Outputs de ejemplo · Qué devuelve cada motor](#-outputs-de-ejemplo--qué-devuelve-cada-motor)
- [Nativo para agentes](#-nativo-para-agentes)
- [Documentación API](#-documentación-api)
- [Filosofía](#-filosofía)

---

## 🎯 El problema que resolvemos

> Los modelos de lenguaje **alucinan**. En finanzas, una alucinación cuesta dinero real.

CryptoCapi resuelve esto con una arquitectura donde la **IA solo interpreta narrativa** (noticias, sentimiento)
y **toda decisión numérica la calcula matemática verificable** — Z-Scores, filtros de Kalman, exponentes de
Lyapunov y datos on-chain leídos directamente de la blockchain.

<div align="center">

**No te decimos qué comprar. Te damos la matemática pura para que tú decidas.**

</div>

---

## 🧠 Arquitectura · Tres Motores Especializados

| Motor | Rol | Tecnología clave |
|:---|:---|:---|
| 📡 **Motor Radar** | Ingesta noticias institucionales (Bloomberg, Reuters, Cointelegraph) y genera sentimiento + resúmenes ejecutivos sin sensacionalismo. La matemática determinista valida o invalida la narrativa antes de publicarla. | `Python` · `LLM engine (multi-model)` · `feedparser` · `BeautifulSoup` |
| 📊 **Motor Quant PRO** | Señal cuantitativa on-demand sobre cualquier par de Binance: filtro de Kalman adaptativo para reducir ruido, exponente de Lyapunov para detectar caos de mercado y Matriz de Intercepción de Régimen (MIR) dual-timeframe 1D/4H. | `NumPy` · `SciPy` · `Pandas` · `TA-Lib` · `Binance REST` |
| 📈 **Motor Quant Plus** | Señales estadísticas pre-computadas sobre 50 períodos: Z-Score logarítmico con umbral t-Student (α=0.001), enriquecimiento on-chain vía RPC (congestión de red, actividad de ballenas) e insight accionable con sello SHA-256 reproducible. | `NumPy` · `SciPy` · `Pydantic` · `Mempool RPC` |

### Cobertura por motor

| Motor | Universo de activos | Ejecución | Latencia típica |
|:---|:---|:---|:---|
| 📡 Radar | ~15 monedas curadas | Pre-computado (scheduler) | < 100 ms |
| 📊 Quant PRO | Cualquier par USDT de Binance | On-demand por request | ~2-3 s |
| 📈 Quant Plus | ~15 monedas curadas | Pre-computado (scheduler) | < 100 ms |

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

**Umbrales inmutables:** cambios de volatilidad extrema o rupturas de bandas estadísticas disparan alertas automáticas. Anomalías de mercado se detectan mediante umbrales de Z-Score calibrados sobre datos históricos.

La resiliencia de IA se apoya en **cadenas de fallback multi-modelo sobre buckets de cuota independientes** con *backoff* exponencial, de modo que ningún motor agote la capacidad de otro.

---

## 🚀 Pruébalo ahora

**Sin registro.** La demo key pública (limitada a BTC y ETH, 30 req/hora por IP) devuelve el payload Alpha completo, sello `audit_trail` incluido:

```bash
curl -H "x-api-key: demo_btc_eth_public" \
  "https://api.cryptocapi.com/v1/market/insights/bitcoin?view=alpha"
```

**En tu terminal.** El agente open source [anti-hallucination-crypto-agent](https://github.com/Jegoba90/anti-hallucination-crypto-agent) consume esta API en vivo, muestra qué eliminó o sobrescribió el pipeline sobre la salida de la IA (`filters_applied`, `fields_overridden`) y te enseña a verificar el `protocol_hash` por tu cuenta. Viene con la demo key precargada: clonar y ejecutar.

**Trial PRO de 14 días, sin tarjeta,** para el resto de monedas y los motores Quant: [cryptocapi.com](https://cryptocapi.com)

---

## 🛠️ Stack Tecnológico Completo

### 🎨 Frontend
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=threedotjs&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-DD2C00?style=for-the-badge&logo=firebase&logoColor=white)
![Zod](https://img.shields.io/badge/Zod-3E67B1?style=for-the-badge&logo=zod&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-5A0FC8?style=for-the-badge&logo=pwa&logoColor=white)

> `Lightweight Charts` (TradingView) · `Swiper` · `jsVectorMap` · `Prism.js` · `DOMPurify` (sanitización XSS) · `date-fns` · `Temporal API`

### ⚙️ Backend / API
![Node.js](https://img.shields.io/badge/Node.js-5FA04E?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express_5-000000?style=for-the-badge&logo=express&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Swagger](https://img.shields.io/badge/OpenAPI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![Sentry](https://img.shields.io/badge/Sentry-362D59?style=for-the-badge&logo=sentry&logoColor=white)

> `Helmet` · `CORS` · `express-rate-limit` · `compression` · `bcryptjs` · `Pino` (logging) · `email transaccional` · `yahoo-finance2` · `Zod` (validación end-to-end)

### 🐍 Motor Cuantitativo (Python · Data Science)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

> `TA-Lib` (análisis técnico) · `LLM engine (multi-model)` · `Web3` · `Web3 data provider` · `feedparser` · `BeautifulSoup4` · `cloudscraper` · `WebSockets` · `APScheduler`

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

> Despliegue multi-servicio containerizado · `Docker Compose` (dev/staging/prod) · `Cloud Functions` · Container Registry

### ✅ Calidad & Testing
![Jest](https://img.shields.io/badge/Jest-C21325?style=for-the-badge&logo=jest&logoColor=white)
![Vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![ESLint](https://img.shields.io/badge/ESLint-4B32C3?style=for-the-badge&logo=eslint&logoColor=white)
![Prettier](https://img.shields.io/badge/Prettier-F7B93E?style=for-the-badge&logo=prettier&logoColor=black)
![Ruff](https://img.shields.io/badge/Ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=black)

> Tipado estricto verificado con `Mypy` · `Pyright` · `type-coverage` · análisis de código muerto con `ts-prune`

---

## 🔄 Flujo de Datos

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/data-flow-dark.svg">
  <img src="assets/data-flow-light.svg" alt="Flujo de datos de CryptoCapi: tres pipelines independientes en Python. Radar consume noticias Tier 1 y precios, y es el único motor que invoca un LLM, con override determinista posterior. Quant PRO consume velas de Binance y Quant Plus lee la blockchain por RPC; ambos son 100% deterministas. Radar y Quant Plus empujan sus resultados a la API Express, mientras que a Quant PRO lo consulta la API on-demand. La API es la única que persiste en PostgreSQL, cachea en Redis y sirve al frontend." width="100%">
</picture>

</div>

---

## 📂 Estructura del Proyecto

El monorepo está organizado de forma clara y modular, separando la interfaz de usuario (Vite), la API (Node) y los servicios de recopilación/análisis cuantitativo (Python).

Conoce la distribución detallada de archivos y carpetas de cada módulo en el mapa de directorios:
👉 **[Mapa Detallado de Estructura del Proyecto (docs/project-structure.md)](docs/project-structure.md)**

---

## ⚖️ Principios de Ingeniería

> Reglas constitucionales que todo Pull Request debe cumplir.

- **Zero-Any** — prohibido `any` en TypeScript y Python; lo desconocido es `unknown` + *type guards*.
- **Tipos opacos de dominio** — `CoinId`, `WalletId` y `TransactionId` nunca son `string` planos; el compilador rechaza pasar un ID donde se espera otro, eliminando en compilación la clase entera de bugs "usé el identificador equivocado".
- **Exhaustividad verificada por el compilador** — todo `switch` sobre una unión discriminada cierra con `assertNever`; añadir un caso nuevo y olvidar manejarlo rompe el build señalando archivo y línea — nunca producción.
- **Arquitectura Hexagonal** — el dominio nunca depende de la infraestructura; cambiar la base de datos no toca la lógica de negocio.
- **Contratos compartidos** — única fuente de verdad de tipos entre frontend y backend; nadie adivina la forma de la API.
- **Cronometría determinista** — `Temporal` API (ES2025) en lugar de `Date` nativo; sin errores de zona horaria/DST en software financiero.
- **Validación paranoica** — `Zod .strict()` por defecto en el backend + `Pydantic` en el collector; `.passthrough()` permitido solo en fronteras de confianza documentadas (engine interno, proveedor externo, config de infraestructura), nunca en entrada de usuario; validación bilateral antes de persistir.
- **Sello criptográfico verificable** — cada motor firma sus resultados con un `protocol_hash` SHA-256 sobre inputs/outputs deterministas; alterar cualquier campo cubierto invalida el sello (*tamper-evidence*). Semántica honesta por motor: `reproducible` (recalculable sin dependencias), `output_seal` (re-verificable contra el origen) y `process_seal` (certifica el proceso, no el texto del LLM).
- **Value Objects** — el dinero nunca es un `number` crudo; se encapsula inmutable para impedir estados inválidos.
- **Dependencias por arquetipo** — el motor ligero calcula sin NumPy; solo el Quant Engine carga NumPy/Kalman → imágenes Docker mínimas.
- **Gestión explícita de recursos** — `using` / `await using` (ES2025) cierran las conexiones serverless automáticamente y evitan fugas.
- **Cache-First** — Redis gestionado con TTL delante de PostgreSQL en todo `GET` público.
- **Degradación honesta** — en modo *fallback*, la confianza reportada nunca es `HIGH`.
- **Type-safe de extremo a extremo** — verificado con `Mypy`, `Pyright` y `type-coverage`.
- **Quality Gate en CI** — GitHub Actions corre tipos, linters, tests (Jest/Pytest) y E2E (Playwright) en cada push.
- **Seguridad & observabilidad** — `Helmet`, rate limiting, sanitización XSS (DOMPurify), `bcrypt`; error monitoring y logs estructurados.

---

## 🔬 Outputs de ejemplo · Qué devuelve cada motor

> Respuestas reales del sistema sobre **BTC**. Radar capturado el **2026-07-16** con la demo key pública; Quant PRO y Quant Plus, el **2026-05-25**. Los pesos internos de los indicadores no se publican.

<details>
<summary>📡 Motor Radar — Sentimiento institucional · sello audit_trail</summary>

```json
{
  "status": "success",
  "version": "1.0.0",
  "timestamp": "2026-07-16T16:33:49.044Z",
  "data": {
    "engine_used": "radar",
    "asset": { "id": "bitcoin", "symbol": "BTC" },
    "summary": "Equilibrio técnico.",
    "sentiment": "neutral",
    "statistical_anomaly_detected": false,
    "confidence": {
      "score": 0.6,
      "label": "MEDIUM"
    },
    "math_diagnostics": {
      "z_score": 0.015,
      "z_score_threshold": 3.5051,
      "bollinger_bandwidth": 0.1195,
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
        "protocol_hash": "0x1fc3502d2b4632e28c60c8b8dbe5c87bb35df1936c09723d043f9457c27e8f28",
        "calculated_at": "2026-07-16T16:33:48.661922Z",
        "seal_type": "process_seal",
        "algorithm_id": "Radar 4-Layer Anti-Hallucination Pipeline",
        "engine_version": "v2.1.0-radar",
        "filters_applied": [],
        "fields_overridden": [
          "analysis.anomaly_details",
          "analysis.confidence",
          "analysis.sentiment_score",
          "confidence",
          "is_volatility_alert"
        ],
        "sentiment_override": false
      }
    },
    "analysis": {
      "detailed_report": "La posición en Bandas de Bollinger es TERCIO_SUPERIOR. El precio opera en un régimen de lateralización, sin un catalizador fundamental evidente en las noticias recientes.",
      "sources_verified": [
        {
          "title": "The most popular bitcoin call option has slipped by $10,000",
          "url": "https://www.coindesk.com/daybook-us/2026/07/16/the-most-popular-bitcoin-call-option-has-slipped-by-usd10-000",
          "credibility": "Tier 1"
        },
        {
          "title": "Dormant Bitcoin Whale Moves $383 Million After More Than 8 Years",
          "url": "https://decrypt.co/373646/bitcoin-whale-moves-383-million-after-eight-years",
          "credibility": "Tier 2"
        }
      ],
      "sources_window": "24h"
    }
  }
}
```

> El `audit_trail` declara qué corrigió Python sobre la salida del LLM: `fields_overridden` lista los campos sobrescritos con valores deterministas y `filters_applied` los filtros léxicos que se dispararon. Cómo verificar el hash: [SEAL.md](docs/SEAL.md). `sources_verified` está abreviado aquí; la respuesta íntegra está en [api/examples/radar-alpha.json](api/examples/radar-alpha.json).

</details>

<details>
<summary>📊 Motor Quant PRO — Análisis cuantitativo multi-timeframe</summary>

```json
{
  "status": "success",
  "version": "1.0.0",
  "timestamp": "2026-05-25T20:18:36.005Z",
  "data": {
    "asset": { "id": "bitcoin", "symbol": "BTC" },
    "resolved_signal": "NEUTRAL_CHOP",
    "resolved_score": 52,
    "mir_diagnostics": {
      "base_raw_score": 55,
      "chaos_penalty_applied": true,
      "explanation": "Convicción direccional contraída por régimen de caos sistémico detectado."
    },
    "macro_1d": {
      "timeframe": "1d",
      "confluence_score": 55,
      "signal": "NEUTRAL_CHOP",
      "regime": {
        "lyapunov": 1.893,
        "status": "CHAOTIC",
        "signal_confidence": "LOW"
      }
    },
    "micro_4h": {
      "timeframe": "4h",
      "confluence_score": 60,
      "signal": "NEUTRAL_CHOP",
      "regime": {
        "lyapunov": 2.031,
        "status": "CHAOTIC",
        "signal_confidence": "LOW"
      }
    }
  }
}
```

</details>

<details>
<summary>⛓️ Motor Quant Plus — Datos on-chain</summary>

```json
{
  "status": "success",
  "version": "1.0.0",
  "timestamp": "2026-05-25T20:17:29.969Z",
  "data": {
    "engine_used": "quant_plus",
    "asset": { "id": "bitcoin", "symbol": "BTC" },
    "summary": "Equilibrio técnico.",
    "sentiment": "neutral",
    "statistical_anomaly_detected": false,
    "confidence": {
      "score": 0.61,
      "label": "MEDIUM"
    },
    "onchain_stats": {
      "network": "bitcoin-mainnet",
      "network_congestion": "LOW",
      "whale_activity_alert": true,
      "onchain_confidence_score": 0.9
    },
    "actionable_insight": {
      "signal": "HOLD",
      "risk_level": "LOW"
    },
    "math_diagnostics": {
      "z_score": 0.1705,
      "bollinger_bandwidth": 0.0988,
      "market_regime": "RANGING_CHOP",
      "extreme_volatility_detected": false,
      "data_quality": "OPTIMAL",
      "sentiment_override": false,
      "anomaly_details": null
    },
    "analysis": {
      "detailed_report": "Régimen de mercado: lateralización. Precio opera en el tercio inferior de las bandas de Bollinger. Z-Score (0.17) en zona neutral — sin anomalías estadísticas."
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

---

## 🤖 Nativo para agentes

El API está pensado para que lo consuma una máquina, no solo una persona. Un archivo [`llms.txt`](https://www.cryptocapi.com/llms.txt) **en vivo** describe cada endpoint, sus parámetros y la forma de las respuestas en el formato estándar que leen los agentes de IA. Tu asistente en Claude Code, Cursor o Copilot descubre toda la superficie del API por su cuenta, sin que escribas una línea de código de integración.

| Recurso | Para qué sirve |
|:---|:---|
| [`llms.txt` en vivo](https://www.cryptocapi.com/llms.txt) | Mapa legible por agentes de todos los endpoints, autenticación y rate limits |
| [Guía de IA y agentes](https://cryptocapi.com/docs/agentes) | Cómo integrar el API dentro de un flujo agéntico |
| [Especificación OpenAPI](https://api.cryptocapi.com/v1/docs) | Contrato completo y navegable del API v1 |

**Funciona donde construyas:** Claude Code · Cursor · GitHub Copilot · ChatGPT · LangChain · cualquier cliente REST.

¿Quieres verlo funcionando? El agente open source [anti-hallucination-crypto-agent](https://github.com/Jegoba90/anti-hallucination-crypto-agent) consume este API en vivo y verifica el sello por su cuenta. Es el ejemplo ejecutable de todo lo anterior.

---

<div align="center">

## 💡 Filosofía

> ### *"Nosotros no te decimos qué comprar.*
> ### *Te damos la matemática pura para que tú decidas."*

<br/>

**Líder de proyecto:** Jesús González · [@Jegoba90](https://github.com/Jegoba90)

<br/>

![Hecho con](https://img.shields.io/badge/hecho_con-matemática_pura-blueviolet?style=for-the-badge)

<br/>

<a href="https://cryptocapi.com"><img src="assets/banner.png" alt="CryptoCapi — Capibara" width="100%"/></a>

</div>
