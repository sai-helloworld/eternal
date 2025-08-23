from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path("chatbot/", views.chatbot),
    # path("view/<int:note_id>/", views.view_note_content, name='view_note_content'),  # Assuming you have a view_note function to handle this
     path('upload/<int:class_id>/<str:subject>/', views.upload_notes, name='upload_notes'),
    path('api/notes/', views.get_notes_by_class_and_subject, name='get_notes_by_class_and_subject'),
    path('download/<int:note_id>/', views.download_note, name='download_note'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)