from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import ValidationError

from models import TradeRequest
from risk_engine import evaluate_trade

app = FastAPI(title="RiskPilot", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """<!doctype html>
<html><head><title>RiskPilot</title><meta name='viewport' content='width=device-width,initial-scale=1'></head>
<body style='font-family:system-ui;max-width:760px;margin:40px auto;padding:20px'>
<h1>RiskPilot</h1><p>Binance Agent OS risk guard — analyze a proposed trade before execution.</p>
<form id='f'>
<input id='symbol' value='BTCUSDT' placeholder='Symbol'><br><br>
<select id='side'><option>BUY</option><option>SELL</option></select><br><br>
<input id='notional' type='number' value='100' placeholder='Notional USDT'><br><br>
<input id='leverage' type='number' value='2' step='0.1' placeholder='Leverage'><br><br>
<input id='stop' type='number' value='2' step='0.1' placeholder='Stop loss %'><br><br>
<input id='equity' type='number' value='1000' placeholder='Account equity USDT'><br><br>
<button>Evaluate risk</button></form><pre id='out'></pre>
<script>f.onsubmit=async(e)=>{e.preventDefault();const body={symbol:symbol.value,side:side.value,notional_usdt:+notional.value,leverage:+leverage.value,stop_loss_pct:+stop.value,account_equity_usdt:+equity.value};const r=await fetch('/evaluate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});out.textContent=JSON.stringify(await r.json(),null,2)}</script>
</body></html>"""


@app.post("/evaluate")
def evaluate(payload: dict):
    try:
        request = TradeRequest(**payload)
    except ValidationError as exc:
        return {"error": "Invalid trade request", "details": exc.errors()}
    result = evaluate_trade(request)
    return result.model_dump()
