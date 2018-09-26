import json
from abc import ABC
import logging

from bitbucket import constants

logger = logging.getLogger(__name__)


class BaseData(ABC):

    def __init__(self):

        self.processed_response = {
            'type_of_activity': None,
            'sub_type': None,
            'author_username': None,
            'author_display_name': None,
            'project_full_name': None,
            'state': None,
            'content_id': None,
            'metadata': None
        }

    def set_data(self, data):
        self.processed_response = {
            'author_username': data.get(constants.ACTOR).get(constants.USERNAME),
            'author_display_name': data.get(constants.ACTOR).get(constants.DISPLAY_NAME),
            'project_full_name': data.get(constants.REPOSITORY).get(constants.FULL_NAME),
        }


class PRBase(BaseData):

    def set_data(self, data):
        super(PRBase, self).set_data(data)
        self.processed_response.update({
            'type_of_activity': constants.PULL_REQUEST,
            'content_id': data.get(constants.PULL_REQUEST).get(constants.ID)
        })


class Push(BaseData):

    def set_data(self, data):
        self.processed_response = {
            'type_of_activity': constants.PUSH,
            'sub_type': None,
            'author_username': data.get(constants.ACTOR).get(constants.USERNAME),
            'author_display_name': data.get(constants.ACTOR).get(constants.DISPLAY_NAME),
            'project_full_name': data.get(constants.REPOSITORY).get(constants.FULL_NAME),
            'state': None,
            'content_id': None,
            'metadata': {
                'summary': data.get(constants.PUSH).get(constants.CHANGES)[constants.ZERO].\
                    get(constants.NEW).get(constants.TARGET).\
                    get(constants.SUMMARY).get(constants.RAW),
                'hash': data.get(constants.PUSH).get(constants.CHANGES)[constants.ZERO].\
                    get(constants.NEW).get(constants.TARGET).get(constants.HASH),
                'date': data.get(constants.PUSH).get(constants.CHANGES)[constants.ZERO].\
                    get(constants.NEW).get(constants.TARGET).get(constants.DATE),
                'message': data.get(constants.PUSH).get(constants.CHANGES)[constants.ZERO].\
                    get(constants.NEW).get(constants.TARGET).get(constants.MESSAGE)
            } if data.get(constants.PUSH).get(constants.CHANGES)[constants.ZERO].\
                    get(constants.NEW) else {}
        }
        return self.processed_response


class PRGeneric(PRBase):

    def set_data(self, data):
        super(PRGeneric, self).set_data(data)
        self.processed_response.update({
            'sub_type': constants.CREATED,
            'state': constants.STATE_OPTIONS.get(data.get(constants.PULL_REQUEST)\
                    .get(constants.STATE)),
            'metadata': {
                'title': data.get(constants.PULL_REQUEST).get(constants.TITLE),
                'dstn_branch': data.get(constants.PULL_REQUEST).get(constants.DESTINATION) \
                    .get(constants.BRANCH).get(constants.NAME),
                'dstn_repo': data.get(constants.PULL_REQUEST).get(constants.DESTINATION) \
                    .get(constants.REPOSITORY).get(constants.FULL_NAME),
                'src_branch': data.get(constants.PULL_REQUEST).get(constants.SOURCE) \
                    .get(constants.BRANCH).get(constants.NAME),
                'reviewers': [r.get(constants.USERNAME) for r in data.get(constants.PULL_REQUEST). \
                    get(constants.REVIEWERS)],
                'created_on': data.get(constants.PULL_REQUEST).get(constants.CREATED_ON),
                'closed_by': data.get(constants.PULL_REQUEST).get(constants.CLOSED_BY).get(constants.USERNAME) \
                    if data.get(constants.PULL_REQUEST).get(constants.CLOSED_BY) else None
            }
        })
        return self.processed_response


class PRComment(PRBase):

    def set_data(self, data):
        super(PRComment, self).set_data(data)
        self.processed_response.update({
            'sub_type': constants.COMMENT,
            'state': constants.STATE_OPTIONS.get(data.get(constants.PULL_REQUEST)\
                    .get(constants.STATE)),
            'metadata': {
                'content': data.get(constants.COMMENT).get(constants.CONTENT).\
                    get(constants.RAW),
                'created_on': data.get(constants.COMMENT).get(constants.CREATED_ON),
                'id': data.get(constants.COMMENT).get(constants.ID)
            }
        })
        return self.processed_response


class PRApproval(PRBase):

    def set_data(self, data):
        super(PRApproval, self).set_data(data)
        self.processed_response.update({
            'sub_type': constants.APPROVAL,
            'state': constants.STATE_OPTIONS.get(data.get(constants.PULL_REQUEST)\
                    .get(constants.STATE)),
            'metadata': {
                'datetime': data.get(constants.APPROVAL).get(constants.DATE),
                'participants': [{
                    'approved': ob.get(constants.APPROVED),
                    'date': ob.get(constants.PARTICIPATED_ON),
                    'username': ob.get(constants.USER).get(constants.USERNAME)
                } for ob in data.get(constants.PULL_REQUEST).get(constants.PARTICIPANTS)]
            }
        })
        return self.processed_response


class ProcessDataFactory:

    def check_type(self, json_response_keys):
        for _type in constants.API_TYPES:
            if _type in json_response_keys:
                return _type
        return None

    def get_processed_data(self, bitbucket_response):
        # Convert the bitbucket byte response to json
        json_response = json.loads(bitbucket_response.decode('utf-8'))

        # check for response type
        api_type = self.check_type(json_response.keys())
        # Create class based on type of api
        if api_type == constants.PUSH:
            process_data = Push()
        elif api_type == constants.COMMENT:
            process_data = PRComment()
        elif api_type == constants.APPROVAL:
            process_data = PRApproval()
        elif api_type == constants.PULL_REQUEST:
            process_data = PRGeneric()

        try:
            processed_data = process_data.set_data(json_response)
        except Exception as error:
            logger.error('Bitbucket data processing error, please find data: %s' % str(json_response))
            raise Exception('Error saving data !!')

        return processed_data
