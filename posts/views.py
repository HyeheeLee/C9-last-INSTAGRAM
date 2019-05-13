from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostModelForm, CommentForm
from .models import Post, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create(request):
    # POST로 요청이 오면
    if request.method == 'POST':
        # 글 작성하기
        # input data가 모두 들어가있다.
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # save는 하고 db에 저장은 하지 마라
            post.user = request.user # 객체를 때려박아도 장고가 알아서 id 만 따와서 들어간다.
            post.save()
            return redirect('posts:list')
        else:
            return render(request, 'posts/create.html', form)
    # GET으로 요청이 오면
    else:
        # post를 작성하는 폼을 가져와 template에서 보여준다. 
        form = PostModelForm()
        context = {
            'form': form
        }
        return render(request, 'posts/create.html', context)    
        

@login_required
def list(request):
    # 모든 Post를 보여줌
    # posts = Post.objects.all()
    
    # 내가 팔로우한 사람들의 Post만 보여줌 
    # posts = []
    # for following in request.user.followings.all():
    #     posts.extend(Post.objects.filter(user=following))
    # posts.extend(Post.objects.filter(user=request.user.id))
    
    posts = Post.objects.filter(user__in=request.user.followings.values('id')).order_by('-pk')
    
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/list.html', context)
    
    
@login_required
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.user != request.user:
        return redirect('posts:list')

    post.delete()
    return redirect('posts:list')
    
    
@login_required
def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.user != request.user:
        return redirect('posts:list')
        
    if request.method == "POST":
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid:
            form.save()
        return redirect('posts:list')
    
    else:
        # 수정내용 편집 페이지로 가기
        form = PostModelForm(instance=post)
        context = {
            'form': form,
        }
        return render(request, 'posts/update.html', context) 
        
        
@login_required
def create_comments(request, post_id):
    comment_form = CommentForm(request.POST)
    
    if comment_form.is_valid:
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
                        
        return redirect('posts:list')
        
   
@login_required     
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # 특정 유저가 특정 포스트를 좋아요 할 때,
    # 만약 '좋아요'가 되어 있다면
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    # -> '좋아요'를 해제한다. 
    # 아니면
    else:
        post.like_users.add(request.user)
    # -> '좋아요'를 한다.
    
    return redirect('posts:list')