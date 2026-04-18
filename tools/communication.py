from .common import simulate_failure

def send_reply(message: str) -> str:
    simulate_failure()
    return f"Message sent to customer: {message}"

def escalate_ticket(reason: str) -> str:
    simulate_failure()
    return f"Ticket Escalated to Human. Reason: {reason}"
