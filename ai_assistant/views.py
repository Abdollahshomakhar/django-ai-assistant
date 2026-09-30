from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .agent import run_agent
from .models import (
    Customer,
    Lead,
    FollowUp,
)

from .serializers import (
    CustomerSerializer,
    LeadSerializer,
    FollowUpSerializer,
    ChatSerializer,
)

from .llm import chat


class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all().order_by("-created_at")

    serializer_class = CustomerSerializer


class LeadViewSet(viewsets.ModelViewSet):

    queryset = Lead.objects.select_related(
        "customer"
    ).all().order_by("-created_at")

    serializer_class = LeadSerializer


class FollowUpViewSet(viewsets.ModelViewSet):

    queryset = FollowUp.objects.select_related(
        "customer",
        "lead"
    ).all().order_by("-due_date")

    serializer_class = FollowUpSerializer


@api_view(["GET", "POST"])
def ai_chat(request):

    if request.method == "GET":
        return Response({
            "message": "AI Chat API is running.",
            "method": "POST",
            "example": {
                "message": "یک مشتری به نام علی رضایی ایجاد کن"
            }
        })

    serializer = ChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    message = serializer.validated_data["message"]

    try:

        result = run_agent(message)

        return Response({
            "success": True,
            "message": message,
            "result": result,
        })

    except Exception as exc:

        return Response({
            "success": False,
            "error": str(exc),
        }, status=500)  