from models import Decision, RiskResult, TradeRequest


def evaluate_trade(request: TradeRequest) -> RiskResult:
    reasons: list[str] = []
    checks: dict[str, bool] = {}
    risk_pct = 0.0

    checks["notional_limit"] = request.notional_usdt <= request.account_equity_usdt * 0.25
    if not checks["notional_limit"]:
        reasons.append("Position notional exceeds 25% of account equity.")

    checks["leverage_limit"] = request.leverage <= 5
    if not checks["leverage_limit"]:
        reasons.append("Leverage is above the conservative 5x limit.")

    if request.stop_loss_pct is not None:
        risk_pct = (request.notional_usdt * request.stop_loss_pct / 100) / request.account_equity_usdt * 100
        checks["risk_limit"] = risk_pct <= request.risk_limit_pct
        if not checks["risk_limit"]:
            reasons.append(f"Estimated stop-loss risk is {risk_pct:.2f}% of equity, above the {request.risk_limit_pct:.2f}% limit.")
    else:
        checks["risk_limit"] = False
        reasons.append("No stop-loss was provided; downside risk cannot be bounded.")

    checks["valid_side"] = request.side.upper() in {"BUY", "SELL"}
    if not checks["valid_side"]:
        reasons.append("Side must be BUY or SELL.")

    failed = sum(not value for value in checks.values())
    if not checks["valid_side"] or not checks["notional_limit"]:
        decision = Decision.BLOCK
    elif failed:
        decision = Decision.REVIEW
    elif request.leverage > 3 or risk_pct > request.risk_limit_pct * 0.75:
        decision = Decision.REVIEW
        reasons.append("Trade is within limits but close enough to a risk threshold to require review.")
    else:
        decision = Decision.ALLOW
        reasons.append("All configured risk checks passed.")

    score = max(0, min(100, int(100 - (failed * 25) - max(0, request.leverage - 1) * 5)))
    return RiskResult(decision=decision, score=score, risk_pct=round(risk_pct, 4), reasons=reasons, checks=checks)
