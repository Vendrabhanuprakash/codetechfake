from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentCertificate


@admin.register(StudentCertificate)
class StudentCertificateAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "course_name",
        "start_date",
        "certificate_id",
        "is_verified",
    )

    list_filter = ("is_verified", "start_date")
    search_fields = ("student_name", "course_name", "certificate_id")
    list_editable = ("is_verified",)