from dataclasses import dataclass
from typing import Any

from models import AgentDecision, TradeRequest
from risk_engine import evaluate_trade


SYSTEM_PROMPT = """
You are RiskPilot, a safety-first crypto market analysis agent connected to Binance Agent OS.

Your job is to analyze a user's proposed crypto trade using Binance market data available through
Agent OS/MCP, then produce a transparent decision. Never invent market data. Distinguish facts,
inferences, and uncertainty. Always provide a bull case, bear case, risk level, confidence, and
an actionable verdict: ALLOW, REVIEW, or BLOCK.

RiskPilot is recommendation-only in this MVP. Do not place an order automatically. If execution is
ever enabled in a future version, require explicit user confirmation immediately before execution.
""".strip()


@dataclass
class MarketSnapshot:
    symbol: str
    last_price: float
    change_24h_pct: float
    high_24h: float | None = None
    low_24h: float | None = None
    source: str = "Binance Agent OS"


def analyze_trade(request: TradeRequest, market: MarketSnapshot | None = None) -> AgentDecision:
    """Deterministic agent decision layer; market context can be supplied by Agent OS/MCP."""
    risk = evaluate_trade(request)

    market_line = "Market snapshot unavailable; connect Binance Agent OS/MCP for live context."
    bull = "A bullish case cannot be confirmed without live market data."
    bear = "A bearish case cannot be confirmed without live market data."
    confidence = "Low"

    if market is not None:
        market_line = (
            f"{market.symbol}: {market.last_price:.4f}, 24h change {market.change_24h_pct:.2f}%"
        )
        if market.change_24h_pct > 1:
            bull = "Positive 24h momentum supports the bullish case, but momentum alone is not confirmation."
            bear = "A reversal remains possible after a strong move; wait for confirmation and respect the stop."
            confidence = "Medium"
        elif market.change_24h_pct < -1:
            bull = "A rebound is possible, but it needs evidence beyond the current negative 24h move."
            bear = "Negative 24h momentum supports the bearish case and increases reversal risk for longs."
            confidence = "Medium"
        else:
            bull = "Price action is relatively neutral over 24h; a breakout could strengthen the bullish case."
            bear = "Neutral momentum can resolve lower; lack of confirmation keeps downside uncertainty elevated."
            confidence = "Low"

    explanation = (
        f"{market_line}\n"
        f"Bull case: {bull}\n"
        f"Bear case: {bear}\n"
        f"Confidence: {confidence}\n"
        f"Risk score: {risk.score}/100\n"
        f"Risk reasons: {'; '.join(risk.reasons)}"
    )

    return AgentDecision(action=risk.decision.value, explanation=explanation, risk=risk)


def tool_manifest() -> dict[str, Any]:
    """Documents the tools RiskPilot expects from Binance Agent OS/MCP."""
    return {
        "name": "RiskPilot",
        "purpose": "Analyze a proposed crypto trade using Binance data before execution.",
        "binance_agent_os": {
            "mcp_endpoint": "https://agent.binance.com/mcp/agentic",
            "required_scope": "market data",
            "execution": "disabled in MVP",
        },
        "market_tools": ["ticker", "candlesticks", "order_book", "funding_rate"],
        "workflow": [
            "parse user intent",
            "retrieve live Binance context",
            "analyze bull and bear cases",
            "run deterministic risk checks",
            "return confidence and ALLOW/REVIEW/BLOCK verdict",
        ],
    }
