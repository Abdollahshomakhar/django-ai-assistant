from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CustomerViewSet,
    LeadViewSet,
    FollowUpViewSet,
    ai_chat,
)


router = DefaultRouter()

router.register(
    "customers",
    CustomerViewSet,
    basename="customer"
)

router.register(
    "leads",
    LeadViewSet,
    basename="lead"
)

router.register(
    "followups",
    FollowUpViewSet,
    basename="followup"
)


urlpatterns = [
    path("ai/chat/", ai_chat),
]

urlpatterns += router.urls