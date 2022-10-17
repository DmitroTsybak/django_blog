from django.urls import path

from women.views import *

urlpatterns = [
    path('',index,name="home"),
    path('about/',about, name='about'),
    path('addpage/', add_page, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>',get_post,name="get_post"),
    path('categories/<slug:cat_slug>',show_categories,name="show_cat"),
    path('cat/<int:num>', categories),
    path('try<int:num_1>/<str:slug>', slag_try),
    path('param/', param),
]


