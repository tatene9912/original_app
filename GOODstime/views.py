from django.conf import settings
from django.utils import timezone 
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.template import engines
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView, DeleteView
from GOODstime.models import Block, Favorite, Post, Report, Review, Stripe_Customer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from accounts.models import User
from .forms import CommentForm, FavoriteForm, MessageForm, PostForm, ProfileForm, ReportForm, ReviewForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import transaction
import stripe
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

class IndexView(ListView):
    template_name = "GOODstime/top.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # tag1の集計と上位3つの取得
        tag1_top3 = (
            Post.objects.values('tag1')
            .annotate(count=Count('tag1'))
            .filter(tag1__isnull=False)
            .exclude(tag1='') 
            .order_by('-count')[:3]
        )

        # tag2の集計と上位3つの取得
        tag2_top3 = (
            Post.objects.values('tag2')
            .annotate(count=Count('tag2'))
            .filter(tag2__isnull=False)
            .exclude(tag2='')
            .order_by('-count')[:3]
        )

        # tag3の集計と上位3つの取得
        tag3_top3 = (
            Post.objects.values('tag3')
            .annotate(count=Count('tag3'))
            .filter(tag3__isnull=False)
            .exclude(tag3='')
            .order_by('-count')[:3]
        )

        # コンテキストに追加
        context['tag1_top3'] = tag1_top3
        context['tag2_top3'] = tag2_top3
        context['tag3_top3'] = tag3_top3

        context['search_count'] = self.get_queryset().count()
        context['query'] = self.request.GET.get('q', '')

        return context
    
    def get_queryset(self):
        # 現在のユーザー
        user = self.request.user

        # ユーザーが未認証の場合でも処理を続行できるようにする
        if user.is_authenticated:
            # 現在のユーザーがブロックしているユーザーを除外
            blocked_users = Block.objects.filter(user=user).values_list('target_user', flat=True)

            # ブロックされたユーザーを除外した投稿のクエリセット
            queryset = Post.objects.exclude(user__in=blocked_users).order_by('-created_at')
        else:
            # 未認証のユーザーには制限なしで投稿を表示
            queryset = Post.objects.all().order_by('-created_at')

        return queryset

