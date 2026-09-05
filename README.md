# 🛡️ RiskPilot — Binance Agent OS Safety Layer

**RiskPilot** is a safety-first AI-agent workflow for the Binance Agent OS Mini Hackathon (Track A). It takes a proposed crypto trade, combines Binance market context with deterministic risk controls, explains the bull and bear cases, and returns a transparent `ALLOW`, `REVIEW`, or `BLOCK` decision before execution.

## Why RiskPilot?

Trading agents can act quickly, but speed without a safety layer can turn a reasonable idea into an oversized or poorly bounded position. RiskPilot is designed as the decision gate between user intent and any future execution action.

### Core workflow

`User trade idea → RiskPilot agent → Binance Agent OS/MCP market context → Bull/Bear analysis → Risk engine → Confidence → ALLOW / REVIEW / BLOCK`

## What the MVP does

- Validates BUY/SELL trade requests
- Checks position size against account equity
- Checks leverage against a conservative maximum
- Calculates estimated stop-loss risk as a percentage of equity
- Flags missing downside protection
- Produces bull and bear cases when market context is available
- Reports confidence and a 0–100 risk score
- Keeps order execution **disabled** in the MVP
- Includes a polished browser demo and automated tests

## Binance Agent OS / MCP

RiskPilot is designed to use Binance Agent OS/MCP market-data capabilities. The configured official MCP endpoint is:

`https://agent.binance.com/mcp/agentic`

The agent workflow is designed around market tools such as ticker, candlesticks, order book, and funding-rate context when those tools are available through the connected Agent OS environment.

**Important:** the local `market_data.py` provider is a public Binance market-data fallback for an easy standalone demo. It does not pretend to be an Agent OS connection.

## Run the demo locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000` and try:

- BTCUSDT
- BUY
- 100 USDT position
- 2x leverage
- 2% stop loss
- 1,000 USDT equity

Then try 6x leverage or a 300 USDT position to demonstrate a stricter decision.

## Project structure

```text
.
├── app.py                    # Browser demo + API
├── agent.py                  # Agent decision layer and prompt
├── market_data.py            # Public Binance demo fallback
├── models.py                 # Typed request/result models
├── risk_engine.py            # Deterministic safety rules
├── prompts/
│   └── riskpilot_system.md   # Agent behavior specification
├── docs/
│   ├── ARCHITECTURE.md       # Agent OS architecture
│   └── DEMO_SCRIPT.md        # 60-second hackathon demo
├── tests/
│   ├── test_agent.py
│   └── test_risk_engine.py
├── SUBMISSION.md              # Hackathon checklist + X draft
└── requirements.txt
```

## Risk logic

The default policy uses three important guardrails:

1. Position notional must not exceed 25% of account equity.
2. Leverage must not exceed 5x.
3. Stop-loss risk should remain within the configured account-risk limit (default 2%).

The result is intentionally explainable:

- **ALLOW** — configured safety checks pass.
- **REVIEW** — the trade is within some limits but needs human review or has a failed safety check that does not force a block.
- **BLOCK** — a critical constraint such as invalid direction or excessive position size is violated.

These are prototype policies, not financial advice.

## Tests

```bash
pytest -q
```

## Hackathon demo

See [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) for a 60-second recording plan and [`SUBMISSION.md`](SUBMISSION.md) for the Track A submission checklist and ready-to-post X copy.

## Security

No API keys, passwords, wallet secrets, or private credentials belong in this repository. Execution remains disabled in the MVP. A future execution adapter should require explicit user confirmation immediately before placing an order.

## Disclaimer

RiskPilot is a hackathon prototype for educational and demonstration purposes. It is not financial advice and does not guarantee safe or profitable trading.
