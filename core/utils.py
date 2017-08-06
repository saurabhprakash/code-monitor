import datetime
import json

from django.template import loader
from django.core.mail import send_mail
from django.conf import settings

from core.models import CodeStandardData
from core.constants import MESSAGE, SUBJECT

class PastDayReport(object):
    """Generate past day report
    """

    def query(self):
        queryset = CodeStandardData.objects.filter(created_at__range=((datetime.datetime.now() - \
            datetime.timedelta(days=1)),datetime.datetime.now()))
        return queryset

    def process_queryset_to_fetch_unique(self, qs):
        """"process query set to generate unique response for single project"""
        response = {}
        for q in qs:
            if (q.project not in response) or (q.project in response and \
                response[q.project].created_at < q.created_at) :
                response[q.project] = q
        return response

    def prepare_response(self, response):
        """"takes unique_response and creates response as required by frontend"""
        scores = []
        errors = []
        convention = []
        warnings = []
        for r in response.values():
            scores.append(r.score)
            metadata = json.loads(r.metadata)
            errors.append(metadata['errors'])
            convention.append(metadata['convention'])
            warnings.append(metadata['warning'])
        results = {
            'projects': response.keys(),
            'scores': scores,
            'errors': errors,
            'convention': convention,
            'warnings': warnings
        }
        return results

    def send_status_report(self):
        report = self.generate()
        print ('report=', report)
        html_message = loader.render_to_string('report.html', report)
        send_mail(SUBJECT, MESSAGE, settings.FROM, settings.TO, fail_silently=False, 
            html_message=html_message)
        print ('complete')
        
    def generate(self):
        qs = self.query()
        unique_response = self.process_queryset_to_fetch_unique(qs)
        return self.prepare_response(unique_response)
