import json

from .llm import chat
from .tools import (
    create_customer,
    get_customer,
    search_customers,
    create_lead,
    update_lead_status,
    create_followup,
    get_pending_followups,
)


TOOLS = {
    "create_customer": create_customer,
    "get_customer": get_customer,
    "search_customers": search_customers,
    "create_lead": create_lead,
    "update_lead_status": update_lead_status,
    "create_followup": create_followup,
    "get_pending_followups": get_pending_followups,
}


SYSTEM_PROMPT = """
You are an AI CRM assistant.

You can perform real actions in the CRM database.

Available tools:

1. create_customer
   arguments:
   {
       "name": string,
       "phone": string,
       "email": string,
       "company": string
   }

2. get_customer
   arguments:
   {
       "customer_id": integer
   }

3. search_customers
   arguments:
   {
       "query": string
   }

4. create_lead
   arguments:
   {
       "customer_id": integer,
       "title": string,
       "description": string,
       "value": number
   }

5. update_lead_status
   arguments:
   {
       "lead_id": integer,
       "status": "new" | "contacted" | "qualified" | "won" | "lost"
   }

6. create_followup
   arguments:
   {
       "customer_id": integer,
       "note": string,
       "due_date": string,
       "lead_id": integer | null
   }

7. get_pending_followups
   arguments:
   {}

IMPORTANT:

If the user asks you to perform an action, return ONLY valid JSON.

For a tool call use:

{
    "action": "tool_name",
    "arguments": {
        ...
    }
}

If no tool is required, use:

{
    "action": "none",
    "answer": "your answer"
}

Do not use markdown.
Do not add explanations outside JSON.
"""


def run_agent(user_message):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    raw_response = chat(
        messages,
        temperature=0,
        json_mode=True,
    )

    try:
        decision = json.loads(raw_response)
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "AI returned invalid JSON.",
            "raw_response": raw_response,
        }

    action = decision.get("action")

    if action == "none":
        return {
            "success": True,
            "answer": decision.get(
                "answer",
                ""
            ),
        }

    if action not in TOOLS:
        return {
            "success": False,
            "error": f"Unknown tool: {action}",
        }

    arguments = decision.get(
        "arguments",
        {}
    )

    try:

        result = TOOLS[action](**arguments)

    except Exception as exc:

        return {
            "success": False,
            "error": str(exc),
            "tool": action,
        }

    return {
        "success": True,
        "tool": action,
        "result": result,
    }