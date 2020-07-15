from posts.models import Vote


def get_vote_analytics_data(queryset=None):
    """
    Get vote analytics
    :params queryset: Vote queryset
    :return: dict
    """
    data = {
        "count_votes": None,
        "count_like_vote": None,
        "count_unlike_vote": None
    }
    if queryset:
        data.update({
            "count_votes": queryset.count(),
            "count_like_vote": queryset.filter(vote=Vote.LIKE).count(),
            "count_unlike_vote": queryset.filter(vote=Vote.UNLIKE).count()
        })
    return data
