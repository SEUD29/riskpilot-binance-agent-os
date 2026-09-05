# RiskPilot Architecture

```text
User natural-language trade idea
            |
            v
     RiskPilot AI Agent
            |
      Binance Agent OS / MCP
            |
      Live market context
            |
            v
   ┌─────────────────────┐
   │ Market analysis     │
   │ Bull / Bear cases   │
   │ Confidence          │
   └──────────┬──────────┘
              v
   ┌─────────────────────┐
   │ Deterministic risk  │
   │ engine              │
   └──────────┬──────────┘
              v
       ALLOW / REVIEW / BLOCK
              |
       explicit user review
              |
       future execution adapter
```

## Agent OS integration

The intended live integration uses Binance Agent OS/MCP market-data tools. The official Agent OS MCP endpoint is:

`https://agent.binance.com/mcp/agentic`

Expected market context can include ticker, candlesticks, order book, and funding-rate information depending on the connected tools and permissions.

## Local demo fallback

`market_data.py` uses Binance public 24-hour market data so the repository can be demonstrated without private API keys. This is explicitly a fallback and is **not** presented as an Agent OS connection.

## Security model

RiskPilot keeps execution separate from analysis in the MVP. No API secrets are stored in the repository and no order is automatically submitted.
