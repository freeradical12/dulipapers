from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api_endpoint(request):
    return JsonResponse({'message': 'API endpoint working'})


def download_data(request):
    # 直接提供下载
    file_path = '/path/to/data.zip'
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="free_data.zip"'
    return response