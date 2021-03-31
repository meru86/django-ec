from django.db import models
from django.conf import settings
from django.utils import timezone




# カテゴリ機能を追加
class Category(models.Model):
    name  = models.CharField('カテゴリ', max_length=100)

    def __str__(self):  # str関数を作成することで管理画面で表示される文字列を定義できる
        return self.name


class Post(models.Model):
    # [on_delete=models.CASCADE]で参照しているオブジェクトが削除されたら一緒に削除する
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # [on_delete=models.PROTECT]でカテゴリを削除する時に同時に投稿が削除されるのを防ぐ
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT)
    title = models.CharField("タイトル", max_length=200)
    image = models.ImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=True)  # 'upload_to'は画像のアップロード先を指定します
    content = models.TextField("本文")
    created =  models.DateTimeField("作成日", default=timezone.now)

    def __str__(self):  # str関数を作成することで管理画面で表示される文字列を定義できる
        return self.title
