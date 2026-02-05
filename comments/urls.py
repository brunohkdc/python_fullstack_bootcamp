from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:post_id>/comments/create', views.create_comment, name='create_comment'),
    path('comments/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]