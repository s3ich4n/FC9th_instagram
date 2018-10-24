from django.shortcuts import redirect


def index(request):
    return redirect('posts:post_list')

# import os
#
# from django.conf import settings
# from django.http import HttpResponse
#
#
# def media_serve(request, path):
#     '''
#     1. /media/로 시작하는 모든 URL은 해당 views를 통해 처리됨.
#     2. /media/<경로>/ 에서,
#         <경로> 부분은 path 변수에 할당.
#     3. settings.py에 있는 MEDIA_ROOT를 기준으로...
#         <경로> 에 해당하는 파일의 경로를 file_path변수에 할당
#             MEDIA_ROOT 가져오는 법:
#                 django.conf import settings
#                 settings.MEDIA_ROOT
#     4. file_path를 open한 '파일 객체'를 HttpResponse에 담아서 리턴.
#     :param:
#     :return:
#     '''
#
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#
#     with open(file_path, 'w') as f:
#         return HttpResponse(f, content_type="image/jpeg")
