from agent import MarketSnapshot, analyze_trade
from models import Decision, TradeRequest


def test_agent_returns_structured_decision_with_market_context():
    request = TradeRequest(
        symbol="BTCUSDT",
        side="BUY",
        notional_usdt=100,
        leverage=2,
        stop_loss_pct=2,
        account_equity_usdt=1000,
    )
    result = analyze_trade(request, MarketSnapshot("BTCUSDT", 100000, 2.5))
    assert result.action == Decision.ALLOW.value
    assert "Bull case:" in result.explanation
    assert "Bear case:" in result.explanation
    assert "Confidence:" in result.explanation
