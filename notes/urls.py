from . import views
from django.urls import path

urlpatterns=[
    path("upload/", views.upload_note),
    path("notes/", views.list_notes),
    path("chatbot/", views.chatbot),
    path("view/<int:note_id>/", views.view_note_content, name='view_note_content'),  # Assuming you have a view_note function to handle this
]

