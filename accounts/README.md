# Auth
            
- 회원가입: UserCreationForm(인자)
- 로그인: AuthenticationForm(인자)
- 로그아웃: X
- 회원정보수정:
- 비밀번호 변경:
- 회원탈퇴:  
---
                            
# User 모델을 가져오는 방법
1. from django.contrib.auth.models import User
    - AbstractBaseUser > AbstractUser > User
    지금은 user를 쓰고 있지만, 나중에 CustomUser라고 쓸건데
    이 방법으로 한다면 전부 다 바꿔줘야 한다. 
    name = "john" > "tom"으로 바꾸면 모든 코드에 찾아가서 "tom"으로 바꿔야 한다.
2. from django.conf import settings > settings.AUTH_USER_MODEL (단순 스트링)
    주로 사용하는 모델을 지정해서 그 모델만 바꿔주면 된다.
    변수 활용하듯
3. form django.contrib.auth import get_user_model (요놈 쓰자)
                                
## User 모델 사용하기
1. models.py
    -> settings.AUTH_USER_MODEL
2. 나머지
    -> get_user_model
---
                
# accounts.User
- user를 새로 설정하면 db 지우고 accounts/migragions 안에 있는 파일 날린다.(init 제외)
    -> migration