from .common import simulate_failure

def get_customer(customer_id: str) -> str:
    simulate_failure()
    if customer_id == "C001":
        return "Alice Smith - Premium Member"
    return "Customer not found."
