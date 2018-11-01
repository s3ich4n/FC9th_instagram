import imghdr

import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class FacebookBackend:
    def authenticate(self, request, facebook_request_token):
        api_base = 'https://graph.facebook.com/v3.2/'
        api_get_access_token = f'{api_base}/oauth/access_token'
        api_me = f'{api_base}/me'

        # request token 저장
        code = facebook_request_token

        # request token을 access token으로 교환
        params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': 'http://localhost:8000/members/facebook-login/',
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': code,
        }
        response = requests.get(api_get_access_token, params)
        # 전달한 문자열을 json으로 생각
        # json.loads는 전달한게 json이면 문자열 파싱 후 python object 리턴
        # response_object = json.loads(response.text)
        data = response.json()
        access_token = data['access_token']

        # access token으로 사용자 정보 가져오기.
        params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'first_name'
                'last_name',
                'picture.type(large)',
            ]),
        }
        response = requests.get(api_me, params)
        data = response.json()

        facebook_id = data['id']
        first_name = data['first_name']
        last_name = data['last_name']
        url_img_profile = data['picture']['data']['url']
        # get 요청의 응답으로 바이너리 데이터를 img_data에 할당.
        img_response = requests.get(url_img_profile)
        img_data = img_response.content

        ext = imghdr.what('', h=img_data)

        f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.content)

        try:
            user = User.objects.get(username=facebook_id)
            user.last_name = last_name
            user.first_name = first_name
            # user.img_profile = f
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=facebook_id,
                first_name=first_name,
                last_name=last_name,
                img_profile=f,
            )
        return user