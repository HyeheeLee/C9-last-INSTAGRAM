from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
# from django.contrib.auth import login, logout as auth_login, auth_logout  # 덜 좋은 방법이지만, 이렇게도 사용가능하다!
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.
def signup(request):
    # 회원가입
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # save 함수의 return 값은 저장된 결과, user로 바로 사용할 수 있다.
            user = form.save()
            # 가입된 유저의 Profile 레코드 함께 생성
            # Profile.objects.create(user_id=user.id)   # 이렇게 해도 되지만,
            # ORM에게는 객체 자체를 넘겨주는게 더 낫기 때문에 아래와 같이 작성하자
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('posts:list')
        else:
            return redirect('accounts:signup')
    
    else:
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
        
        
def login(request):
    if request.method == "POST":
        # 실제 로그인(세션에 유저 정보를 넣는다.)
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # form으로부터 user 정보를 빼오고 싶다!
            auth_login(request, form.get_user())
            return redirect('posts:list')
        else:
            return redirect('accounts:login')
        
    else:
        # 유저로부터 username과 password를 받는다. 
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    
    
def profile(request, username):
    # username을 가진 유저의 상세 정보를 보여주는 페이지
    
    # profile = User.objects.get(username=username) 
    profile = get_object_or_404(get_user_model(), username=username)    # get_user_model()은 User와 같다.
    return render(request, 'accounts/profile.html', {'profile': profile})
    
    
def delete(request):
    # POST 계정을 삭제한다. == DB에서 user를 삭제한다.
    if request.method == "POST":
        request.user.delete()
        return redirect('posts:list')
    
    # GET > 진짜 삭제하시겠습니까?
    else:
        return render(request, 'accounts/delete.html')
        
        
@login_required
def follow(request, user_id):
    person = get_object_or_404(get_user_model(), pk=user_id)
    # 만약 이미 팔로우한 사람이라면
    if request.user in person.followers.all():
    # > 언팔
        person.followers.remove(request.user)
    # 아니면
    else:
    # > 팔로우
        person.followers.add(request.user)
        
    return redirect('profile', person.username)
    
    
@login_required
def change_profile(request):
    # 프로필 정보 수정
    if request.method == "POST":
        # ProfileForm(수정할 데이터, 수정 될 데이터)
        profile_form = ProfileForm(data=request.POST, instance=request.user.profile, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            
        return redirect('profile', request.user.username)
        
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'accounts/change_profile.html', {'profile_form': profile_form})
    