from .common import simulate_failure

def issue_refund(order_id: str) -> str:
    simulate_failure()
    return f"Refund issued successfully for {order_id}"
