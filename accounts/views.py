from django.shortcuts import render

# 유저 목록이 출력되는 뷰
# + 기능 Follow라는 기능
# 중간 테이블을 직접 생성 - 모델

# 유저 모델을 커스터마이징 -> 1. 커스터마이징 하는 방법을 배워서
# 확장 하는 방법에 따라서
# 1) 새로운 유저 모델을 만드는 방법 - 기존 유저 데이터를 유지할 수가 없다.
# 2) 기존 모델을 확장 하는 방법 - DB 다운 타임 alter table - table lock
# 나 유저 모델
# 나를 팔로우한 사람 필드
# 내가 팔로우한 사람 필드

# 커스터마이징 할 수가 없다면?
# 새로운 모델을 추가하는 방법


# 사진 모델
# 사진을 좋아요한 사람 필드
# 사진을 저장한 사람 필드


"""
1. 유저 목록 혹은 유저 프로필에서 팔로우 버튼
1-1. 전체 유저 목록을 출력해주는 뷰 - User모델에 대한 ListView

2. 팔로우 정보를 저장하는 뷰
"""
from django.views.generic.list import ListView
from django.contrib.auth.models import User

class UserList(ListView):
    model = User
    template_name = 'accounts/user_list.html'

# 기존에 입력받는 뷰 CreateView 상속 받아서
# 커스텀이 힘들다
# 회원가입 -> User 모델에 갑을 입력받는다 -> CreateView
# 회원가입시 모델 필드 외에 추가 입력이 필요하다
# 커스템 하려면 함수형 뷰가 적절하다

from django.contrib.auth.models import User
from .forms import SignUpForm
def signup(request):
    # 함수형뷰는 request 필요
    # Class Based View 라면 -> dispatch에서 처리 -> get, post
    if request.method == "POST":
        # Todo : 입력받는 내용을 이용해서 회원 객체 생성
        # 입력받은 내용 확인

        # 모델 폼을 이용해서 간결하게 바꾼다
        # id, password 요건(길이가 짧은지, 특수문자가 들어가는지, 한글이 들어가는지)을 충족하는지 확인 하는 것 -> validation
        # forms.py에 생성
        signup_form = SignUpForm(request.POST) #request.POST 빈양식이 아닌 폼이 채워진 상태로 나온다
        # 모델폼은 알아서 인스턴스 객체를 만들어 준다
        if signup_form.is_valid():
            # 1. 저장하고 인스턴스 생성
            user_instance = signup_form.save(commit=False) #save()를 호출하면 인스턴스를 호출해서 생성 // form validation을 하지 않은 상태
            # 2. 패스워드 암호화 -> 저장(db hit가 두번!! -> commit=False -> 저장없이 인스턴스만 만듦)
            # 폼이 가지고 있는 cleaned data ?? : 유효한 문자만 남긴 상태로 처리 과정을 거친 데이터 --> db에 넣을 때는 항상 클린드 데이터
            # request.POST.get('password') <- 이러한 단계를 안거친 데이터
            user_instance.set_password(signup_form.cleaned_data['password'])
            user_instance.save()

            return render(request, 'accounts/signup_complete.html', {'username' : user_instance.username}) #회원가입이 정상처리 되었을 때만 띄우겠다

        '''
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        #print(username, password, password2)
        # 데이터 확인했으니
        # 회원 객체 생성하기 ->user 모델 import


        user = User()
        user.username = username
        #user.password = password
        # 암호화 필요
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        '''

        # render는 3가지 동작 처리
        # 1. 템플릿 불러오기
        # 2. 템플릿 렌더링 하기
        # 3. HTTP Response 하기
    else:
        # Todo : form 객체를 만들어서 전달
        # form에는 username, password만 입력 받으면 된다

        signup_form = SignUpForm()
        #context_value = {'form':signup_form}

        #return render(request, 'accounts/signup.html', context_value)
    return render(request, 'accounts/signup.html', {'form':signup_form}) #return을 앞으로 뺌으로써 윗단 else도 없애고 clean code를 만들 수 있다
