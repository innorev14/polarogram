from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_delete
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, View

from .models import Post

# 뷰 실행전에 로그인여부, csrf 체크
class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/post_list.html'

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'text']
    template_name = 'post/post_create.html'
    success_url = '/'

    def form_valid(self, form):
        # 입력된 항목이 올바른지 체
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({
                'form': form
            })

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['image', 'text']
    template_name = 'post/post_update.html'

    # method에 따라 GET/POST 분기
    def dispatch(self, request, *arg, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "수정할 권한이 없습니다")
            return HttpResponseRedirect(object.get_absolute_url())

        return super(PostUpdate, self).dispatch(request, *arg, **kwargs)

class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    templat_name = 'post/post_detail.html'

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(requst, "삭제할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PostDelete, self).dispatch(request, *args, **kwargs)



class PostLikedList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/post_list.html'

    def get_queryset(self):
        # 로그인한 유저가 좋아요를 클릭한 글을 찾아서 반환
        user = self.request.user
        queryset = user.liked_post.all()
        return queryset

class PostSavedList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/post_list.html'

    def get_queryset(self):
        # 로그인한 유저가 저장한 글을 찾아서 반환
        user = self.request.user
        queryset = user.saved_post.all()
        return queryset

class PostLiked(View):
    def get(self, request, *args, **kwargs):
        # liked를 할 정보가 있다면 진행, 없다면 중
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            # 1. 어떤 포스팅?
            # url : www.naver.com/blog/like/?photo_id=1
            # request.GET.get('photo_id')
            # url : www.naver.com/blog/like/1/
            # path('blog/like/<int:photo_id>/')
            # kwargs['photo_id']
            # 2. 누가?
            if 'post_id; in kwargs':
                post = kwargs['post_id']
                user = request.user
                if user in post.liked.all():
                    post.liked.remove(user)
                else:
                    post.liked.add(user)

            # 레퍼러 얻기
            referer_url = request.META.get('HTTP_REFERER')
            # https://www.naver.com
            # /blog/doc/1234/
            # ?id=2223
            # domain, path, query
            # path
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

class PostSaved(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'post_id' in kwargs:
                post_id = kwargs['post_id']
                post = Post.objects.get(pk=post_id)
                user = request.user
                if user in post.liked.all():
                    post.liked.remove(user)
                else:
                    post.liked.add(user)
            return HttpResponseRedirect('/')

# signal
# 동작을 하기 전이나 후에 신호를 보냄
# 오버라이드도 할 수 있지만 signal은 한번에 처리하게 할 수 있다
# 1. 어떤 시그널이 발생했을 때 반응할 것이냐?
# 2. 그 시그널이 발생 했을 때 어떻게 알것인가?
@receiver(post_delete, sender=Post)
def post_delete(sender, instance, **kwargs):
    storage = instance.image.storage
    if storage.exists(str(instance.image)):
        storage.delete(str(instance.image))










