from django.contrib import admin

from .models import Customer, Lead, FollowUp


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "email",
        "company",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "company",
    )

    ordering = ("-created_at",)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "customer",
        "status",
        "value",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "customer__name",
        "customer__email",
    )

    ordering = ("-created_at",)


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "lead",
        "note",
        "due_date",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "due_date",
    )

    search_fields = (
        "note",
        "customer__name",
        "customer__email",
        "lead__title",
    )

    ordering = ("due_date",)    