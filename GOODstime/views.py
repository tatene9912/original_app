from django.shortcuts import get_object_or_404, redirect, render
from django.template import engines
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView
from GOODstime.models import Favorite, Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from accounts.models import User
from .forms import CommentForm, FavoriteForm, MessageForm, PostForm, ProfileForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

class IndexView(generic.TemplateView):
    template_name = "GOODstime/top.html"


    def get(self, request, *args, **kwargs):
        print("Template search paths:", engines['django'].dirs)
        return super().get(request, *args, **kwargs)

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'GOODstime/post_create.html'
    model = Post
    login_url = reverse_lazy('accounts:login')
    form_class = PostForm

    def form_valid(self, form):
        menu = form.save(commit=False)
        menu.user = self.request.user
        menu.save()
        messages.success(self.request, '投稿が完了しました。')
        return super().form_valid(form)
    
    success_url = reverse_lazy('GOODstime:top')

class PostUpdateView(UpdateView):
    template_name = 'GOODstime/post_update.html'
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        menu = form.save(commit=False)
        menu.save()
        messages.success(self.request, '投稿を編集しました。')
        return redirect('GOODstime:myPage')
    
class MyPostListView(ListView):
    model = Post
    template_name = "GOODstime/my_post_list.html"
    paginate_by = 15
    context_object_name = 'posts'

    def get_queryset(self):
        # ログイン中のユーザーに関連する投稿のみをフィルタリングし、関連するuserとmatch_userを効率的に取得
        return Post.objects.filter(user=self.request.user).select_related('user', 'match_user')
    
    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        user = request.user

        # 取引キャンセル処理
        if 'delete_post' in request.POST:
            try:
                post = Post.objects.get(id=post_id)
                post.delete()
                messages.success(self.request, '投稿を削除しました。')
            except Post.DoesNotExist:
                messages.error(self.request, '該当する投稿が見つかりませんでした。')

            return redirect('GOODstime:my_post_list')

        return redirect('GOODstime:my_post_list')


class PostListView(ListView):
    model = Post
    template_name = "GOODstime/post_list.html"
    paginate_by = 15
    context_object_name = 'posts'

    SORT_OPTIONS = [
        {'key': 'price_high', 'value': '価格順が高い順'},
        {'key': 'price_low', 'value': '価格が低い順'},
        {'key': 'created_at', 'value': '新しい順'},
    ]

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET

        # 検索条件の処理
        if q := query.get('q'):
            queryset = queryset.filter(
                Q(work_name__icontains=q) |
                Q(content__icontains=q) |
                Q(tag1__icontains=q) |
                Q(tag2__icontains=q) |
                Q(tag3__icontains=q) |
                Q(give_character__icontains=q) |
                Q(want_character__icontains=q)
            )

        # フィルターの処理（取引未成立の投稿のみ）
        filter_status = self.request.GET.get('filter_status')
        if filter_status == 'uncompleted':
            queryset = queryset.filter(status='unmatched')
            print(f"After Filter Query Count: {queryset.count()}")

        # 並び替えの処理
        sort = query.get('order_by')
        if sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'price_low':
            queryset = queryset.order_by('price')
        else:
            # デフォルトは作成日順
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['search_count'] = self.get_queryset().count()
        context['query'] = query

        # 並び替えオプションをコンテキストに追加
        context['sort_list'] = self.SORT_OPTIONS

        # 現在の並び替えオプションをコンテキストに追加
        context['current_sort'] = self.request.GET.get('order_by', 'created_date')

        # 現在のフィルター状態をコンテキストに追加
        context['current_filter'] = self.request.GET.get('filter_status', '')

        return context

    
class PostDetailView(DetailView):
    model = Post
    template_name = 'GOODstime/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])
        user = self.request.user

        # お気に入りチェック
        if user.is_authenticated:
            favorite = Favorite.objects.filter(user=user, post=post).first()
            context['is_favorite'] = favorite is not None
            context['favorite'] = favorite
        else:
            context['is_favorite'] = False
            context['favorite'] = None

        # お気に入りの数を取得
        favorite_count = Favorite.objects.filter(post=post).count()
        context['favorite_count'] = favorite_count

        # コメントフォームを渡す
        context['comment_form'] = CommentForm()

        # 投稿に紐付くコメントを渡す
        context['comments'] = post.comments.all()

        # 取引未成立のチェック
        is_unmatched = post.status == "unmatched"
        context['is_unmatched'] = is_unmatched

        return context

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        user = request.user

        # コメント投稿
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(data=request.POST)
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return redirect('some_error_page') 

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.user = user
                comment.save()
                messages.success(self.request, 'コメントを投稿しました')
                return redirect('GOODstime:post_detail', pk=post.pk)
            else:
                context = self.get_context_data(**kwargs)
                context['comment_form'] = comment_form
                context['error_message'] = comment_form.errors
                return self.render_to_response(context)

        # リクエスト送信
        elif 'request_match' in request.POST:
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                messages.error(self.request, '対象の投稿が見つかりませんでした。')
                return redirect('GOODstime:post_list')

            # 取引未成立ならばユーザーを登録
            if post.match_user is None:
                post.match_user = user
                post.save()
                messages.success(self.request, 'リクエストを送信しました。')
            else:
                messages.error(self.request, '他にリクエスト中のユーザーがいます。')

            return redirect('GOODstime:post_detail', pk=post.pk)

        return redirect('GOODstime:post_list')


