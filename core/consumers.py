import json

from channels import Group

from core import models as core_models

def ws_connect(message):
    Group('socket_report').add(message.reply_channel)
    Group('socket_report').send({
        'text': json.dumps(core_models.CommitData.objects.commits_update())
    })


def ws_disconnect(message):
    Group('socket_report').discard(message.reply_channel)
