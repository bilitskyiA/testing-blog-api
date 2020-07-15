from rest_framework import serializers
from rest_framework_tracking.models import APIRequestLog

from accounts.models import UserAccount
from posts.serializers import PostSerializer, VoteSerializer


class UserAccountSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    votes = VoteSerializer(many=True, read_only=True)
    last_activity = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'posts', 'votes', 'last_activity', 'last_login']

    @staticmethod
    def get_last_activity(obj):
        """
        Getting date of last user request using special library drf-tracking
        """
        activities = APIRequestLog.objects.filter(user=obj.id)
        if activities.exists():
            return activities.last().requested_at
        return None