from django.shortcuts import get_object_or_404

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'GOODstime/post_create.html'
    model = Post
    login_url = reverse_lazy('accounts:login')
    form_class = PostForm

    def form_valid(self, form):
        # 現在のユーザー
        user = self.request.user

        # Stripe_Customerに関連付けられているか確認
        is_paid_member = Stripe_Customer.objects.filter(user=user).exists()

        # 有料会員でない場合、投稿数制限をチェック
        if not is_paid_member:
            now = timezone.now()
            current_month_posts_count = Post.objects.filter(
                user=user,
            ).count()

            # 投稿制限を超えている場合
            if current_month_posts_count >= 5:
                messages.error(self.request, '今月の投稿数上限を超えています。')
                return self.form_invalid(form)

        # 制限を超えていない場合、または有料会員の場合は投稿を保存
        post = form.save(commit=False)
        post.user = user
        post.save()
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
        post_id = request.POST.get('post_id') 

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

        # 現在のユーザー
        user = self.request.user

        # 現在のユーザーがブロックしているユーザーを除外
        blocked_users = Block.objects.filter(user=user).values_list('target_user', flat=True)
        queryset = queryset.exclude(user__in=blocked_users)

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

        # 譲渡キャラ名の検索
        if give_query := query.get('give_character'):
            queryset = queryset.filter(give_character__icontains=give_query)

        # 希望キャラ名の検索
        if want_query := query.get('want_character'):
            queryset = queryset.filter(want_character__icontains=want_query)

        # フィルターの処理（取引未成立の投稿のみ）
        filter_status = self.request.GET.get('filter_status')
        if filter_status == 'uncompleted':
            queryset = queryset.filter(status='unmatched')

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

        return context

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)  # request.FILES を追加
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールを更新しました。')
            return redirect('GOODstime:myPage')
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
        user = self.request.user

        # 良かった評価の数を取得
        context['good_score'] = Review.objects.filter(target_user=user, score=1).count()

        # 悪かった評価の数を取得
        context['bad_score'] = Review.objects.filter(target_user=user, score=2).count()

        # 必要に応じて他のコンテキストを追加
        context['profile'] = self.get_object()  # ログイン中のユーザー情報をコンテキストに追加
        return context

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'GOODstime/user_profile.html'
    context_object_name = 'profile_user'  # テンプレート内でアクセスする際の名前を指定

    def get_object(self, queryset=None):
        # URLのkwargsからpkを取得して特定のユーザーを取得
        pk = self.kwargs.get('pk')
        if pk is None:
            raise Http404("ユーザーが指定されていません。")
        return get_object_or_404(User, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()  # プロフィール対象のユーザー
        user = self.request.user  # ログイン中のユーザー

        # 良かった評価の数を取得
        context['good_score'] = Review.objects.filter(target_user=profile_user, score=1).count()

        # 悪かった評価の数を取得
        context['bad_score'] = Review.objects.filter(target_user=profile_user, score=2).count()

        # ログイン中のユーザーがすでにブロックしているか確認
        context['is_blocked'] = Block.objects.filter(user=user, target_user=profile_user).exists()

        # プロフィール対象のユーザーの投稿一覧を取得
        context['posts'] = Post.objects.filter(user=profile_user).order_by('-created_at')  # 最新順
        # 投稿一覧をページネート
        posts = Post.objects.filter(user=profile_user).order_by('-created_at')
        paginator = Paginator(posts, 10)  # 1ページに10件表示
        page = self.request.GET.get('page')
        context['posts'] = paginator.get_page(page)

        return context

    def post(self, request, *args, **kwargs):
        profile_user = self.get_object()
        user = request.user

        if user == profile_user:
            messages.error(request, "自分自身をブロックまたは解除することはできません。")
            return redirect('GOODstime:user_profile', pk=profile_user.pk)

        # ブロックする処理
        if 'add_block' in request.POST:
            if not Block.objects.filter(user=user, target_user=profile_user).exists():
                Block.objects.create(user=user, target_user=profile_user)
                messages.success(request, f"{profile_user.nic_name} をブロックしました。")
            else:
                messages.warning(request, f"{profile_user.nic_name} はすでにブロックされています。")

        # ブロック解除する処理
        if 'remove_block' in request.POST:
            block = Block.objects.filter(user=user, target_user=profile_user).first()
            if block:
                block.delete()
                messages.success(request, f"{profile_user.nic_name} のブロックを解除しました。")
            else:
                messages.warning(request, f"{profile_user.nic_name} はブロックされていません。")

        return redirect('GOODstime:user_profile', pk=profile_user.pk)
    
class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'GOODstime/review_list.html'
    paginate_by = 10

    def get_queryset(self):
        # URL のパラメータから対象ユーザーを取得
        user_pk = self.kwargs.get('user_pk')  # プロフィールページから渡されるユーザーID
        review_type = self.request.GET.get('type', 'good')  # デフォルトで 'good'

        # 対象ユーザーのレビューをフィルタリング
        try:
            target_user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Review.objects.none()

        if review_type == 'good':
            return Review.objects.filter(target_user=target_user, score=1)
        elif review_type == 'bad':
            return Review.objects.filter(target_user=target_user, score=2)
        else:
            return Review.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 対象ユーザーとフィルタタイプをコンテキストに追加
        user_pk = self.kwargs.get('user_pk')
        context['target_user'] = User.objects.get(pk=user_pk)
        context['current_type'] = self.request.GET.get('type', 'good')
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
        user = self.request.user

        context['message_form'] = MessageForm()
        context['review_form'] = ReviewForm()
        context['messages_post'] = post.messages.all()

        if user.is_authenticated:
            if post.user == user:
                target_user = post.match_user
            else:
                target_user = post.user
            context['has_posted_review'] = Review.objects.filter(user=user, target_user=target_user, post=post).exists()
        else:
            context['has_posted_review'] = False

        return context

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        user = request.user

        # メッセージ投稿
        if 'message_submit' in request.POST:
            message_form = MessageForm(data=request.POST)
            post = Post.objects.filter(id=post_id).first()
            if not post:
                return redirect('some_error_page')

            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.post = post
                message.user = user
                message.save()
                messages.success(self.request, 'メッセージを送信しました。')
                return redirect('GOODstime:interchange_detail', pk=post.pk)
            else:
                messages.error(self.request, 'メッセージの送信に失敗しました。')
                return self.render_to_response(self.get_context_data(message_form=message_form))

        # 評価登録
        if 'review_submit' in request.POST:
            review_form = ReviewForm(data=request.POST)
            post = Post.objects.filter(id=post_id).first()
            if not post:
                return redirect('some_error_page')

            # ターゲットユーザーの判定
            target_user = post.match_user if post.user == user else post.user

            # 二重評価を防ぐ
            if Review.objects.filter(user=user, target_user=target_user, post=post).exists():
                messages.error(self.request, '既にこの取引に対する評価を登録済みです。')
                return redirect('GOODstime:interchange_detail', pk=post.pk)

            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = user
                review.target_user = target_user
                review.post = post
                review.save()

                # 両方のユーザーが評価済みかチェックしてステータスを更新
                if Review.objects.filter(post=post, user=post.user).exists() and Review.objects.filter(post=post, user=post.match_user).exists():
                    post.status = 'completed'
                    post.save()

                messages.success(self.request, '評価を登録しました。')
                return redirect('GOODstime:interchange_detail', pk=post.pk)
            else:
                messages.error(self.request, '評価の登録に失敗しました。')
                return self.render_to_response(self.get_context_data(review_form=review_form))

        # 取引キャンセル
        if 'cancel_transaction' in request.POST:
            post = Post.objects.filter(id=post_id).first()
            if not post:
                messages.error(self.request, '該当する取引が見つかりませんでした。')
                return redirect('GOODstime:another_interchange_list')

            post.match_user = None
            post.status = "unmatched"
            post.save()
            messages.success(self.request, '取引をキャンセルしました。')
            return redirect('GOODstime:another_interchange_list')

        return redirect('GOODstime:another_interchange_list')

class ReportCreateView(LoginRequiredMixin, CreateView):
    template_name = 'GOODstime/post_report.html'
    model = Report
    login_url = reverse_lazy('accounts:login')
    form_class = ReportForm

    def form_valid(self, form):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])

        # すでに通報しているかチェック
        existing_report = Report.objects.filter(user=user, post=post).first()
        if existing_report:
            messages.error(self.request, 'この投稿に対する通報はすでに行われています。')
            return redirect('GOODstime:post_detail', pk=post.pk)

        # 通報を保存
        report = form.save(commit=False)
        report.user = user
        report.post = post
        report.save()

        # 通報数を確認して削除フラグを設定
        report_count = Report.objects.filter(post=post).count()
        if report_count >= 1:
            post.delete_flg = True
            post.save()

        messages.success(self.request, '投稿を通報しました。')
        return super().form_valid(form)

    success_url = reverse_lazy('GOODstime:top')

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'GOODstime/user_delete.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        # ログインしていない場合はリダイレクト
        if self.request.user.is_anonymous:
            return redirect('login')  # ログインページにリダイレクト
        return self.request.user

    def get_success_url(self):
        messages.info(self.request, '退会しました。')
        return reverse_lazy('GOODstime:top')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()

        # トランザクションを使用して、関連データを削除
        with transaction.atomic():
            # ユーザーに関連するデータを削除する処理
            user.posts.all().delete()  # ユーザーの投稿を削除
            user.reviews.all().delete()  # ユーザーのレビューを削除
            
        # 最後にユーザー自身を削除
        return super().delete(request, *args, **kwargs)

