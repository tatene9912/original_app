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
    path('profile_detail/<int:pk>/', views.ProfileView.as_view(), name='profile_detail'),
    path('profile_detail/', views.ProfileView.as_view(), name='profile'),
]
