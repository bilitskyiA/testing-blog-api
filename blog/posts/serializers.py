from rest_framework import serializers
from posts.models import Post, Vote


class VoteSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source="post.id")

    class Meta:
        model = Vote
        fields = ['id', 'author', 'post', 'vote', 'created']

    def save(self):
        """
        Dynamically add author and post to saving data of new Vote object.
        """
        url_kwargs = self.context['request'].parser_context['kwargs']
        post = Post.objects.get(id=url_kwargs.get('post_id'))
        super(VoteSerializer, self).save(
            author=self.context["request"].user,
            post=post
        )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'body', 'created', 'updated', 'votes']

    def save(self):
        """
        Dynamically add author to saving data of new Post object.
        """
        super(PostSerializer, self).save(author=self.context["request"].user)


class AnalyticsSerializer(serializers.Serializer):
    count_votes = serializers.IntegerField()
    count_like_vote = serializers.IntegerField()
    count_unlike_vote = serializers.IntegerField()
