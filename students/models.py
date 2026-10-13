import secrets
from django.db import models

def generate_certificate_id():
    return secrets.token_hex(8).upper()


class StudentCertificate(models.Model):
    certificate_id = models.CharField(
        max_length=16,
        unique=True,
        default=generate_certificate_id,
        editable=False
    )

    student_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=150)
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_name} - {self.course_name}"