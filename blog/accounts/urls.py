from django.urls import path

from accounts.views import UserAccountListAPIView, UserAccountRetrieveApiView

urlpatterns = [
    path('users/', UserAccountListAPIView.as_view(), name='users'),
    path('users/<int:pk>/', UserAccountRetrieveApiView.as_view(), name='user')
]

