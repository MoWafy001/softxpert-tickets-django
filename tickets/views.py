from django.http import JsonResponse

def handler404(request, exception):
    return JsonResponse({"error": "Not Found", "message": "The requested resource was not found."}, status=404)

def handle500(request):
    return JsonResponse({"error": "Server Error", "message": "An internal server error occurred."}, status=500)
