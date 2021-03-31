# コンテキストプロセッサー：変数ビューからテンプレートに直接渡さなくてもテンプレート上で変数を使える仕組み
from .models import Category

def common(request):
    category_data = Category.objects.all()  # すべてのcategory_dataを取得します
    context = {
        'category_data': category_data
    }
    return context  # category_dataを返すことで、どこのテンプレートでも取得することができます。
