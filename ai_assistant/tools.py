from django.utils import timezone

from .models import (
    Customer,
    Lead,
    FollowUp,
)


def create_customer(
    name,
    phone="",
    email="",
    company=""
):

    customer = Customer.objects.create(
        name=name,
        phone=phone,
        email=email,
        company=company,
    )

    return {
        "success": True,
        "customer_id": customer.id,
        "name": customer.name,
    }


def get_customer(customer_id):

    try:

        customer = Customer.objects.get(
            id=customer_id
        )

    except Customer.DoesNotExist:

        return {
            "success": False,
            "error": "Customer not found."
        }

    return {
        "success": True,
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "email": customer.email,
            "company": customer.company,
        }
    }


def search_customers(query):

    customers = Customer.objects.filter(
        name__icontains=query
    )[:20]

    return {
        "success": True,
        "customers": [
            {
                "id": customer.id,
                "name": customer.name,
                "phone": customer.phone,
                "email": customer.email,
                "company": customer.company,
            }
            for customer in customers
        ]
    }


def create_lead(
    customer_id,
    title,
    description="",
    value=0
):

    try:

        customer = Customer.objects.get(
            id=customer_id
        )

    except Customer.DoesNotExist:

        return {
            "success": False,
            "error": "Customer not found."
        }

    lead = Lead.objects.create(
        customer=customer,
        title=title,
        description=description,
        value=value,
    )

    return {
        "success": True,
        "lead_id": lead.id,
        "title": lead.title,
    }


def update_lead_status(
    lead_id,
    status
):

    try:

        lead = Lead.objects.get(
            id=lead_id
        )

    except Lead.DoesNotExist:

        return {
            "success": False,
            "error": "Lead not found."
        }

    valid_statuses = {
        choice[0]
        for choice in Lead.Status.choices
    }

    if status not in valid_statuses:

        return {
            "success": False,
            "error": "Invalid lead status."
        }

    lead.status = status
    lead.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )

    return {
        "success": True,
        "lead_id": lead.id,
        "status": lead.status,
    }


def create_followup(
    customer_id,
    note,
    due_date,
    lead_id=None
):

    try:

        customer = Customer.objects.get(
            id=customer_id
        )

    except Customer.DoesNotExist:

        return {
            "success": False,
            "error": "Customer not found."
        }

    lead = None

    if lead_id:

        try:

            lead = Lead.objects.get(
                id=lead_id
            )

        except Lead.DoesNotExist:

            return {
                "success": False,
                "error": "Lead not found."
            }

    followup = FollowUp.objects.create(
        customer=customer,
        lead=lead,
        note=note,
        due_date=due_date,
    )

    return {
        "success": True,
        "followup_id": followup.id,
        "note": followup.note,
        "due_date": followup.due_date,
    }


def get_pending_followups():

    followups = FollowUp.objects.filter(
        status=FollowUp.Status.PENDING,
        due_date__lte=timezone.now()
    ).select_related(
        "customer",
        "lead"
    )

    return {
        "success": True,
        "followups": [
            {
                "id": item.id,
                "customer": item.customer.name,
                "lead": item.lead.title
                if item.lead else None,
                "note": item.note,
                "due_date": item.due_date,
            }
            for item in followups
        ]
    }