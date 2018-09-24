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
