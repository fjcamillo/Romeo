import requests
import json
# payload = {u'entry': [
#                         {u'messaging': [
#                                         {u'timestamp': 1480197139793,
#                                         u'message':
#                                             {u'text': u'Arrived',
#                                             u'is_echo': True,
#                                             u'app_id': 628060924045502,
#                                             u'seq': 404,
#                                             u'mid': u'mid.1480197139793:82ecb50989'},
#                                             u'recipient': {u'id': u'1173757599378036'},
#                                             u'sender': {u'id': u'345435105819111'}}],
#                                         u'id': u'345435105819111',
#                                         u'time': 1480197140165}],
#                                         u'object': u'page'}

# payload = {u'entry':
#         [{u'messaging': [{u'read': {u'seq': 413, u'watermark': 1480197939810}, u'timestamp': 1480197940174, u'recipient': {u'id': u'345435105819111'}, u'sender': {u'id': u'1173757599378036'}}], u'id': u'345435105819111', u'time': 1480197941320}], u'object': u'page'}

payload = {'body': 'Francisc'}
payload = json.dumps(payload)

# {u'message': {u'app_id': 628060924045502,
#               u'is_echo': True,
#               u'mid': u'mid.1480197139793:82ecb50989',
#               u'seq': 404,
#               u'text': u'ol'},
#  u'recipient': {u'id': u'1173757599378036'},
#  u'sender': {u'id': u'345435105819111'},
#  u'timestamp': 1480197139793}


r = requests.post("https://04e27ba9.ngrok.io/chat/hardware/", data=payload)
# response = r.json()
# print response
