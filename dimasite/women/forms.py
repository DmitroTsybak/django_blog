from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={"class":"form-input"})) # добавляємо окремий клас для данного інпута
#     slug = forms.SlugField(max_length=255, label="URL")
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
#     is_published = forms.BooleanField(label="Публикация", required=False, initial=True)
#     category_id = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории", empty_label="Категорія не вбрана")


class AddPostForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["title"].empty_label = "Категорія не вбрана"



    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', "photo", 'is_published', 'category']
        widgets = {
            "title":forms.TextInput(attrs={"class":"form-input"}),
            "content":forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    #перевірка власної валідації, має починатися з префіка clean ,запусається після стандартної валідації
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title)>50:
            raise ValidationError("Довжина не повинна перевищувати 50 символів!!!")
        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username','email','password1','password2')