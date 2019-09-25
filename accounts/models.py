from django.db import models

# Create your models here.
# 중간 모델 작성
from django.contrib.auth.models import User

class Follow(models.Model):
    # 2개 필드 - ForeignKey
    # A가 B를 팔로우 하고 있다.
    # on_delete 연관된 객체가 삭제된다면 어떻게 할것이냐?
    # related_name은 참조 객체의 입장에서 필드명, 속성값

    me = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    you = models.ForeignKey(User, on_delete=models.CASCADE,related_name='follower')

    def __str__(self):
        return self.me.username+" follow "+self.you.username