import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

from .models import Note
from .chatbot import ask_groq


# -------------------------------
# 1. Teacher Upload Notes
# -------------------------------
@csrf_exempt
def upload_note(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        unit = request.POST.get("unit")
        title = request.POST.get("title")
        file = request.FILES.get("file")

        if not (subject and unit and title and file):
            return JsonResponse({"error": "All fields are required"}, status=400)

        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        note = Note(subject=subject, unit=unit, title=title, file=filename)
        note.save()
        print(f"Note uploaded: {note}")

        return JsonResponse({"message": "Note uploaded successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=405)


# -------------------------------
# 2. List Notes for Students
# -------------------------------
def list_notes(request):
    notes = list(Note.objects.values("id", "subject", "unit", "title", "file", "uploaded_at"))
    return JsonResponse(notes, safe=False)


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
        

from django.db import connection
from django.http import JsonResponse

def view_note_content(request, note_id):
    print('helloworld')
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT file FROM notes_note WHERE id = %s", [note_id])
            row = cursor.fetchone()
            if not row:
                return JsonResponse({'error': 'Note not found'}, status=404)
            print(note_id)
            file_path = row[0]  # This is the relative path stored in DB
            print(f"Retrieved file path:")
            print(f"File path from DB: {file_path}")
            full_path = f"media/{file_path}"  # Adjust if your media root is different

            with open(full_path, 'r') as f:
                content = f.read()

        return JsonResponse({'content': content})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
