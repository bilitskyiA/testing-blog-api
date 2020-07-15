from django.core.exceptions import ValidationError

from rest_framework import viewsets, generics
from rest_framework.response import Response

from rest_framework_tracking.mixins import LoggingMixin

from posts.models import Vote, Post
from posts.serializers import VoteSerializer, PostSerializer, AnalyticsSerializer
from posts.servicies import get_vote_analytics_data


class PostModelViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    Endpoint for creating and getting posts
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class VoteApiView(LoggingMixin, generics.ListCreateAPIView):
    """
    Endpoint for creating and getting votes
    """
    serializer_class = VoteSerializer

    def get_queryset(self):
        queryset = Vote.objects.all()
        post_id = self.kwargs.get('post_id', None)
        if post_id:
            queryset.filter(post=int(post_id))
        return queryset


class AnalyticsApiView(LoggingMixin, generics.RetrieveAPIView):
    """
    Vote analytics. You can choose vote for calculation in specific date range.
    (e.g. ~/analytics/?start_date=2020-07-20&end_date=2020-07-21)
    """
    serializer_class = AnalyticsSerializer

    def get_queryset(self):
        queryset = Vote.objects.all()
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        try:
            if start_date:
                queryset = queryset.filter(created__gte=start_date)
            if end_date:
                queryset = queryset.filter(created__lte=end_date)
        except ValidationError:
            pass
        return queryset

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Getting votes data for analytics
        data = get_vote_analytics_data(queryset)
        serializer = self.get_serializer(data=data)
        return Response(serializer.initial_data)
