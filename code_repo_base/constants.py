PUSH = 'push'
COMMENT = 'comment'
PULL_REQUEST = 'pullrequest'
APPROVAL = 'approval'


# This order is important as 'pullrequest'/PULL_REQUEST_CREATION is present with all approval
# and comment requests, so when we check this in last we
API_TYPES = [COMMENT, PUSH, APPROVAL, PULL_REQUEST]

ACTOR = 'actor'
USERNAME = 'username'
USER = 'user'
DISPLAY_NAME = 'display_name'
REPOSITORY = 'repository'
FULL_NAME = 'full_name'
CHANGES = 'changes'
ZERO = 0
NEW = 'new'
SUMMARY = 'summary'
RAW = 'raw'
TARGET = 'target'
HASH = 'hash'
DATE = 'date'
MESSAGE = 'message'
TARGET = 'target'
DATE = 'date'
CREATED = 'created'
STATE = 'state'
ID = 'id'
DESTINATION = 'destination'
TITLE = 'title'
BRANCH = 'branch'
NAME = 'name'
SOURCE = 'source'
CREATED_ON = 'created_on'
REVIEWERS = 'reviewers'
STATE_OPTIONS = {
    'OPEN': 'O',
    'MERGED': 'M',
    'DECLINED': 'D'
}
CONTENT = 'content'
TYPE = 'type'
PARTICIPANTS = 'participants'
APPROVED = 'approved'
PARTICIPATED_ON = 'participated_on'
CLOSED_BY = 'closed_by'
DEFAULT_NUMBER_OF_DAYS = 30
TIME_FORMAT_ERROR = 'Time format mismatch'
