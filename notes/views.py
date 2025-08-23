import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

from .chatbot import ask_groq


# -------------------------------
# 1. Teacher Upload Notes
# -------------------------------
# @csrf_exempt
# def upload_note(request):
#     if request.method == "POST":
#         subject = request.POST.get("subject")
#         unit = request.POST.get("unit")
#         title = request.POST.get("title")
#         file = request.FILES.get("file")

#         if not (subject and unit and title and file):
#             return JsonResponse({"error": "All fields are required"}, status=400)

#         fs = FileSystemStorage()
#         filename = fs.save(file.name, file)

#         note = Note(subject=subject, unit=unit, title=title, file=filename)
#         note.save()
#         print(f"Note uploaded: {note}")

#         return JsonResponse({"message": "Note uploaded successfully!"})

#     return JsonResponse({"error": "Invalid request"}, status=405)



# -------------------------------
# 3. Chatbot with Groq
# -------------------------------
# notes/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .chatbot import ask_groq

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def chatbot(request):
    if request.method == "OPTIONS":
        # Handle CORS preflight
        response = JsonResponse({"status": "ok"})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            query = data.get("query", "")
            if not query:
                return JsonResponse({"error": "Query is required"}, status=400)
            
            answer = ask_groq(query)
            return JsonResponse({"answer": answer})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        





from django.shortcuts import render
from django.http import JsonResponse
from .models import ClassNote
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_notes(request, class_id, subject):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            ClassNote.objects.create(
                class_id=class_id,
                subject_name=subject,
                pdf_file=pdf_file
            )
            return JsonResponse({'status': 'success', 'message': 'Notes uploaded successfully'})
        return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)
    
    return render(request, 'upload_notes.html', {'class_id': class_id, 'subject': subject})




from django.http import JsonResponse, FileResponse
from .models import ClassNote  # Replace with your actual model name

def get_notes_by_class_and_subject(request):
    class_name = request.GET.get('className')
    subject_name = request.GET.get('subjectName')

    if not class_name or not subject_name:
        return JsonResponse({'error': 'Missing className or subjectName'}, status=400)

    notes = ClassNote.objects.filter(class_id__iexact=class_name, subject_name__iexact=subject_name)

    data = [
        {
            'id': note.id,
            'filename': note.pdf_file.name.split('/')[-1],
            'uploaded_at': note.uploaded_at.strftime('%Y-%m-%d %H:%M'),
        }
        for note in notes
    ]

    return JsonResponse(data, safe=False)


def download_note(request, note_id):
    try:
        note = ClassNote.objects.get(id=note_id)
        return FileResponse(note.pdf_file.open(), as_attachment=True, filename=note.pdf_file.name)
    except ClassNote.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)
