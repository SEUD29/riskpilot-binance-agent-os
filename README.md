# RiskPilot — Binance Agent OS Risk Guard

RiskPilot is a lightweight AI-agent safety layer for Binance Agent OS. It converts a proposed natural-language trading workflow into structured risk checks before an execution step is allowed.

## What it does

- Validates a proposed BUY/SELL trade
- Checks position notional against account equity
- Checks leverage against a conservative limit
- Estimates stop-loss risk as a percentage of equity
- Returns `ALLOW`, `REVIEW`, or `BLOCK`
- Explains every failed or passed check
- Provides a simple browser demo

## Architecture

`User intent → Agent/LLM → TradeRequest → Risk Engine → Decision → (future) Binance Agent OS execution`

The current MVP deliberately keeps execution separate from risk evaluation. A future adapter can pass only approved actions to Binance Agent OS/MCP after explicit user confirmation.

## Example

A 100 USDT BTCUSDT position on a 1,000 USDT account with 2x leverage and a 2% stop has estimated account risk of 0.20%, so it can pass the configured checks.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open `http://127.0.0.1:8000`.

## Configuration

Copy `.env.example` to `.env` for future Agent OS/MCP integration settings. No API keys or secrets belong in the repository.

## Binance Agent OS

RiskPilot is designed to sit before Binance Agent OS trading actions. Agent OS provides an MCP endpoint and agentic capabilities; RiskPilot adds a transparent, deterministic risk gate so the agent can explain why a proposed action is allowed, needs review, or is blocked.

## Hackathon MVP

Track A: AI Agent / workflow. The MVP focuses on a clear safety-oriented trading workflow rather than autonomous order placement. The demo can show a user request, structured risk evaluation, and the resulting decision.

## Disclaimer

This project is a hackathon prototype and is not financial advice. It does not guarantee safe or profitable trading.
