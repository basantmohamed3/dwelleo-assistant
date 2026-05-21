import uuid


def create_support_ticket(issue: str):
    ticket_id = f"DW-{str(uuid.uuid4())[:8]}"

    return {
        "ticket_id": ticket_id,
        "status": "created",
        "issue": issue,
        "priority": "medium"
    }