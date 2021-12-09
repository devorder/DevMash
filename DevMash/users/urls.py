from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.user_profile, name='user-profile'),
    path('account/', views.user_account, name='user-account'),
    path('profile/<str:user_id>/', views.profile, name='profile'),
    path('edit-account/', views.edit_account, name='edit-account'),
    path('add-skill/', views.add_skill, name='add-skill'),
    path('delete-skill/<str:skill_id>', views.delete_skill, name='delete-skill'),
    path('edit-skill/<str:skill_id>', views.edit_skill, name='edit-skill'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:message_id>', views.inbox_message, name='message'),
    path('send-message/<str:receiver_id>/', views.send_message, name='send-message')
]
