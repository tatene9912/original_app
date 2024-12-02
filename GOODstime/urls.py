from django.urls import path
from . import views

app_name = 'GOODstime'

urlpatterns = [
    path('', views.IndexView.as_view(),name="top"),
    path('new/', views.PostCreateView.as_view(),name="new"),
    path('my_post_list/', views.MyPostListView.as_view(), name="my_post_list"),
    path('post_update/<int:pk>/', views.PostUpdateView.as_view(),name="post_update"),
    path('post_list/', views.PostListView.as_view(),name="post_list"),
    path('post_detail/<int:pk>', views.PostDetailView.as_view(),name="post_detail"),
    path('tags/<str:tag>/', views.TagSearchView.as_view(), name='tag_search'),
    path('add_favorite/<int:post_id>/', views.add_favorite, name='add_favorite'),
    path('favorites/remove/<int:pk>/', views.remove_favorite, name='remove_favorite'),
    path('favorite_list/', views.FavoriteListView.as_view(), name="favorites_list"),
    path('mypage/', views.MyPage.as_view(), name="myPage"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('profile_detail/', views.ProfileView.as_view(), name='profile_detail'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('requested-posts/', views.RequestedPostListView.as_view(), name='requested_post_list'),
    path('interchange_detail/<int:pk>', views.InterchangeDetailView.as_view(),name="interchange_detail"),
    path('own_interchange_list/', views.OwnInterchangeListView.as_view(), name="own_interchange_list"),
    path('another_interchange_list/', views.AnotherInterchangeListView.as_view(), name="another_interchange_list"),
    path('interchange_detail/<int:pk>', views.InterchangeDetailView.as_view(),name="interchange_detail"),
    path('post_report/<int:pk>', views.ReportCreateView.as_view(),name="post_report"),
    path('review_list/<int:user_pk>/', views.ReviewListView.as_view(), name='review_list'),
    path('user_delete/<int:pk>', views.UserDeleteView.as_view(), name='user_delete'),
    path('legal/', views.LegalView.as_view(), name='legal'),
    path('guideline/', views.GuidelineView.as_view(), name='guideline'),
    path('config/', views.stripe_config),
    path('create_checkout_session/', views.create_checkout_session, name='checkout_session'),
    path('success/', views.success),
    path('cancel/', views.cancel),
    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
    path('stripe/webhook/', views.checkout_success_webhook, name='stripe_webhook'),
    path('cancelsubscription/', views.cancel_subscription, name='cancel_subscription'),
    path('cancel_subscription/', views.CancelSubscriptionView.as_view(), name='cancelSubscription'),
    path('update_payment_method/', views.update_payment_method, name='update_payment_method'),
    path('update_payment_method_success/', views.PaymentUpdateSuccessView.as_view(), name='update_payment_method_success'),
    path('Inquiry/', views.InquiryCreateView.as_view(), name='Inquiry'),
]
