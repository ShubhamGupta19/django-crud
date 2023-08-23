from datetime import date, datetime
from enum import unique
import os
from platform import platform
import random
import string

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from  django.core.validators import validate_email
from config.request_param_validators import get_request_body
from error_handling.custom_exceptions.common_exceptions import RequestBodyValidation
from error_handling.custom_exceptions.notes_exceptions import NotesDoesNotExist

from config.custom_decorators.login_required import login_required

from users.models import  UserProfile


from django.db.models import F

from notes.models import Notes


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def create_notes(request):
    request_body = get_request_body(request)
    
    Notes.objects.create(
        user=request.user_profile,
        title=request_body.get("title"),
        description=request_body.get("description"),
    )

    return JsonResponse({"success": True})

@csrf_exempt
@login_required
@require_http_methods(["GET"])
def get_all_notes(request):
    request_body = get_request_body(request)
    
    notes = Notes.objects.filter(user=request.user_profile)
    
    return JsonResponse(
        {
            "notes": [note.to_dict(summary_only=True) for note in notes],
        }
    )
    
    
@csrf_exempt
@login_required
@require_http_methods(["GET"])
def get_notes(request, note_id):
    request_body = get_request_body(request)
    
    try:
        note = Notes.objects.get(id=note_id, user=request.user_profile)
    except Notes.DoesNotExist:
        raise NotesDoesNotExist

    return JsonResponse(
        note.to_dict()
    )

@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def update_notes(request, note_id):
    request_body = get_request_body(request)
    
    try:
        note = Notes.objects.get(id=note_id, user=request.user_profile)
    except Notes.DoesNotExist:
        raise NotesDoesNotExist
    
    note.title = request_body.get("title") or note.title
    note.description = request_body.get("description") or note.description
    note.save()

    return JsonResponse({"success": True})

@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def delete_notes(request, note_id):
    request_body = get_request_body(request)
    
    try:
        note = Notes.objects.get(id=note_id, user=request.user_profile)
    except Notes.DoesNotExist:
        raise NotesDoesNotExist
    
    note.delete()

    return JsonResponse({"success": True})