from django import forms

from .models import Post


class UploadFileForm(forms.Form):
    '''
    부트스트랩 의존적임!
    '''
    image_file = forms.ImageField(
        # 파일입력 위젯 사용
        widget=forms.FileInput(
            # html 위젯 설정
            # form-control-file 클래스 사용
            attrs={
                'class': 'form-control-file',
            }
        )
    )
    comment = forms.CharField(
        required=False,
        # html 렌더링 위젯으로 textarea 사용
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def save(self, **kwargs):
        post = Post.objects.create(
            photo=self.cleaned_data['photo'],
            **kwargs,
        )
        return post
