from django.shortcuts import render, redirect  # redirectを追加
from django.views.generic import TemplateView  # djangoの汎用TemplateViewをimport
from django.views.generic import View  # djangoの汎用Viewをimport
from .models import Post, Category  # model.pyで作成したPostモデル,Categoryモデルをimport
from .forms import PostForm  # forms.pyで作成したPostFormをimport
from django.contrib.auth.mixins import LoginRequiredMixin  # ログインを必須にする
from django.db.models import Q  # or検索するためにdjango.db.modelsからQモジュールを使用
from functools import reduce  # 演算を使用
from operator import and_  # 足し算
from django.http.response import HttpResponse

class CallbackView(View):
		def get(self, request, *args, **kwargs):
				return HttpResponse('OK')

# LoginRequiredMixinを引数に追加することでプロフィールを見るのにログインを必須にする 
class IndexView(LoginRequiredMixin, View):  # appのurls.pyに記載するclassを書く(トップページにアクセスがあった時に表示)
    def get(self, request, *args, **kwargs):  # 画面が表示されたら呼ばれる 
        post_data = Post.objects.order_by('-id')  # postモデルからデータを取得, order_byで並び替え('-id'で降順)
        return render(request, 'app/index.html', {  # 指定したテンプレートにデータを渡す
            'post_data': post_data 
        })
    
    # template_name = 'app/index.html'

class PostDetailView(View):  # 投稿詳細クラス
    def get(self, request, *args, **kwargs):  # 画面が表示されたら呼ばれる 
        post_data = Post.objects.get(id=self.kwargs['pk'])  # self.kwargs['pk']でidを取得
        return render(request, 'app/post_detail.html', {  # 指定したテンプレートにデータを渡す
            'post_data': post_data 
        })  

class CreatedPostView(LoginRequiredMixin, View):  # 投稿用クラス
    def get(self, request, *args, **kwargs):  # 画面が表示されたら呼ばれる 
        form = PostForm(request.POST or None)
        return render(request, 'app/post_form.html', {  # 指定したテンプレートにデータを渡す
            'form': form
        })
    
    def post(self, request, *args, **kwargs):  # ボタンを押したら考慮される
        form = PostForm(request.POST or None)

        if form.is_valid():  # formの内容をチェック
            post_data = Post()
            post_data.author = request.user  # ログインユーザーを代入
            post_data.title = form.cleaned_data['title']  # タイトルはフォームで入力されたタイトルを代入。'form.cleaned_data'でフォームの内容を取得
            category = form.cleaned_data['category']  # フォームから入力されたカテゴリを取得します
            category_data = Category.objects.get(name=category)  # カテゴリモデルから取得したカテゴリでフィルターをかけてデータを取得いたします。
            post_data.category = category_data  # カテゴリデータをpost_dataに登録します
            post_data.content = form.cleaned_data['content']  # 本文はフォームで入力された本文を代入。'form.cleaned_data'でフォームの内容を取得
            if request.FILES:  # 画像がアップロードされたら、
                post_data.image = request.FILES.get('image')  # forms.pyで取得した画像をpost_dataに格納
            post_data.save()  # save関数を考慮することで、データベースに保存することができる
            return redirect('post_detail', post_data.id)  # フォームにエラーがあったら、投稿フォームを表示する
     
        return render(request, 'app/post_form.html', {  # 指定したテンプレートにデータを渡す
            'form': form
        })

