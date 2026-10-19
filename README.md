# Pactora

**Your agent negotiates. PayPal settles.**

Pactora lets AI agents negotiate freelance deals on behalf of clients and freelancers. Once both sides agree, PayPal authorizes the funds, captures them on delivery, and pays out the freelancer.

> Status: scaffold only. The agent and negotiation logic are not built yet.

## Structure

```
pactora/
├── backend/            FastAPI · LangGraph · langchain-openai · SQLAlchemy + Postgres
│   └── app/
│       ├── main.py         FastAPI app + CORS
│       ├── config.py       Settings loaded from backend/.env
│       ├── db.py           SQLAlchemy engine, session, Base
│       ├── routes/         /health, /paypal/test
│       ├── services/
│       │   └── paypal.py   OAuth token, orders, authorize, capture, payouts
│       ├── agents/         (empty) negotiation agents
│       ├── graphs/         (empty) LangGraph workflows
│       └── models/         (empty) SQLAlchemy models
├── frontend/           Next.js 14 (App Router) · TypeScript · Tailwind · shadcn/ui
│   ├── app/            Landing page
│   ├── components/     UI components (shadcn in components/ui)
│   └── lib/api.ts      Backend client
└── render.yaml         Render Blueprint (backend, frontend, Postgres)
```

## Prerequisites

- Python 3.11
- Node.js 20+
- PostgreSQL 14+ (local or Docker)
- A [PayPal Developer](https://developer.paypal.com/dashboard/) sandbox app (client ID and secret)
- An OpenAI API key

## Setup

### 1. Database

With Docker:

```bash
docker run -d --name pactora-db -p 5432:5432 \
  -e POSTGRES_USER=pactora -e POSTGRES_PASSWORD=pactora -e POSTGRES_DB=pactora \
  postgres:16
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then fill in PayPal + OpenAI keys
uvicorn app.main:app --reload --port 8000
```

Check it's running:

- http://localhost:8000/health returns `{"status": "ok", ...}`
- http://localhost:8000/paypal/test returns `{"status": "ok", "token": "ok"}` once the PayPal credentials are valid
- http://localhost:8000/docs has the interactive API docs

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env             # NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

Open http://localhost:3000. The header shows whether the frontend can reach the backend.

## Environment variables

| Variable | Service | Description |
| --- | --- | --- |
| `PAYPAL_CLIENT_ID` | backend | PayPal REST app client ID |
| `PAYPAL_CLIENT_SECRET` | backend | PayPal REST app secret |
| `PAYPAL_BASE_URL` | backend | `https://api-m.sandbox.paypal.com` (sandbox) or `https://api-m.paypal.com` (live) |
| `OPENAI_API_KEY` | backend | OpenAI key for the agents |
| `DATABASE_URL` | backend | Postgres URL. `postgres://` and `postgresql://` are both accepted |
| `CORS_ORIGINS` | backend | Extra comma-separated allowed origins. `localhost:3000` is always allowed |
| `NEXT_PUBLIC_API_URL` | frontend | Backend base URL. Applied at build time |

## PayPal flow

`backend/app/services/paypal.py` wraps the payment lifecycle:

1. `create_order(amount, intent="AUTHORIZE")`: creates an order. The buyer approves it via the `approve` link.
2. `authorize_order(order_id)`: holds the funds.
3. `capture_authorization(authorization_id)`: captures the held funds on delivery.
4. `create_payout(email, amount)`: pays the freelancer. Payouts must be enabled on the sandbox account.

## Deploy to Render

1. Push this repo to GitHub.
2. In Render, choose **New → Blueprint** and select the repo. `render.yaml` creates the backend, the frontend and a Postgres database.
3. Fill in the secrets when prompted:
   - backend: `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `OPENAI_API_KEY`, and `CORS_ORIGINS` set to the frontend URL
   - frontend: `NEXT_PUBLIC_API_URL` set to the backend URL
4. `NEXT_PUBLIC_API_URL` is baked in at build time. If you change it, redeploy the frontend.

## License

[MIT](LICENSE)
