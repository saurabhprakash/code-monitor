import json

from channels import Group

from core import models as core_models
from core import constants

def ws_connect(message):
    Group(constants.INSTANT_COMMIT_REPORT).add(message.reply_channel)
    Group(constants.INSTANT_COMMIT_REPORT).send({
        'text': json.dumps(core_models.CommitData.objects.commits_update())
    })


def ws_disconnect(message):
    Group(constants.INSTANT_COMMIT_REPORT).discard(message.reply_channel)
