from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "branch",
        "attendance_date",
        "check_in",
        "check_out",
        "status",
        "checkin_method",
    )

    list_filter = (
        "status",
        "branch",
        "attendance_date",
        "checkin_method",
    )

    search_fields = (
        "member__first_name",
        "member__last_name",
        "member__phone",
    )

    date_hierarchy = "attendance_date"

    ordering = ("-attendance_date", "-check_in")