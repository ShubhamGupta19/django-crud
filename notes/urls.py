from django.urls import path
from .apis.notes import (
    create_notes,
    get_all_notes,
    get_notes,
    update_notes,
    delete_notes
)

urlpatterns = [
    path("create/", create_notes),
    path("get-all/", get_all_notes),
    path("get/<int:note_id>/", get_notes),
    path("update/<int:note_id>/", update_notes),
    path("delete/<int:note_id>/", delete_notes),
]