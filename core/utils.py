import datetime
import json
import logging
import traceback

from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

from core import models
from core.constants import MESSAGE, SUBJECT

logger = logging.getLogger(__name__)


class PastDayReport(object):
    """Generate past day report
    """

    def query(self):
        queryset = models.CodeStandardData.objects.filter(created_at__range=((datetime.datetime.now() - \
            datetime.timedelta(days=1)),datetime.datetime.now()))
        return queryset

    def process_queryset_to_fetch_unique(self, qs):
        """"process query set to generate unique response for single project"""
        response = {}
        for q in qs:
            if (q.project not in response) or (q.project in response and \
                    response[q.project].created_at < q.created_at):
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
        html_message = loader.render_to_string('report.html', report)
        send_mail(SUBJECT, MESSAGE, settings.FROM, settings.TO, fail_silently=False, 
            html_message=html_message)

    def generate(self):
        qs = self.query()
        unique_response = self.process_queryset_to_fetch_unique(qs)
        return self.prepare_response(unique_response)


class DashboardReports:

    def commit_data_stats(self, days=7):
        """:returns weekly data for commit data models
        """
        end_date = datetime.datetime.today()
        start_date = end_date + datetime.timedelta(days=-(days))
        return models.CommitData.objects.ranged_query(start_date, end_date)

    def processed_commit_data_stats(self, days=7):
        """:returns weekly data for commit data models
        """
        end_date = datetime.datetime.today()
        start_date = end_date + datetime.timedelta(days=-(days))
        return models.ProcessedCommitData.objects.ranged_query(start_date, end_date)

    def create_response(self, commit_data_weekly_stats, processed_commit_data_weekly_stats):
        """gets the django query set and creates response as per user"""

        response = {}

        def get_int(value):
            return value if isinstance(value, int) else 0

        def calculate_lines_contribution(change_details, parent_change_details, update=True):
            """calculates the number of lines added/removed in codebase
            """
            response = parent_change_details if parent_change_details else {}
            for detail in change_details:
                try:
                    if update:
                        response['lines_added'] = parent_change_details['lines_added'] + get_int(detail['lines_added'])
                        response['lines_removed'] = parent_change_details['lines_removed'] + \
                                                    get_int(detail['lines_removed'])
                    else:
                        response['lines_added'] = get_int(detail['lines_added'])
                        response['lines_removed'] = get_int(detail['lines_removed'])
                except:
                    logger.error('Error calculate_lines_contribution: %s' % traceback.print_exc())
            return response

        # Process commit data(model: CommitData)
        for data in commit_data_weekly_stats:
            if data.user.id in response:
                response[data.user.id]['commit_count'] += 1
                response[data.user.id]['lines'] = calculate_lines_contribution(data.change_details,
                    response[data.user.id]['lines'], update=True)
            else:
                response[data.user.id] = {
                    'commit_count': 1,
                    'name': '%s %s' % (data.user.first_name, data.user.last_name),
                    'lines': calculate_lines_contribution(data.change_details, None, update=False),
                    # TODO: This will have bugs for user working on multiple projects
                    'project': data.project,
                    'issues': {}
                }

        # Process ProcessedCommitData model entries for weekly data
        for data in processed_commit_data_weekly_stats:
            if data.commit_ref.user_id in response:
                if response[data.commit_ref.user_id].get('issues') and data.language in \
                        response[data.commit_ref.user_id]['issues']:
                    response[data.commit_ref.user_id]['issues'][data.language] += data.issues_count
                else:
                    if 'issues' in response[data.commit_ref.user_id]:
                        response[data.commit_ref.user_id]['issues'][data.language] = data.issues_count
                    else:
                        response[data.commit_ref.user_id]['issues'] = {
                            data.language: data.issues_count
                        }
        return response

    def reports(self, week=1):
        """
        :return:
        Call commit_data_stats and processed_commit_data_stats with week*7 
        as those function takes number of days
        """
        commit_data_weekly_stats = self.commit_data_stats(week*7)
        processed_commit_data_weekly_stats = self.processed_commit_data_stats(week*7)
        weekly_report = self.create_response(commit_data_weekly_stats, processed_commit_data_weekly_stats)
        return {
            'weekly_report': weekly_report,
            'users': User.objects.only('first_name', 'last_name').filter(is_active=True, is_staff=False)
        }


class IssueReports:

    @staticmethod
    def weekly_user_issue_report(user_id):
        end_date = datetime.datetime.today()
        start_date = end_date + datetime.timedelta(days=-7)
        if user_id:
            return {
                'issues': models.CommitData.objects.get_commits_with_issues_for_user(\
                    user_id, start_date, end_date)
            }
        return {'error': True, 'message': 'No user id found'}


class UserData:
    
    @staticmethod
    def create_user_report(user_id, weeks):
        return {
            'number_of_commits': models.CommitData.objects.\
                commit_counts_for_user_in_given_weeks(user_id, weeks),
        }


class CompareUser:
    
    @staticmethod
    def compare(user_id_1, user_id_2, weeks):
        return {
            'user1': UserData.create_user_report(user_id_1, int(weeks)),
            'user2': UserData.create_user_report(user_id_2, int(weeks))
        }


class MailReport:
    
    @staticmethod
    def get_users_with_no_commits(user_ids):
        """returns users with no commits for a given time range
            user_ids: is the list of users who have commit entries
        """
        return User.objects.exclude(id__in=user_ids)

    @staticmethod
    def prepare_report(r_range='weekly'):
        dr = DashboardReports()
        report = dr.reports()
        response = {
            'get_users_with_no_commits': MailReport.get_users_with_no_commits\
                (report.get('weekly_report').get('user_ids_in_report')),
            
        }
        print (response)


class LeadReports:

    @staticmethod
    def get_lead_report(weeks=1):
        """gets number of user with no commits over given number of weeks
        """
        dr = DashboardReports()
        return {
            'no_commit_users': models.CommitData.objects.get_users_with_no_commit_n_weeks(weeks),
            'commit_report': dr.reports(weeks)
        }
