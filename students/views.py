import json
from datetime import date

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from .models import StudentCertificate


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

        # Validate required fields
        if not name or not course or not start_date:
            return JsonResponse(
                {"error": "All fields are required."},
                status=400
            )

        # Validate field lengths
        if len(name) > 100 or len(course) > 150:
            return JsonResponse(
                {"error": "Name or course is too long."},
                status=400
            )

        # Validate date format
        parsed_date = date.fromisoformat(start_date)

        # Save the student record in the database
        student = StudentCertificate.objects.create(
            student_name=name,
            course_name=course,
            start_date=parsed_date
        )

        # Return the certificate ID and verification URL
        verification_url = request.build_absolute_uri(
            reverse(
                "verify_certificate",
                args=[student.certificate_id]
            )
        )

        return JsonResponse(
            {
                "id": str(student.certificate_id),
                "verification_url": verification_url
            },
            status=201
        )

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
