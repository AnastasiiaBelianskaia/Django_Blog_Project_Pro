from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.forms import ModelForm

from .models import Comment, Post, User


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['heading', 'short_definition', 'text', 'image', 'is_published']
        widgets = {
            'is_published': forms.RadioSelect
        }


class FeedbackForm(forms.Form):

    GRADES = (
        ('5', 'Five'),
        ('4', 'Four'),
        ('3', 'Three'),
        ('2', 'Two'),
        ('1', 'One'),
    )
    author = forms.CharField(max_length=100, required=True)
    title = forms.CharField(max_length=100, required=True)
    text = forms.CharField(widget=forms.Textarea, required=True)
    evaluate_the_blog = forms.ChoiceField(choices=GRADES, help_text='1 is the lowest score, 5 is the top score')
    reply_me = forms.BooleanField(required=False)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class PasswordForm(PasswordChangeForm):

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.save()
        return self.user


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
