from django.urls import path

from women.views import *

urlpatterns = [
    path('',index,name="home"),
    path('about/',about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>',ShowPost.as_view(),name="get_post"),
    path('categories/<slug:cat_slug>',show_categories,name="show_cat"),
    path('cat/<int:num>', categories),
    path('try<int:num_1>/<str:slug>', slag_try),
    path('param/', param),
]


