from django.urls import path   # mysiteのurls.pyのpathをimport
from .views import CallbackView
from app import views  # viewsをimport

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # トップページにアクセスがあった場合にviews.pyのIndexViewを開く
    path('callback/', CallbackView.as_view(), name='callback'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),  # int:pkにはIDが入ります。データを登録すると自動的にIDが割り振られる。どのデータを処理したいのかを特定するためにint:pkにurlを設定する
    path('post/new/', views.CreatedPostView.as_view(), name='post_new'),   # 新規投稿用のurlを追加
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),   # 投稿編集用のurlを追加
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),   # 投稿削除用のurlを追加
    # <str:category>を設定することででカテゴリの名前がurl
    path('category/<str:category>', views.CategoryView.as_view(), name='category'),   # カテゴリ用のurlを追加
    path('search', views.SearchView.as_view(), name='search'),   # 検索用のurlを追加
]
