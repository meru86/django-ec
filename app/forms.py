from django import forms  # Djangoのformsをimport
from .models import Category  # models.pyのカテゴリをimport


class PostForm(forms.Form):
    category_data = Category.objects.all()  # すべてのカテゴリをcategory_dataに格納
    category_choice = {}  # 空の辞書を作成
    for category in category_data:
        category_choice[category] = category  # categoryの辞書を作成

    title = forms.CharField(max_length=30, label='タイトル')
    # [.items()]で作成されたカテゴリを選択できる
    category = forms.ChoiceField(label='カテゴリ', widget=forms.Select, choices=list(category_choice.items()))
    content = forms.CharField(label='内容', widget=forms.Textarea())  # textareaを設定することで複数行を指定できる
    image = forms.ImageField(label='イメージ画像', required=False)
