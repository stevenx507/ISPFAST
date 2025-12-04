ispmax/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── clients.py
│   │   │   ├── mikrotik.py
│   │   │   ├── billing.py
│   │   │   ├── admin.py
│   │   │   ├── provisioning.py
│   │   │   └── monitoring.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── mikrotik_service.py
│   │   │   ├── mikrotik_advanced_service.py
│   │   │   ├── autoprovision_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── billing_service.py
│   │   │   ├── ai_support_service.py
│   │   │   └── cache_service.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── validators.py
│   │   │   └── helpers.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── schemas.py
│   ├── migrations/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── wsgi.py
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── EnhancedDashboard.tsx
│   │   │   ├── EnhancedSpeedTest.tsx
│   │   │   ├── ProfessionalDashboard.tsx
│   │   │   ├── AutoProvisioningWizard.tsx
│   │   │   ├── ClientSimpleDashboard.tsx
│   │   │   ├── BillingWidget.tsx
│   │   │   └── SupportChat.tsx
│   │   ├── contexts/
│   │   │   └── ThemeContext.tsx
│   │   ├── pages/
│   │   │   ├── ClientDashboard.tsx
│   │   │   ├── AdminPanel.tsx
│   │   │   ├── Login.tsx
│   │   │   └── Provisioning.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── auth.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   ├── .eslintrc.js
│   └── Dockerfile
├── mobile/
│   ├── src/
│   │   ├── screens/
│   │   │   ├── DashboardScreen.tsx
│   │   │   └── LoginScreen.tsx
│   │   ├── components/
│   │   └── navigation/
│   ├── app.json
│   ├── package.json
│   └── babel.config.js
├── scripts/
│   ├── mikrotik/
│   │   ├── advanced_professional_v7.rsc
│   │   ├── advanced_professional_v6.rsc
│   │   ├── zero_touch_provisioning.rsc
│   │   ├── client_self_service.rsc
│   │   ├── qos_enterprise.rsc
│   │   └── hotspot_captive.rsc
│   ├── deployment/
│   │   ├── setup.sh
│   │   └── deploy_cpanel.sh
│   └── monitoring/
│       ├── prometheus.yml
│       └── alertmanager.yml
├── docs/
│   ├── INSTALL.md
│   ├── MIKROTIK_SETUP.md
│   ├── API_DOCS.md
│   └── DEPLOYMENT.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
