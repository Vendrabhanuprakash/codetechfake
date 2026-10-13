from django.db import models

# Create your models here.

import uuid
from django.db import models


class StudentCertificate(models.Model):
    certificate_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    student_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=150)
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.student_name} - {self.course_name}"
