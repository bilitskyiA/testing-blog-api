from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import UserAccount


class Post(models.Model):
    """Model to store posts data"""
    author = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("Post author")
    )
    title = models.CharField(max_length=256, verbose_name=_("Name of post"))
    body = models.TextField(verbose_name=_("Content of post"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Vote(models.Model):
    """Model to store votes data"""

    LIKE = 1
    UNLIKE = -1
    NULL = 0

    VOTE_CHOICES = [
        (LIKE, 'Like'),
        (UNLIKE, 'Unlike'),
        (NULL, 'Null')
    ]

    author = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="votes",
        verbose_name=_("Vote author")
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=_('Post')
    )
    vote = models.SmallIntegerField(choices=VOTE_CHOICES, default=NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.post.title}'
