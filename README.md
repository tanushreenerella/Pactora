# Pactora

> **Your agent negotiates. PayPal settles.**

Pactora is an agent-to-agent commerce platform. A client describes a job, their AI agent negotiates in parallel with multiple freelancer agents, and once the client approves a deal, payment is authorized and held through PayPal. When the work is delivered and approved, the payment is captured and paid out to the freelancer automatically.

Built for the **PayPal AI Hackathon 2026**.

---

## How it works

1. **Post a job.** "Logo design, $100 max, 5 days"
2. **Agents negotiate.** The client agent negotiates with several freelancer agents (each with its own rates, speed and style) over multiple rounds.
3. **Human approves.** The client reviews a ranked shortlist with reasoning and approves one deal.
4. **Payment held.** A PayPal order is created with `intent=AUTHORIZE`, so funds are held, not charged.
5. **Delivery approved.** The freelancer marks the work delivered and the client approves it.
6. **Settled.** The authorization is captured and the freelancer is paid via PayPal Payouts.

---

## Tech stack

| Layer | Tech |
|---|---|
| Agents | LangGraph, LangChain |
| Backend | FastAPI (Python 3.11), SQLAlchemy, PostgreSQL |
| Payments | PayPal REST API (Orders, Payouts), PayPal Agent Toolkit (sandbox) |
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind, shadcn/ui |
| Deployment | Render |

---

## Project structure

```
pactora/
├── backend/
│   ├── agents/          # client + freelancer agent definitions
│   ├── graphs/          # LangGraph negotiation workflows
│   ├── models/          # DB models
│   ├── services/
│   │   └── paypal.py    # PayPal API wrapper
│   ├── config.py
│   └── main.py
├── frontend/
│   ├── app/
│   └── lib/api.ts
├── render.yaml
├── .env.example
└── LICENSE
```

---

## Getting started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (local, or a free cloud instance such as Render or Neon)
- A PayPal Developer account: https://developer.paypal.com/
- An LLM API key (OpenAI, Anthropic or Gemini)

### 1. Set up the PayPal sandbox

1. Log in to the [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/).
2. Go to **Apps & Credentials** (Sandbox mode), then **Create App**.
3. Copy the **Client ID** and **Secret**.
4. Under **Sandbox → Accounts**, make sure you have:
   - a **Business** account (acts as the platform / receives funds)
   - a **Personal** account (acts as the client / buyer)
5. Enable **Payouts** for your sandbox app if it isn't already on.

### 2. Clone the repo

```bash
git clone https://github.com/<your-username>/pactora.git
cd pactora
```

### 3. Configure environment variables

```bash
cp .env.example backend/.env
```

Fill in `backend/.env`:

```env
PAYPAL_CLIENT_ID=your_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_sandbox_secret
PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com
OPENAI_API_KEY=your_llm_key
DATABASE_URL=postgresql://user:password@localhost:5432/pactora
```

For the frontend, create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_PAYPAL_CLIENT_ID=your_sandbox_client_id
```

### 4. Run the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Check that it works:

- http://localhost:8000/health returns `{"status": "ok"}`
- http://localhost:8000/paypal/test confirms the PayPal sandbox token was fetched

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000.

---

## Testing the payment flow (for judges)

Use the sandbox **Personal** account credentials below when PayPal asks you to log in during checkout:

```
Email:    <sandbox-personal-email>
Password: <sandbox-personal-password>
```

No real money is moved; everything runs on the PayPal sandbox.

---

## Deployment

The repo includes a `render.yaml` blueprint for both services.

1. Push the repo to GitHub.
2. On [Render](https://render.com), choose **New → Blueprint** and select the repo.
3. Add the environment variables from step 3 in the Render dashboard.
4. Deploy.

Live demo: `<add link>`
Demo video: `<add YouTube link>`

---

## Roadmap

- [x] Project scaffold + PayPal sandbox connection
- [ ] Freelancer agent personas
- [ ] LangGraph negotiation graph (parallel, multi-round)
- [ ] Human-in-the-loop deal approval
- [ ] PayPal authorize → capture → payout flow
- [ ] Live negotiation UI + deal timeline
- [ ] Dispute flow (stretch)

---

## License

This project is licensed under the [MIT License](LICENSE).
