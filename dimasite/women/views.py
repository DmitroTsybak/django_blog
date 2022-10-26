from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.views.decorators.cache import cache_page

from .models import *
from .forms import *

# Create your views here.

menu = [{'title': "Про сайт", 'url_name': 'about'},
        {'title': "Добавити статтю", 'url_name': 'add_page'},
        {'title': "Зворотній зв'язок", 'url_name': 'contact'},
        ]


# @cache_page(60)
def index(request):
    posts = Women.objects.filter(is_published=True).select_related("category")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'cat_selected': 0,
               'page_obj': page_obj,
               'title': 'Головна сторінка'}
    return render(request, "women/index.html", context=context)


def about(request):

    return render(request, "women/about.html", {"title": "About"})


class AddPage(LoginRequiredMixin,CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    extra_context = {"title":"Добавити статтю"}



# def add_page(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect("home")
#             # except:
#             #     form.add_error
#             try:
#                 form.save()
#                 return redirect("home")
#             except:
#                 form.add_error(None, "Ошибка добавления поста")
#
#     else:
#         form = AddPostForm()
#     return render(request, "women/addpage.html", {"title": "Add page", "form": form})


class Contact(CreateView):
    pass





class ShowPost(DetailView):
    model = Women  # силка на таблицю з якої підтягуються дані
    template_name = "women/info.html"  # переопреділення назви шаблону, бо автомвтично підтягує інакший!!!
    slug_url_kwarg = 'post_slug'  # по стандарту передається слаг під назвою slug, а так його міняємо

    context_object_name = 'info'  # даний клас автоматично підтягує елемент з бази, який відповідає слагу,
    # але передає його під назвою object_list , тому якщо хочемо використовувати назву яка іде в шаблоні
    # то потрібно переоприділити атрибут context_object_name!!!
    #

    # дана функція використовується для передачі динамічних даних на сторінку
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # визивається вбудований метод
        context['title']=context['info'].title # створення ключа title через звернення до обєкта який лежить в ключі info
        context['cat_selected']=context['info'].category_id
        return context
                     # "cat_selected": context_object_name.category_id}


# def get_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {"info": post,
#                "title": post.title,
#                "cat_selected": post.category_id}
#     return render(request, 'women/info.html', context=context)


def show_categories(request, cat_slug):
    cat = Category.objects.filter(slug=cat_slug)[0]
    posts = Women.objects.filter(category_id=cat.id, is_published=True).select_related("category")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj,
               'cat_selected': cat.id,
               'title': cat.name}
    return render(request, "women/index.html", context=context)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "women/register.html"
    extra_context = {'title':"Реєстрація"}
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'
    extra_context = {'title': "Авторизація"}

    def get_success_url(self): # редірект у випадку успішної реєстрації!!!
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')

def categories(request, num):
    if num > 60:
        raise Http404()
    return HttpResponse(f"<h1>The different categories  {num} </h1>")


def slag_try(req, num_1, slug):
    return HttpResponse(f"<h1>Hello it is try page!!!</h1>"
                        f"<p>This is int first: {num_1} </p>"
                        f"<p>This is slug second : {slug} </p>")


def param(request):
    res = request.GET
    print(res)
    if res:
        return HttpResponse(f"<h2>Hello it is param page!!!</h2>"
                            f"<p>This is first param :  {res[list(res.keys())[0]]}</p>"
                            f"<p>This is second param : {res[list(res.keys())[1]]}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h3>Mistace 404 !!! Sorry not found</h3>")
