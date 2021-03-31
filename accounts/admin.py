from django.contrib import admin

from .models import CustomUser

admin.site.register(CustomUser)  # register関数を使ってmodel(CustomtUserクラス)を追加
