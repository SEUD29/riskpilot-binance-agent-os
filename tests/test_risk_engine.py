from models import Decision, TradeRequest
from risk_engine import evaluate_trade


def base(**overrides):
    data = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "notional_usdt": 100,
        "leverage": 2,
        "stop_loss_pct": 2,
        "account_equity_usdt": 1000,
    }
    data.update(overrides)
    return TradeRequest(**data)


def test_safe_trade_allows():
    result = evaluate_trade(base())
    assert result.decision == Decision.ALLOW
    assert result.risk_pct == 0.2


def test_missing_stop_requires_review():
    result = evaluate_trade(base(stop_loss_pct=None))
    assert result.decision == Decision.REVIEW


def test_excessive_notional_blocks():
    result = evaluate_trade(base(notional_usdt=300))
    assert result.decision == Decision.BLOCK


def test_excessive_leverage_requires_review_or_block():
    result = evaluate_trade(base(leverage=6))
    assert result.decision in {Decision.REVIEW, Decision.BLOCK}


def test_invalid_side_blocks():
    result = evaluate_trade(base(side="HOLD"))
    assert result.decision == Decision.BLOCK
