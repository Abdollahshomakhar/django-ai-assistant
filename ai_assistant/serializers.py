from rest_framework import serializers

from .models import (
    Customer,
    Lead,
    FollowUp,
)


class CustomerSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Customer
        fields = "__all__"


class LeadSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Lead
        fields = "__all__"


class FollowUpSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = FollowUp
        fields = "__all__"
# class ChatSerializer(serializers.Serializer):
#     message = serializers.CharField(
#         required=True,
#         allow_blank=False
#     )
class ChatSerializer(serializers.Serializer):
    message = serializers.CharField(
        required=True,
        allow_blank=False
    )
