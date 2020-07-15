from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.views import PostModelViewSet, VoteApiView, AnalyticsApiView

app_name = "posts"

router = DefaultRouter()
router.register('', PostModelViewSet, 'posts')

urlpatterns = [
    path('<int:post_id>/votes/', VoteApiView.as_view(), name="votes"),
    path('analytics/', AnalyticsApiView.as_view(), name="analytics"),
]

urlpatterns += router.urls
