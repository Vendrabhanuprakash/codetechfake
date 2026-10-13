from django.shortcuts import render

# Create your views here.

import json
import uuid
from datetime import date

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .models import StudentCertificate

from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render

@ensure_csrf_cookie
def index(request):
    return render(request, "students/index.html")

@require_POST
@csrf_protect
def create_certificate(request):
    try:
        data = json.loads(request.body)

        name = data.get("name", "").strip()
        course = data.get("course", "").strip()
        start_date = data.get("startDate", "")

        if not name or not course or not start_date:
            return JsonResponse(
                {"error": "All fields are required."},
                status=400
            )

        if len(name) > 100 or len(course) > 150:
            return JsonResponse(
                {"error": "Name or course is too long."},
                status=400
            )

        parsed_date = date.fromisoformat(start_date)

        student = StudentCertificate.objects.create(
            student_name=name,
            course_name=course,
            start_date=parsed_date
        )

        return JsonResponse({
            "id": str(student.certificate_id),
            "verification_url": request.build_absolute_uri(
                f"/verify/{student.certificate_id}/"
            )
        }, status=201)

    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse(
            {"error": "Please enter valid student details."},
            status=400
        )


def verify_certificate(request, certificate_id):
    student = get_object_or_404(
        StudentCertificate,
        certificate_id=certificate_id
    )

    return render(
        request,
        "students/verify.html",
        {"student": student}
    )
