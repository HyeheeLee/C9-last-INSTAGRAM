from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    content = forms.CharField(
        label="content", 
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 50,
            'placeholder': '지금 뭘 하고 계신가요?',
        }))
    
    class Meta:
        model = Post
        # created_at, updated_at의 경우 따로 사용자에게 input 만들어줄 필요없다. 아래와 같이 하지말자!
        # fields = '__all__'
        # input을 만들 칼럼 값을 list로 만들어 넣어줌.
        fields = ['content', 'image']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']