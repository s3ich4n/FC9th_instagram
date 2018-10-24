from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 이 인스턴스에 주어진 데이터가 유효하면
        # authenticate에서 리턴된 User 객체를 채움
        self._user = None

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def clean(self):
        super().clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(
            username=username,
            password=password,
        )
        if user is None:
            raise forms.ValidationError(
                '사용자명 또는 비밀번호가 올바르지 않습니다.'
            )
        self._user = user

    @property
    def user(self):
        # 유효성 검증을 실행했을 때
        # 필드나 폼에서 유효하지 않은 항목이 있으면 이 부분에 추가됨.
        if self.errors:
            raise ValueError('폼의 데이터 유효성 검증에 실패하였습니다.')
        return self._user


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='사용자명',
        widget=forms.TextInput(
            # html 위젯 속성
            # see also: http://getbootstrap.com/docs/4.1/components/forms/#overview
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password_confirm = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    # clean_<fildname>() 형태의 메소드
    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            self.fields['username'].widget.attrs['class'] += 'is-invalid'
            raise forms.ValidationError('이미 사용중인 사용자명 입니다.')

        return data

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            self.fields['password'].widget.attrs['class'] += ' is-invalid'
            self.fields['password_confirm'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError('비밀번호 값이 서로 일치하지 않습니다.')

        return password_confirm

    def save(self):
        if self.errors:
            raise ValueError('폼의 데이터 유효성 검증에 실패했습니다.')
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )
        return user
