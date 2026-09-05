from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import ValidationError

from agent import analyze_trade
from market_data import fetch_market_snapshot
from models import TradeRequest

app = FastAPI(title="RiskPilot", version="1.0.0")


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """<!doctype html>
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>RiskPilot</title><style>
body{font-family:system-ui;background:#0b1020;color:#eef2ff;max-width:850px;margin:auto;padding:28px}
.card{background:#151c32;border:1px solid #2b3555;border-radius:18px;padding:24px;margin-top:18px}
input,select,button{width:100%;box-sizing:border-box;padding:12px;margin:7px 0;border-radius:10px;border:1px solid #394568;background:#0f162b;color:#fff;font-size:15px}
button{cursor:pointer;font-weight:700;background:#3157d5;border:0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
pre{white-space:pre-wrap;line-height:1.55}.tag{display:inline-block;padding:5px 10px;border-radius:999px;background:#263354}
small{color:#aeb9d6}@media(max-width:650px){.grid{grid-template-columns:1fr}}
</style></head><body>
<h1>🛡️ RiskPilot</h1><p>AI-powered safety layer for Binance Agent OS. Analyze before you trade.</p>
<div class='card'><form id='f'><div class='grid'>
<div><label>Symbol</label><input id='symbol' value='BTCUSDT'></div>
<div><label>Side</label><select id='side'><option>BUY</option><option>SELL</option></select></div>
<div><label>Position (USDT)</label><input id='notional' type='number' value='100'></div>
<div><label>Leverage</label><input id='leverage' type='number' value='2' step='0.1'></div>
<div><label>Stop loss (%)</label><input id='stop' type='number' value='2' step='0.1'></div>
<div><label>Account equity (USDT)</label><input id='equity' type='number' value='1000'></div>
</div><button>Analyze trade</button></form></div>
<div class='card'><div id='status'><span class='tag'>READY</span></div><pre id='out'>Enter a proposed trade and click Analyze trade.</pre></div>
<script>f.onsubmit=async(e)=>{e.preventDefault();out.textContent='Analyzing market + risk...';const body={symbol:symbol.value,side:side.value,notional_usdt:+notional.value,leverage:+leverage.value,stop_loss_pct:+stop.value,account_equity_usdt:+equity.value};try{const r=await fetch('/evaluate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const data=await r.json();status.innerHTML='<span class="tag">'+(data.action||'ERROR')+'</span>';out.textContent=data.explanation||JSON.stringify(data,null,2)}catch(err){status.innerHTML='<span class="tag">ERROR</span>';out.textContent=err.toString()}};</script>
</body></html>"""


@app.post("/evaluate")
def evaluate(payload: dict):
    try:
        request = TradeRequest(**payload)
    except ValidationError as exc:
        return {"error": "Invalid trade request", "details": exc.errors()}

    try:
        market = fetch_market_snapshot(request.symbol)
    except Exception as exc:
        market = None
        market_error = str(exc)
    else:
        market_error = None

    result = analyze_trade(request, market)
    response = result.model_dump()
    response["market_source"] = market.source if market else "Unavailable"
    if market_error:
        response["market_error"] = "Live demo market data could not be fetched."
    return response
"""