from django.urls import path   # mysiteのurls.pyのpathをimport
from accounts import views  # accountsファイルのviewをimport

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='account_login'),  # ログインページにアクセスがあった場合にviews.pyのLoginViewを開く
    path('logout/', views.LogoutView.as_view(), name='account_logout'),  # ログアウトページにアクセスがあった場合にviews.pyのLogoutViewを開く
    path('signup/', views.SignupView.as_view(), name='account_signup'),  # サインアップページにアクセスがあった場合にviews.pyのSignupViewを開く
    path('profile/', views.ProfileView.as_view(), name='profile'),  # プロフィールページにアクセスがあった場合にviews.pyのProfileViewを開く
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),  # プロフィールページにアクセスがあった場合にviews.pyのProfileViewを開く
]