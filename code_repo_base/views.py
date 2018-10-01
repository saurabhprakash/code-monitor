from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from code_repo_base import models, utils

decorators = [csrf_exempt, ]


@method_decorator(decorators, name='dispatch')
class WebhookDataView(View):

    def post(self, request):
        # Process required request data and get information to be saved in database
        pd = utils.ProcessDataFactory()
        data = pd.get_processed_data(request.body)
        models.CodeRepoDataBase.objects.create_entry(**data)
        return JsonResponse({'message': 'Data added successfully.'})



class ReportsView(View):
    """
        For a given time range(default 1 week)
            Overall
                - Total number of PR raised
                - Total number of PR merged + declined
                - Total number of PRs reviewed + non-reviewed
                - Total number if push to repos
                - Total number of comments in PR
            Project Specific Data
                - Total number of PR raised specific to project
                - Total number of PR "merged + declined" specific to project
                - Total number of pushes specific to project
                - Total number of PR reviewed specific to project + non-reviewed
                - Total number of comments specific to project
            Individual Specific data:
                - User with most number of reviews done
                - User with most number of pull request
                - User with most number of pushes

            Weekend work

    """
    def get(self, request):

        return JsonResponse({})

