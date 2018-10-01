from django.views import View
from django.http import JsonResponse


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

