from django.http import HttpResponse, JsonResponse


def moses(request):
    return JsonResponse({"message": "Hello, Moses!"})