from django.urls import path
from . import views


app_name = 'users'


urlpatterns = [ 
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('profile/', views.ProfileUserView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditUserView.as_view(), name='profile_edit'),
    path('password-change/', views.UserPasswordChangeView.as_view(),
        name='password_change'),
    path('password-change/done/', views.UserPasswordChangeDoneView.as_view(),
        name='password_change_done'),
    path('password-reset/', views.UserPasswordResetView.as_view(),
        name='password_reset'),
    path('password-reset/done/', views.UserPasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('password-reset/complete/', views.UserPasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
]
