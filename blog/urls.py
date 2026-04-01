from django.urls import path
from . import views
# URL patterns for blog app views.
app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('share/<int:post_id>/', views.post_share, name='post_share'),
    path('comment/<int:post_id>/', views.post_comment, name='post_comment'),
]
