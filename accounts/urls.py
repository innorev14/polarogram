from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import UserList, signup

app_name = 'accounts'

urlpatterns = [
    path('user/list/', UserList.as_view(), name='user_list'),
    path('signin/', LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('signout/', LogoutView.as_view(template_name='accounts/signout.html'), name='signout'),
    # 함수형뷰는 이름만 씀
    path('signup/', signup, name='signup'),
]