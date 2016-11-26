# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic
import requests
import json
from pprint import pprint

# Create your views here.
# def index(request):
#     return HttpResponse('<h1>Hello Test</h1>')

# fj_user_id = '345435105819111'


user_ids = {
'Rommel': "1280262622045342"
}

training_Set = [
'Hi',
]

test_Set = [
'Good Day, How can Romeo help you today?',
]

verify_token = '5244680129'
page_access_token = 'EAAI7N9RGaL4BAFgt5zRVnffcuV9MuePhO731FX6LA5Y23w0GX7C4IduaUdJ382cgosZBPZANxnZBZALM2ZAYAJq1Yk8zVWDIkIsObhTCkb5sEY6WDSkX4sPp4qjQMHyhZBw3VZAXB2c5ZBcXuOyl3nTOzC2M2xRndEk0H04OMxq5ZCwZDZD'

class index(generic.View):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '5244680129':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, Invalid Token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(message)
                    post_facebook_messages(message['sender']['id'],message['message']['text'])
                    # post_facebook_messages(mel_user_id,message['message']['text'])

        return HttpResponse()

def post_facebook_messages(fbid, received_messages):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    response_msg = json.dumps({"recipient": {"id":fbid},"message":{"text":received_messages}})
    print('-----')
    print(response_msg)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg, )
    pprint(status.json())