class LegalView(TemplateView):
    template_name = 'GOODstime/legal.html'

class SubscriptionView(TemplateView):
    template_name = 'GOODstime/subscription.html'

# 設定用の処理
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)

# 支払い画面に遷移させるための処理
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # ユーザーが認証されているか確認
        if request.user.is_authenticated:
            # ユーザーがすでに Stripe カスタマーであるか確認
            if hasattr(request.user, 'stripe_customer'):

                return redirect('GOODstime:cancel_subscription')  
            
            try:
                checkout_session = stripe.checkout.Session.create(
                    client_reference_id=request.user.id,
                    success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=domain_url + 'cancel/',
                    payment_method_types=['card'],
                    mode='subscription',
                    line_items=[
                        {
                            'price': settings.STRIPE_PRICE_ID,
                            'quantity': 1,
                        }
                    ]
                )
                return redirect(checkout_session.url)
            except Exception as e:
                return JsonResponse({'error': str(e)})
        

endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

@csrf_exempt
def checkout_success_webhook(request):
    payload = request.body
    sig_header = request.headers.get('stripe-signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print("Invalid payload:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature:", e)
        return HttpResponse(status=400)

    # デバッグ出力
    print("Received event:", event)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("Checkout session completed:", session)

        # 顧客情報を確認
        customer_id = session['customer']
        print("Customer ID:", customer_id)  # デバッグ出力

        # 顧客情報をStripeから取得
        customer = stripe.Customer.retrieve(customer_id)
        email = customer['email']
        print("Email:", email)  # デバッグ出力

        # 支払い方法を取得するためのAPI呼び出し
        payment_methods = stripe.PaymentMethod.list(
            customer=customer_id,
            type="card"
        )
        
        if payment_methods.data:
            payment_method_id = payment_methods.data[0].id  # 最初の支払い方法を取得
            print("Payment Method ID:", payment_method_id)  # デバッグ出力
        else:
            print("No payment methods found.")
            payment_method_id = None

        try:
            user = User.objects.get(email=email)
            print("User:", user)  # デバッグ出力

            # Stripe_Customerの取得または作成
            stripe_customer, created = Stripe_Customer.objects.get_or_create(
                user=user,
                defaults={
                    'stripeCustomerId': customer_id,  # 顧客ID
                    'stripeSubscriptionId': session.get('subscription', None),  # サブスクリプションID
                    'stripePaymentMethodId': payment_method_id  # 支払い方法ID
                }
            )
            if not created:
                stripe_customer.stripeSubscriptionId = session.get('subscription', None)
                stripe_customer.stripePaymentMethodId = payment_method_id  # 支払い方法IDを更新
                stripe_customer.save()

            print(f"Stripe Customer {'created' if created else 'updated'} for user: {user}")

        except User.DoesNotExist:
            print(f"User with email {email} does not exist.")
        except Exception as e:
            print(f"Error in fulfilling order: {str(e)}")

    elif event['type'] == 'invoice.payment_succeeded':
        # ここにinvoice.payment_succeededの処理を追加できます
        pass

    return HttpResponse(status=200)



# 支払いに成功した後の画面
def success(request):
    return render(request, 'GOODstime/success.html')

# 支払いに失敗した後の画面
def cancel(request):
    return render(request, 'GOODstime/cancel.html')

@csrf_exempt
@login_required
def update_payment_method(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_method_id = data.get('payment_method_id')
            subscription_id = data.get('subscription_id')

            print('payment_method_id:', payment_method_id)
            print('subscription_id:', subscription_id)

            if not payment_method_id:
                return JsonResponse({'status': 'error', 'message': 'Payment method ID is missing'})

            stripe.api_key = settings.STRIPE_SECRET_KEY
            
            # サブスクリプションから古い支払い方法を取得
            subscription = stripe.Subscription.retrieve(subscription_id)
            old_payment_method_id = subscription.default_payment_method
            print('old_payment_method_id:', old_payment_method_id)

            if old_payment_method_id:
                # 古い支払い方法のデタッチ
                stripe.PaymentMethod.detach(old_payment_method_id)
                print('古い支払い方法がデタッチされました')

            # 新しいカード情報を顧客にアタッチ
            customer = subscription.customer
            stripe.PaymentMethod.attach(payment_method_id, customer=customer)
            print('新しい支払い方法がアタッチされました')

            # デフォルトの支払い方法を更新
            stripe.Customer.modify(
                customer,
                invoice_settings={
                    'default_payment_method': payment_method_id,
                },
            )
            print('デフォルトの支払い方法が更新されました')

            # Stripe_Customerを取得し、支払い方法IDを更新
            stripe_customer = Stripe_Customer.objects.get(user=request.user)
            stripe_customer.stripePaymentMethodId = payment_method_id  # 新しい支払い方法IDを保存
            stripe_customer.save()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    elif request.method == 'GET':
        try:
            # 現在のユーザーに関連するStripe_Customerを取得
            subscription = Stripe_Customer.objects.get(user=request.user)
            subscription_id = subscription.stripeSubscriptionId  # サブスクリプション ID
            old_payment_method_id = subscription.stripePaymentMethodId  # 古い支払い方法 ID
        except Stripe_Customer.DoesNotExist:
            subscription_id = None
            old_payment_method_id = None  # 古い支払い方法 ID がない場合の処理
        
        context = {
            'subscription_id': subscription_id,
            'old_payment_method_id': old_payment_method_id,  # 古い支払い方法 ID をコンテキストに追加
        }
        return render(request, 'GOODstime/update_payment_method.html', context)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



class PaymentUpdateSuccessView(TemplateView):
    template_name = 'GOODstime/update_payment_method_success.html'

class CancelSubscriptionView(TemplateView):
    template_name = 'GOODstime/cancel_subscription.html'


def cancel_subscription(request):
    if request.user.is_authenticated:
        try:
            # StripeのAPIキーを設定
            stripe.api_key = settings.STRIPE_SECRET_KEY
            
            stripe_customer = request.user.stripe_customer  # Stripe カスタマー情報を取得
            subscription_id = stripe_customer.stripeSubscriptionId  # サブスクリプションIDを取得

            # Stripe APIを使ってサブスクリプションをキャンセル
            stripe.Subscription.delete(subscription_id)
            print(f"Subscription {subscription_id} canceled successfully.")

            # Stripe_Customerレコードを削除
            stripe_customer.delete()
            print(f"Stripe_Customer record for user {request.user} deleted successfully.")

            return render(request, 'GOODstime/cancel_success.html')  # 解約成功ページにリダイレクト

        except stripe.error.StripeError as e:
            # Stripe APIでのエラー処理
            print(f"Error in canceling subscription: {e}")
            return redirect('error_page')  # エラーページにリダイレクト

        except Exception as e:
            # その他のエラー処理
            print(f"Unexpected error: {e}")
            return redirect('error_page')  # エラーページにリダイレクト
    else:
        return redirect('login')  # 認証されていない場合はログインページへ