from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from bitbucket import utils, models

decorators = [csrf_exempt, ]


@method_decorator(decorators, name='dispatch')
class BitbucketView(View):

    def post(self, request):
        # Process required request data and get information to be saved in database
        pd = utils.ProcessDataFactory()
        data = pd.get_processed_data(request.body)
        models.BitbucketActivity.objects.create_entry(**data)
        return JsonResponse({'message': 'Data added successfully.'})
