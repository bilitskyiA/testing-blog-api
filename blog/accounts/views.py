from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_tracking.mixins import LoggingMixin


from accounts.models import UserAccount
from accounts.serializers import UserAccountSerializer


class UserAccountListAPIView(LoggingMixin, ListAPIView):
    """
    Endpoint for getting users list
    """
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all()


class UserAccountRetrieveApiView(LoggingMixin, RetrieveAPIView):
    """
    Endpoint for getting user detail information
    """
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all()


class ObtainJWTView(TokenObtainPairView):
    """
    Custom JWT token creating view to track date of last user login
    """

    def post(self, request, *args, **kwargs):
        response = super(ObtainJWTView, self).post(request, *args, **kwargs)

        if response.status_code == 200:
            user = UserAccount.objects.filter(username=self.request.POST.get("username"))
            user.update(last_login=timezone.now())

        return response
