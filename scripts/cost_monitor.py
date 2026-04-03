#!/usr/bin/env python3
"""
BEN//OS COST GATEKEEPER - 3 Modi System
FREE ($0/Tag)   - System am Laufen halten
MIDDLE ($0.50/Tag max) - Normale Arbeit, Recherche, Code
BOOST ($2.00+/Call) - NUR mit Bens explizitem OK
"""
import json
import os
from datetime import datetime, timedelta

LOG_DIR = os.path.expanduser("~/benos/logs")
os.makedirs(LOG_DIR, exist_ok=True)

# ========================================
# 3 MODI DEFINITION
# ========================================
MODELS = {
    # --- FREE TIER ---
    "qwen-free": {"tier": "FREE", "in_price": 0.0, "out_price": 0.0, "desc": "OpenRouter Free"},
    # --- MIDDLE TIER ---
    "mimo-v2-flash": {"tier": "MIDDLE", "in_price": 0.10, "out_price": 0.30, "desc": "Xiaomi Flash"},
    "mimo-v2-omni": {"tier": "MIDDLE", "in_price": 0.40, "out_price": 2.00, "desc": "Xiaomi Omni (Multimodal)"},
    # --- BOOST TIER ---
    "mimo-v2-pro": {"tier": "BOOST", "in_price": 1.00, "out_price": 3.00, "desc": "Xiaomi Pro (1M Context)"},
    "claude-sonnet": {"tier": "BOOST", "in_price": 3.00, "out_price": 15.00, "desc": "Claude Sonnet"},
    "gpt-4o": {"tier": "BOOST", "in_price": 2.50, "out_price": 10.00, "desc": "GPT-4o"},
    "claude-opus": {"tier": "BOOST", "in_price": 5.00, "out_price": 25.00, "desc": "Claude Opus"},
}

# TAGESBUDGETS (USD)
BUDGETS = {
    "FREE": 0.0,
    "MIDDLE": 0.50,
    "BOOST": 999.0,  # Unbegrenzt, aber immer Ben-Check needed
}

def get_model_info(name):
    """Findet Modell-Info. Falls nicht gefunden -> UNKNOWN."""
    name_lower = name.lower()
    for key, info in MODELS.items():
        if key in name_lower:
            return {"name": key, **info}
    return {"name": name, "tier": "UNKNOWN", "in_price": 0.50, "out_price": 1.50, "desc": "Unbekannt"}

def estimate_cost(model_info, tokens_in, tokens_out):
    cost_in = tokens_in / 1_000_000 * model_info["in_price"]
    cost_out = tokens_out / 1_000_000 * model_info["out_price"]
    return round(cost_in + cost_out, 6)

def get_daily_usage():
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"api_calls_{today}.jsonl")
    if not os.path.exists(log_file):
        return {"FREE": 0.0, "MIDDLE": 0.0, "BOOST": 0.0}
    usage = {"FREE": 0.0, "MIDDLE": 0.0, "BOOST": 0.0}
    with open(log_file) as f:
        for line in f:
            try:
                entry = json.loads(line)
                tier = entry.get("tier", "UNKNOWN")
                if tier in usage:
                    usage[tier] += entry.get("cost", 0)
            except:
                pass
    return usage

def check_model(model_name, tokens_in=0, tokens_out=0, allow_boost=False):
    """
    Prueft ob ein Model-Call erlaubt ist.
    
    Rules:
    - FREE: Immer erlaubt
    - MIDDLE: Erlaubt bis Tagesbudget ($0.50)
    - BOOST: Nur mit allow_boost=True (Ben-OK)
    """
    info = get_model_info(model_name)
    cost = estimate_cost(info, tokens_in, tokens_out)
    usage = get_daily_usage()
    
    tier = info["tier"]
    result = {
        "model": info["name"],
        "tier": tier,
        "cost_estimate": cost,
        "daily_usage": usage,
        "daily_budget": BUDGETS.get(tier, 0),
        "budget_used_pct": round(usage.get(tier, 0) / BUDGETS.get(tier, 1) * 100, 1) if BUDGETS.get(tier, 1) > 0 else 0,
        "allowed": True,
        "warning": "",
        "desc": info["desc"],
    }
    
    # BOOST = immer Ben-Check
    if tier == "BOOST" and not allow_boost:
        result["allowed"] = False
        result["warning"] = f"BOOST MODE: {info['name']} ({info['desc']}) - ${cost:.4f}. Erfordert Bens OK!"
    
    # MIDDLE = Budget-Check
    elif tier == "MIDDLE":
        if usage["MIDDLE"] + cost > BUDGETS["MIDDLE"]:
            result["allowed"] = False
            result["warning"] = f"MIDDLE Budget ueberschritten: ${usage['MIDDLE']:.3f} + ${cost:.4f} > ${BUDGETS['MIDDLE']:.2f}. Schalte auf FREE um."
        else:
            remaining = BUDGETS["MIDDLE"] - usage["MIDDLE"] - cost
            result["budget_remaining"] = round(remaining, 4)
    
    elif tier == "UNKNOWN":
        result["warning"] = f"WARNING: Unbekanntes Model '{model_name}'. Bitte in MODELS-Liste pruefen."
    
    # Log Call (auch wenn blocked)
    log_entry = {
        "time": datetime.now().isoformat(),
        "model": info["name"],
        "tier": tier,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost": cost,
        "allowed": result["allowed"],
        "warning": result["warning"]
    }
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"api_calls_{today}.jsonl")
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return result

def daily_report():
    """Erzeugt taeglichen Kostenreport."""
    usage = get_daily_usage()
    total = sum(usage.values())
    report = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "usage": usage,
        "total_usd": round(total, 4),
        "status": "FREE" if total == 0 else "MIDDLE" if total < BUDGETS["MIDDLE"] else "BOOST",
        "budget_remaining_middle": round(BUDGETS["MIDDLE"] - usage["MIDDLE"], 4),
    }
    return report

# ========================================
# TEST / CLI
# ========================================
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        print(json.dumps(daily_report(), indent=2))
    elif len(sys.argv) > 1:
        model = sys.argv[1]
        tokens_in = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
        tokens_out = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
        boost = len(sys.argv) > 4 and sys.argv[4] == "boost"
        print(json.dumps(check_model(model, tokens_in, tokens_out, boost), indent=2))
    else:
        print("Cost Gatekeeper v2")
        print("Usage:")
        print("  python3 cost_monitor.py report")
        print("  python3 cost_monitor.py <model> <tokens_in> [tokens_out] [boost]")
        print()
        print("Verfuegbare Modelle:")
        for name, info in MODELS.items():
            print(f"  {name:20s} [{info['tier']:6s}] {info['desc']}")
