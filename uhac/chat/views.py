# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic
import requests
import json
from pprint import pprint
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# Create your views here.
# def index(request):
#     return HttpResponse('<h1>Hello Test</h1>')

# fj_user_id = '345435105819111'

count_vec = CountVectorizer()
normalized_text = TfidfTransformer()

user_ids = {
'Rommel': "1280262622045342",
'Francisc':"1173757599378036",
}

training_Set = [
'Hi',
'Good Day',
'Arrived',
'Walked In',
'I Just Arrived',
'I want one mocha frapuccino',
"nothing thanks.",
"I'm back",
"yes",
"no",
"I'm right here",
"no, is there anything new to the menu?",
"clicked the beverage",
"ah yes. can I have the Menu again?",
"ok,thanks.",
"okay",
"Nothing Thanks."
]

labels = [
'Good Day, How can Romeo help you today?',
'Nice to see you again',
'Hi, What can I get for you today, sir?',
'Good morning! Can I take your order?',
"Hi Mel! Here's our Menu, you can now order. To order, Just click the item you are going to order. And the bill will go straight to your bank account.",
"Ok mel. We recieved your order. Your order will be served to you within 3 minutes. Is there anything you want to add?",
"ok sir, have a Good Day! Come Again.",
"Welcome back Mel. Do you want the usual?",
"ok. your order will be ready in 3 minutes. Have a Good Day!, is there anthing else?",
"ok sir, have a Good Day! Come Again.",
"Welcome back mel. Do you want the usual?",
"ok sir. Today's special is Iced Chai Tea Latte and Cinnamon Bun. Click the item that you want to order and it will be served to you",
"Ok mel. We recieved your order. Your order will be served to you within 3 minutes. Is there anything you want to add?",
"ok sir, here's the menu just the same process to add order.",
"ok sir, we recieved your additional order, just wait for a few minutes and your order will be ready.",
"Is there anything else?",
"Thank you Sir, Have a Good Day! Come Again."
]

trained = count_vec.fit_transform(training_Set)
normal = normalized_text.fit_transform(trained)
clf = RandomForestClassifier(normal, labels)

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
        print("Incoming")
        print(incoming_message)
        print("END")
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(message)

                    answer = clf.predict(message['message']['text'])

                    post_facebook_messages(message['sender']['id'],str(answer))

                    # post_facebook_messages(message['sender']['id'],message['message']['text'])
                    # post_facebook_messages(mel_user_id,message['message']['text'])

        return HttpResponse()


class hardware(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        hardmessage = json.loads(self.request.body.decode('utf-8'))
        pprint(self.request.body.decode('utf-8'))
        pprint('---')
        pprint(hardmessage)
        message = hardmessage['body']
        pprint(message)
        if message == 'Rommel':
            answer = clf.predict(str(labels[random.randint(0, len(labels)-1)]))
            post_facebook_messages(user_ids['Francisc'], str(answer))
        return HttpResponse()

def randome(fbid, received_messages):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    response_msg = json.dumps({"recipient": {"id":fbid},"message":{"text":received_messages}})
    print('-----')
    print(response_msg)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg, )
    pprint(status.json())

def post_facebook_messages(fbid, received_messages):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    response_msg = json.dumps({"recipient": {"id":fbid},"message":{"text":received_messages}})
    print('-----')
    print(response_msg)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg, )
    pprint(status.json())


def cam_saw_client(fbid, message_to_pass):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    response_msg = json.dumps({"recipient"})
    pass

# def
