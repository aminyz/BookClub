from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Home'

urlpatterns = [
        path('', views.home, name='home'),
        path('posts/', views.pots_list, name='posts'),
        path('books/', views.book_list, name='books'),
        path('journals/', views.journal_list, name='journals'),
        path('articles/', views.article_list, name='articles'),
        path('posts/<int:id>', views.post_detail, name='post_detail'),
        path('posts/<post_id>/comment', views.post_comment, name='post_comment'),
        path('authors/', views.author_list, name='author_list'),
        path('authors/<int:id>', views.author_detail, name='author_detail'),
        path('ticket/', views.ticket, name='ticket'),
        path('login/', auth_views.LoginView.as_view(), name='login'),
        path('logout/', views.log_out, name='logout'),
        path('register/', views.register, name='register'),
        path('profile/', views.edit_profile, name='profile')
]
