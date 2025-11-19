ispmax/
├── backend/
│   ├── app.py                 # Entry point API
│   ├── config.py              # Configuración (Env vars)
│   ├── models.py              # Modelos DB (SQLAlchemy)
│   ├── services/
│   │   ├── mikrotik.py        # Lógica Core RouterOS
│   │   └── billing.py         # Integración Stripe (Mock)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                  # React + Vite
│   ├── src/
│   │   └── App.tsx            # UI Monolítica (Demo)
│   └── Dockerfile
├── scripts/
│   └── mikrotik_qos_security.rsc # Script de provisión RouterOS
├── mobile/                    # React Native (Placeholder)
├── docs/                      # Documentación
├── docker-compose.yml         # Orquestación
└── .env                       # Variables de entorno
