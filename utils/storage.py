import os, json, pathlib, threading

# Use static/data directory by default, or environment variable if set
DATA_DIR = pathlib.Path(os.getenv("DATA_DIR", "static/data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

ORDERS_FILE = DATA_DIR / "orders.json"
_lock = threading.Lock()

def _read_all():
    if ORDERS_FILE.exists():
        try:
            return json.loads(ORDERS_FILE.read_text('utf-8'))
        except Exception:
            return []
    return []

def save_order(order: dict):
    with _lock:
        data = _read_all()
        data.append(order)
        ORDERS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), 'utf-8')

def list_orders():
    return _read_all()