class PostEditView(LoginRequiredMixin, View):  # 投稿編集用クラス
    def get(self, request, *args, **kwargs):  # 画面が表示されたら呼ばれる 
        post_data = Post.objects.get(id=self.kwargs['pk'])  # self.kwargs['pk']でidを取得
        form = PostForm(request.POST or None,
            initial = {  # フォームには初期値を入れたいので'PostForm'の引数にinitial
                'title': post_data.title,
                'category': post_data.category,
                'content': post_data.content,
                'image': post_data.image,
            }
        )

        return render(request, 'app/post_form.html', {  # 指定したテンプレートにデータを渡す
            'form': form
        })

    def post(self, request, *args, **kwargs):  # 画面が表示されたら呼ばれる 
        form = PostForm(request.POST or None)  # Post.Formを考慮してフォームに格納

        if form.is_valid():  # formの内容をチェック
            post_data = Post.objects.get(id=self.kwargs['pk'])  # self.kwargs['pk']でidを取得
            post_data.title = form.cleaned_data['title']  # タイトルはフォームで入力されたタイトルを代入。'form.cleaned_data'でフォームの内容を取得

            # CreatedPostViewのpost関数と同じ修正をする
            category = form.cleaned_data['category']  # フォームから入力されたカテゴリを取得します
            category_data = Category.objects.get(name=category)  # カテゴリモデルから取得したカテゴリでフィルターをかけてデータを取得いたします。
            post_data.category = category_data  # カテゴリデータをpost_dataに登録します

            post_data.content = form.cleaned_data['content']  # 本文はフォームで入力された本文を代入。'form.cleaned_data'でフォームの内容を取得
            if request.FILES:  # 画像がアップロードされたら、
                post_data.image = request.FILES.get('image')  # forms.pyで取得した画像をpost_dataに格納
            post_data.save()  # save関数を考慮することで、データベースに保存することができる
            return redirect('post_detail', self.kwargs['pk'])  # フォームにエラーがあったら、投稿フォームを表示する
     
        return render(request, 'app/post_form.html', {  # 指定したテンプレートにデータを渡す
            'form': form
        })

class PostDeleteView(LoginRequiredMixin, View):  # 投稿削除用クラス
    def get(self, request, *args, **kwargs):  # 画面が表示されたら呼ばれる 
        post_data = Post.objects.get(id=self.kwargs['pk'])  # urlからself.kwargs['pk']でidを取得してpost_dataを取得します
        return render(request, 'app/post_delete.html', {  # 指定したテンプレートにpost_dataを渡す
            'post_data': post_data 
        })  

    def post(self, request, *args, **kwargs):  # 画面が表示されたら呼ばれる 
        post_data = Post.objects.get(id=self.kwargs['pk'])  # urlからself.kwargs['pk']でidを取得してpost_dataを取得します
        post_data.delete()  # post_dataを削除
        return redirect('index')


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        # urlからカテゴリ名を取得し、カテゴリモデルでフィルターをかけてデータを取得
        category_data = Category.objects.get(name=self.kwargs['category'])
        # order_by関数でデータの並び替え('-id'で降順に並び替え)、category_dataでフィルターをかける
        post_data = Post.objects.order_by('-id').filter(category=category_data)
        return render(request, 'app/index.html', {  # 指定したテンプレートにpost_dataを渡す
            'post_data' : post_data
        })


class SearchView(View):
    def get(self, request, *args, **kwargs):
        # 投稿のidで降順に並び替え
        post_data = Post.objects.order_by('-id')
        keyword = request.GET.get('keyword')  # 検索ホームからキーワードを取得します
        q=keyword

        if keyword:
            exclusion_list = set([' ', '  '])  # 半角スペースと全角スペースで半角と全角のスペースを除外するリストを作成する
            query_list = ''  # 空文字
            for word in keyword:
                if not word in exclusion_list:  
                    query_list += word  # スペースを除いた文字を抽出する
            # keywordをQオブジェクトで「or検索」する
            query = reduce(and_, [
                Q(title__icontains=q) | 
                Q(content__icontains=q) for q in query_list])
            post_data = post_data.filter(query)  # Qオブジェクトを使用して、投稿データをキーワードでフィルターをかける
        
        return render(request, 'app/index.html', {  # 指定したテンプレートにkeyword,post_dataを渡す
            'keyword': keyword,
            'post_data': post_data
        })
