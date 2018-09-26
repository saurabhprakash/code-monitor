from django.db import models


class BitbucketActivityManager(models.Manager):
    """
    Bitbucket Activity Manager
    """

    def create_entry(self, **kwargs):
        """
        Create an entry to bitbucket activity model,
        :parameter kwargs: has all the fields for entry related to bitbucket activity model
        :returns: Nothing
        """
        super(BitbucketActivityManager, self).get_queryset().create(
            type_of_activity=kwargs.get('type_of_activity'),
            sub_type=kwargs.get('sub_type'),
            actor_username=kwargs.get('author_username'),
            actor_display_name=kwargs.get('author_display_name'),
            project_full_name=kwargs.get('project_full_name'),
            state=kwargs.get('state'),
            content_id=kwargs.get('content_id'),
            metadata=kwargs.get('metadata')
        )

"""

In past month:
    - total number of push: BitbucketActivity.objects.filter(type_of_activity='push', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).count()
    - total number of pull request: BitbucketActivity.objects.filter(type_of_activity='pullrequest', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id').count()
    - BitbucketActivity.objects.filter(type_of_activity='pullrequest', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id')
    - Information of all pr [(pr.content_id, pr.state) for pr in BitbucketActivity.objects.filter(type_of_activity='pullrequest', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id')]
    - merged prs count: BitbucketActivity.objects.filter(type_of_activity='pullrequest', state='M', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id').count()
    - open prs count: BitbucketActivity.objects.filter(type_of_activity='pullrequest', state='O', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id').count()
    - number of comments: BitbucketActivity.objects.filter(type_of_activity='pullrequest', sub_type='comment', created_at__range=((datetime.datetime.now() - datetime.timedelta(days=30)), datetime.datetime.now())).distinct('content_id').count()

"""