# 모델폼을 만들려면 2가지가 필요하다
# generic view를 만들려면 제네릭 뷰 필요 -> 모델 필요
# 모델폼 : 모델, 폼 필요

from django.contrib.auth.models import User
from django import forms
# from django.forms import ModelForm
# 이렇게 쓰지 않는건 model.xxx로 반복되기 때문
class SignUpForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)


    class Meta:
        model = User
        # field에는 해당 모델에 대해 입력받을 필드들을 나열한다
        # + 추가 필드도 포함될 수 있다. -> 필드 목록과 추가 필드가 겹치면 오버라이드
        # fields 에 써진 순서대로 출력한다
        fields = ['username', 'password', 'password2', 'first_name', 'last_name', 'email']
        #fields = '__all__' <- 전체를 다 부르고 싶을 때

        # 폼 객체만들어서 context value로 전달

        # Todo : 필드의 기본값(initial value), placeholder 설정법, css Class 설정법, validator 설정법, help text 설정법
        # Todo : 커스텀 필드 만드는 법

    # password, password2 일치 확인 -> view에서 처리할 수 있으나!! form에서!!
    #def clean_필드명(self):
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        # 항상 해당 필드의 값 리턴한다
        return cd['password2']