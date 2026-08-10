from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "payment_number",
        "invoice_number",
        "receipt_number",
        "member",
        "membership",
        "amount",
        "discount",
        "tax",
        "final_amount",
        "payment_method",
        "payment_status",
        "organization",
        "branch",
        "payment_date",
    )

    list_filter = (
        "organization",
        "branch",
        "payment_method",
        "payment_status",
        "payment_date",
    )

    search_fields = (
        "payment_number",
        "invoice_number",
        "receipt_number",
        "transaction_id",
        "member__first_name",
        "member__last_name",
        "member__phone",
    )

    readonly_fields = (
        "payment_number",
        "invoice_number",
        "receipt_number",
        "final_amount",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-payment_date",
        "-id",
    )

    list_per_page = 25

    autocomplete_fields = (
        "member",
        "membership",
        "organization",
        "branch",
        "collected_by",
    )

    fieldsets = (
        (
            "Payment Identification",
            {
                "fields": (
                    "payment_number",
                    "invoice_number",
                    "receipt_number",
                )
            },
        ),
        (
            "Customer & Membership",
            {
                "fields": (
                    "member",
                    "membership",
                )
            },
        ),
        (
            "Organization",
            {
                "fields": (
                    "organization",
                    "branch",
                    "collected_by",
                )
            },
        ),
        (
            "Financial Details",
            {
                "fields": (
                    "amount",
                    "discount",
                    "tax",
                    "final_amount",
                )
            },
        ),
        (
            "Payment Details",
            {
                "fields": (
                    "payment_method",
                    "payment_status",
                    "payment_date",
                    "transaction_id",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "notes",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )