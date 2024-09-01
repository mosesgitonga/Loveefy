from django.http import JsonResponse

def moses(request):
    return JsonResponse({"message": "Hello, Moses!"})