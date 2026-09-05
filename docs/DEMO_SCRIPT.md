# 60-Second Hackathon Demo Script

## Screen recording

**0–8s — Intro**

Show the RiskPilot homepage and say:
> "This is RiskPilot, a safety layer for Binance Agent OS that checks a trade before execution."

**8–20s — User intent**

Enter:
- Symbol: `BTCUSDT`
- Side: `BUY`
- Position: `100 USDT`
- Leverage: `2x`
- Stop loss: `2%`
- Account equity: `1,000 USDT`

Say:
> "I give it a proposed trade instead of blindly executing it."

**20–38s — Analysis**

Click **Analyze trade**. Show the live market source, bull case, bear case, confidence, and risk score.

Say:
> "RiskPilot combines market context with deterministic risk checks and explains both the bullish and bearish cases."

**38–50s — Safety decision**

Change leverage to `6x` or position size to `300 USDT`, then analyze again. Show `REVIEW` or `BLOCK`.

Say:
> "When the trade crosses a safety threshold, RiskPilot refuses to treat it as a normal trade and flags it for review or blocks it."

**50–60s — Agent OS + close**

Show the GitHub README/architecture briefly.

Say:
> "The architecture is designed for Binance Agent OS/MCP, while the MVP keeps execution disabled so the risk decision stays transparent and user-controlled."

## Recording tips

- Record the screen, not yourself, unless you want to.
- Keep the video around 45–60 seconds.
- Make sure the final `ALLOW/REVIEW/BLOCK` result is readable.
- Do not show API keys, passwords, wallet secrets, or private account information.
