# adminはweb上でデータベースを操作できる(削除、編集)
from django.contrib import admin
from .models import Post, Category  # modelのPost,Categoryをimport
# from .models import Post  # modelのPost,Categoryをimport

admin.site.register(Post)  # register関数を使ってmodel(Postクラス)を追加
admin.site.register(Category)  # register関数を使ってmodel(Categoryクラス)を追加
