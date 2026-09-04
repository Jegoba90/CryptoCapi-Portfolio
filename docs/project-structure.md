# 🗺️ CryptoCapi — Estructura del Proyecto

Monorepo de 3 servicios (Backend Node, Collector Python, Frontend Vite) con contratos compartidos. El núcleo del producto son **3 motores**: **Radar** (NLP/IA), **Quant Pro** (matemático/Binance) y **Quant Plus** (on-chain, 100% determinista).

```
cryptocapi-refactor/
│
├── 📄 Raíz (monorepo + documentación)
│   ├── README.md                       # Documentación principal
│   ├── PRODUCT_SPECIFICATIONS.md       # Especificación de los 3 motores
│   ├── TECHNICAL_CONSTITUTION.md       # Leyes de ingeniería CTC-2026
│   ├── BUSINESS_RULES.md               # Definiciones de dominio
│   ├── firebase.json / .firebaserc     # Firebase hosting + functions
│   ├── firestore.rules                 # Reglas de seguridad Firestore
│   ├── cloudbuild.yaml                 # Cloud Build (raíz)
│   ├── package.json                    # Workspace root + scripts lint:all
│   └── LICENSE                         # MIT License
│
├── 📂 backend/                         # API Node.js 24 + TypeScript (Cloud Run)
│   ├── src/
│   │   ├── api/                        # Express app, middlewares, router
│   │   │   ├── express.ts              # Express app builder
│   │   │   ├── middlewares/            # Auth, validation (Zod), errors
│   │   │   └── routes/                 # Main router
│   │   ├── modules/                    # Business modules (hexagonal)
│   │   │   ├── access/                 # API keys, plans, B2B auth
│   │   │   ├── asset/                  # Assets (coins, tokens)
│   │   │   ├── internal/               # Internal endpoints (collector -> backend)
│   │   │   ├── market/                 # Market data, insights, ETF, macro
│   │   │   ├── payments/               # Stripe / monetization
│   │   │   ├── proxy/                  # Requests proxy
│   │   │   └── quant/                  # Quant Pro (on-demand proxy to engine)
│   │   ├── workers/                    # sanitizer.worker.ts (worker threads)
│   │   ├── scripts/                    # init-db, generate-key, audits
│   │   ├── shared/                     # Config, logger, cache (Redis), DB (Neon)
│   │   ├── types/                      # Type definitions
│   │   └── app.ts                      # Entry point (port 3000)
│   ├── openapi.yaml                    # OpenAPI Spec of public API
│   ├── ARCHITECTURE.md                 # Backend architecture docs
│   ├── tests/                          # Jest tests (domain)
│   ├── tsconfig.json
│   └── Dockerfile
│
├── 📂 collector/                       # Python 3.12 — Radar + Quant Plus (Cloud Run Job)
│   ├── services/
│   │   ├── insight_service.py          # 📡 RADAR — NLP/LLM narrative (LLM engine multi-model)
│   │   ├── quant_service.py            # ⛓️ QUANT PLUS — on-chain, 100% deterministic (no AI)
│   │   ├── insights_common.py          # Shared Radar/Quant Plus code + post-LLM filters
│   │   ├── math_engine.py              # MathContext: Z-Score (t-Student), Bollinger, regime
│   │   ├── onchain_manager.py          # On-chain: Alchemy (ETH gas) + Mempool.space (BTC)
│   │   ├── api_client.py               # CoinGecko API client
│   │   ├── yfinance_client.py          # Yahoo Finance client (90d daily)
│   │   ├── fred_client.py              # Federal Reserve API client (macro)
│   │   ├── world_bank_client.py        # World Bank API client (global inflation)
│   │   └── news_scraper.py             # RSS news feed ingestor
│   ├── quant/                          # 📊 QUANT PRO — Binance math engine (deterministic)
│   │   ├── engine.py                   # Dual-timeframe analysis orchestrator (1D/4H)
│   │   ├── connectors/                 # binance_rest.py (4-mirror), binance_ws.py
│   │   ├── core/                       # kalman, indicators, confluence, regime, constants
│   │   ├── models/                     # schemas.py (Pydantic)
│   │   └── tests/                      # Engine tests (kalman, confluence, regime, engine)
│   ├── models/                         # Pydantic models
│   ├── utils/                          # seal.py (protocol_hash SHA-256), logger, formatters, http
│   ├── config/                         # settings.py, shared_config.py
│   ├── database/                       # PostgreSQL connection
│   ├── tests/unit/                     # Unit tests (post-LLM filters, seal)
│   ├── tools/                          # Diagnostics scripts (divergence, type-check)
│   ├── main.py                         # Entry point + schedulers (cycles)
│   ├── quant_server.py                 # HTTP Micro-server on-demand (port 8000/8080)
│   └── Dockerfile
│
├── 📂 frontend/                        # Vite + Vanilla TypeScript (Firebase Hosting)
│   ├── src/
│   │   ├── core/                       # App init, router, events, domain (DDD),
│   │   │                               #   agentCatalog (.well-known), sitemapRoutes
│   │   ├── features/                   # access, api, api-management, auth, community,
│   │   │                               #   docs, home, market, methodology, portfolio,
│   │   │                               #   precios, search, status, shared
│   │   ├── services/                   # API layer + Firebase (auth, firestore)
│   │   ├── shared/                     # UI components, utils (formatters, state, EventBus)
│   │   ├── config/                     # Endpoints, constants
│   │   ├── types/                      # TypeScript definitions
│   │   └── css/                        # Tailwind + custom CSS
│   ├── scripts/                        # generate-agent-mirror (.md mirror, per deploy)
│   ├── tests/                          # Playwright E2E tests
│   ├── public/                         # Static assets + llms.txt, robots.txt, sitemap.xml
│   └── vite.config.js / playwright.config.js
│
├── 📂 shared/                          # 🔗 Shared contracts (source of truth)
│   ├── schemas/                        # Zod: asset, market, quant, response (AuditTrail)
│   ├── types/                          # contracts.ts, models.ts (DTOs Frontend <=> Backend)
│   ├── utils/                          # configLoader.ts
│   └── config.json                     # Shared configuration values
│
├── 📂 functions/                       # Firebase Cloud Functions (index.js)
│
├── 📂 infra/                           # 🏗️ Infrastructure and deployment
│   ├── deploy.ps1                      # Multi-service deployment script
│   ├── docker-compose.yml              # Local docker-compose configuration
│   ├── nginx.conf                      # Nginx reverse proxy config
│   └── sql/                            # migrations/, scripts/, schema.sql
│
├── 📂 docs/                            # 📚 Technical documentation
│   ├── ANTI_HALLUCINATION_SEAL.md      # Pipeline + protocol_hash of the 3 engines
│   ├── CLOUD_INFRASTRUCTURE.md         # GCP topology + deployment guide
│   ├── LOCAL_DEVELOPMENT_GUIDE.md      # Local development setup guide
│   ├── PRE_PRODUCTION_GUIDE.md         # Pre-production validation checklist
│   ├── project-structure.md            # This file
│   └── monitoring.md                   # Observability configuration
│
└── 📂 .github/                         # 🛠️ Configuración y automatizaciones de GitHub
    ├── 📂 workflows/                   # Recetas/instrucciones de GitHub Actions (CI/CD)
    │   ├── quality-gate.yml            # Orquestador del Quality Gate (linters, tipos, tests)
    │   ├── playwright.yml              # Automatización de pruebas E2E del frontend
    │   ├── deploy.yml                  # Automatización del deploy a GCP Cloud Run/Hosting
    │   └── setup-branch-protection.yml # Automatización de políticas de protección de ramas
    ├── dependabot.yml                  # Alertas y actualización automática de librerías
    └── copilot-instructions.md         # Reglas de contexto y comportamiento para Copilot
```
