from .common import simulate_failure

ORDERS = {
    "123": {"status": "delivered", "amount": 50.0},
    "124": {"status": "processing", "amount": 100.0},
}

def get_order(order_id: str) -> str:
    simulate_failure()
    order = ORDERS.get(order_id)
    if order:
        return f"Order exists: {order}"
    return "Order not found."