class TagSearchView(ListView):
    model = Post
    template_name = 'GOODstime/post_tag_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return Post.objects.filter(tag1=tag) | Post.objects.filter(tag2=tag) | Post.objects.filter(tag3=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag')  # タグ名をテンプレートに渡す
        return context

def add_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # post を取得
    if request.method == 'POST':
        # 既存のお気に入りをチェック
        if Favorite.objects.filter(user=request.user, post=post).exists():
            messages.info(request, 'すでにお気に入りに追加されています。')
            return redirect('GOODstime:post_detail', pk=post.id)

        favorite = Favorite(user=request.user, post=post)  # 新しいお気に入りを作成
        favorite.save()
        messages.success(request, 'お気に入りに追加しました。')
        return redirect('GOODstime:post_detail', pk=post.id)

    return redirect('GOODstime:post_detail', pk=post.id)


def remove_favorite(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk, user=request.user)
    favorite.delete()
    messages.success(request, 'お気に入りを解除しました。')
    return redirect('GOODstime:post_detail', pk=favorite.post.id)  # リダイレクト先を post_detail に設定

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'GOODstime/favorites_list.html'
    paginate_by = 10

    def get_queryset(self):
        # ログイン中のユーザーに関連するお気に入りのみをフィルタリング
        return Favorite.objects.filter(user=self.request.user)


class MyPage(LoginRequiredMixin, TemplateView):
    template_name = 'GOODstime/myPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user 
        return context

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールを更新しました。')
            return redirect('GOODstime:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'GOODstime/edit_profile.html', {
        'form': form,
    })

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'GOODstime/profile_detail.html'

    def get_object(self, queryset=None):
        # ログイン中のユーザー情報を取得
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 必要に応じて他のコンテキストを追加
        context['profile'] = self.get_object()  # ログイン中のユーザー情報をコンテキストに追加
        return context

# 別のユーザーのプロフィールを表示する
class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'GOODstime/user_profile.html'

    def get_object(self, queryset=None):
        # URLのpkで指定されたユーザーを取得
        pk = self.kwargs.get('pk')
        return User.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context

    
class RequestedPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "GOODstime/requested_post_list.html"
    context_object_name = "requested_posts"

    def get_queryset(self):
        # match_userが設定されていて取引未成立の投稿を取得
        queryset = Post.objects.filter(user=self.request.user, match_user__isnull=False, status='unmatched')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requested_posts = Post.objects.filter(user=self.request.user, match_user__isnull=False, status='unmatched')
        context['requested_posts'] = requested_posts
        return context

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            messages.error(request, "対象の投稿が見つかりませんでした。")
            return redirect('GOODstime:requested_post_list')

        if action == "approve":
            # 取引成立に更新
            post.status = "matched"
            post.save()
            messages.success(request, "リクエストを承認しました。")
        elif action == "reject":
            # match_userを解除
            post.match_user = None
            post.status = "unmatched"
            post.save()
            messages.success(request, "リクエストを削除しました。")
        else:
            messages.error(request, "不正なアクションです。")

        return redirect('GOODstime:requested_post_list')
    
class OwnInterchangeListView(ListView):
    model = Post
    template_name = "GOODstime/own_interchange_list.html"
    paginate_by = 15
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user, status='matched')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_path'] = self.request.path  # 現在のURLを渡す
        return context
    
class AnotherInterchangeListView(ListView):
    model = Post
    template_name = "GOODstime/another_interchange_list.html"
    paginate_by = 15
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(match_user=self.request.user, status='matched')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_path'] = self.request.path  # 現在のURLを渡す
        return context

class InterchangeDetailView(DetailView):
    model = Post
    template_name = 'GOODstime/interchange_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # メッセージフォームを渡す
        context['message_form'] = MessageForm()

        # 投稿に紐付くメッセージを渡す
        context['messages_post'] = post.messages.all()

        storage = messages.get_messages(self.request)
        storage.used = True

        return context
    
    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        user = request.user

        # メッセージ投稿
        if 'message_submit' in request.POST:
            message_form = MessageForm(data=request.POST)
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return redirect('some_error_page') 

            if message_form.is_valid():
                print("Message form is valid")
                message = message_form.save(commit=False)
                message.post = post
                message.user = user
                message.save()
                messages.success(self.request, 'メッセージを送信しました。')
                return redirect('GOODstime:interchange_detail', pk=post.pk)
            else:
                context = self.get_context_data(**kwargs)
                context['message_form'] = message_form
                context['error_message'] = message_form.errors  
                return self.render_to_response(context)

        # 取引キャンセル処理
        if 'cancel_transaction' in request.POST:
            try:
                post = Post.objects.get(id=post_id)
                post.match_user = None
                post.status = "unmatched"
                post.save()
                messages.success(self.request, '取引をキャンセルしました。')
            except Post.DoesNotExist:
                messages.error(self.request, '該当する取引が見つかりませんでした。')

            return redirect('GOODstime:another_interchange_list')

        return redirect('GOODstime:another_interchange_list')

