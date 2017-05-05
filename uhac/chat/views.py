# coding=utf-8

#Django Imports
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic
import requests
import json
from pprint import pprint
import random
import urllib
import os
import time

#Scikit Learn Imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


#PIL Image Imports and Data Science Imports
from PIL import Image
import pandas as pd
import numpy as np

#Facebook Webhook Token
verify_token = '5244680129'

#Facebook Page Token
page_access_token = 'EAAI7N9RGaL4BAFgt5zRVnffcuV9MuePhO731FX6LA5Y23w0GX7C4IduaUdJ382cgosZBPZANxnZBZALM2ZAYAJq1Yk8zVWDIkIsObhTCkb5sEY6WDSkX4sPp4qjQMHyhZBw3VZAXB2c5ZBcXuOyl3nTOzC2M2xRndEk0H04OMxq5ZCwZDZD'



#Scikit Learn Text Feature Extraction Tools
count_vec = CountVectorizer()
normalized_text = TfidfTransformer()

#Waiting for Payment Image
# global wait_image
wait_image = 0
STANDARD_SIZE = (512,512)
#Start Initial Training
pca = PCA(n_components=9)
customer_names = ['fj','shella','rommel','cha','jay','jhoffer','paul','shaneh','william']
customer_test = []
#PCA - Eigenfaces Functions
def img_to_matrix(filename, STANDARD_SIZE, verbose=False):
    img = Image.open(filename)
    if verbose==True:
        print("Changin size from %s to %s" % (str(img.size), str(STANDARD_SIZE)))
    img = img.resize(STANDARD_SIZE)
    img = list(img.getdata())
    img = map(list, img)
    img = np.array(img)
    return img

def flatten_image(img):
    s = img.shape[0] * img.shape[1]
    img_wide = img.reshape(1,s)
    return img_wide[0]

def create_name(split_name, namepool):
    names = split_name.split('/')[-1]
    for namep in namepool:
        if namep in names:
            name = namep
            print(name)
    return name

def pca_classifier(STANDARD_SIZE, verbose=False):
    global customer_names
    global pca
    global customer_test
    PROJECT_ROOT  = os.path.abspath(os.path.dirname('__file__')) + "/training_set"
    if verbose==True:
        print(PROJECT_ROOT)
    images = [PROJECT_ROOT+"/"+f for f in os.listdir(PROJECT_ROOT)]

    if verbose==True:
        print(len(images))
    labelsPCA = [create_name(creator, customer_names) for creator in images]
    if verbose==True:
        print(len(labelsPCA))
    data = []
    counter = 0
    for image in images:
        print(image)
        img = img_to_matrix(image, STANDARD_SIZE)
        img = flatten_image(img)
        data.append(img)
        counter += 1
        if verbose==True:
            print("appending data: " + str(counter))
    train_x = np.array(data)

    X = pca.fit_transform(train_x)
    TEST_ROOT = os.path.abspath(os.path.dirname('__file__')) + "/test_set"
    if (verbose==True):
        print(TEST_ROOT)
    test_images = [TEST_ROOT+"/"+f for f in os.listdir(TEST_ROOT)]
    if verbose==True:
        print(len(test_images))
    test_data = []
    counter = 0
    for timage in test_images:
        print(timage)
        img = img_to_matrix(timage, STANDARD_SIZE)
        img = flatten_image(img)
        test_data.append(img)
        counter += 1
        if verbose==True:
            print("appending test data: " + str(counter))

    customer_test = [create_name(creator, customer_names) for creator in test_images]
    test_datas = np.array(test_data)
    transformed = pca.transform(test_datas)
    # clf = KNeighborsClassifier().fit(X, labelsPCA)
    clf = RandomForestClassifier().fit(X, labelsPCA)
    pred = clf.predict(transformed)
    # clf = classifier.fit(X, labelsPCA)
    pscore = accuracy_score(pred, customer_test)
    print("\n\n--------------------PSCORE------------------------\n\n")
    print(pscore)
    print("\n\n--------------------PSCORE------------------------\n\n")
    return clf

def pca_pred(classifier, prediction, std_size, verbose=False):
    global pca
    print('---entered image prediction-----')
    PREDPATH = os.path.abspath(os.path.dirname('__file__'))
    prediction_location = PREDPATH + "/" + prediction
    img = img_to_matrix(prediction_location, std_size)
    img = flatten_image(img)
    prediction_data = np.array(img)

    pcaPred = pca.transform(prediction_data)
    pred = classifier.predict(pcaPred)
    print("\n\n------------PREDICTING---------------\n\n")
    print(str(pred[0]))
    print("\n\n------------PREDICTING---------------\n\n")
    return pred[0]


clf = pca_classifier(STANDARD_SIZE, True)

class index(generic.View):

    def __init__(self):
        self.STANDARD_SIZE = (512,512)

        #Image Counter for Account Creation
        # self.count_image = 0
        # self.knn = KNeighborsClassifier()
        # self.clf = pca_classifier(self.knn, self.STANDARD_SIZE, True)

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '5244680129':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, Invalid Token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        global wait_image
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        print("\n-------------------Incoming---------------------------\n")
        print(incoming_message)
        print("\n---------------------END------------------------------\n")
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                pprint(message)
                if ('message' not in message):
                    print("Watermark spotted")
                elif ('text' in message['message']) and (message['message']['text']=="Create"):
                    print('-----ENTERED CREATE----')
                    #Initiate Create Account
                    pass
                elif ('text' in message['message']) and (wait_image==0) and (message['message']['text']!="Pay") and (message['message']['text']!="Create") and ("attachments" not in message['message']):
                    print('-----ENTERED Chatbot----')
                    #Initiate chatbot
                    chatbot(message['message']['text'], message['sender']['id'], training_Set, labels, True)

                elif ('text' in message['message']) and (message['message']['text']=="Pay") and ("attachments" not in message['message']):
                    print('-----ENTERED pay----')
                    #Initiate payment
                    wait_image = 1
                    print(wait_image)
                    pay(message['sender']['id'],True)

                elif ('text' in message['message']) and (wait_image==1) and ('attachments' not in message['message']):
                    print('-----ENTERED image1----')
                    amount = message['message']['text']
                    wait_image = 2
                    print(wait_image)
                    pay_ask_image(message['sender']['id'], True)

                elif (wait_image==2) and ('attachments' in message['message']):
                    print('-----ENTERED image2----')
                    payment_image(message["sender"]["id"], message["message"]["attachments"] ,True)

                # elif ('watermark' in message['read']) or ('watermark' in message['delivery']):
                #     print('--------------------------WATERMARK------------------------')
                #     print('Received Watermark no more need to send information')

                elif (wait_image!=2) and ('attachments' in message['message']):
                    senderid = message["sender"]["id"]
                    print("--senderid----")
                    print(str(senderid))
                    for attached in message["message"]["attachments"]:
                        print("--entered attached--")
                        imageurl = attached["payload"]["url"]
                        # Image Received
                        urllib.urlretrieve(imageurl,"ftest.jpg")
                        post_facebook_messages(message['sender']['id'],str("received image"))


                else:
                    print("=================================None")
                    post_facebook_messages(message['sender']['id'],str("none"))

        return HttpResponse()





def chatbot(predict_message, sender_id, training_Set, labels, verbose):
    if verbose==True:
        print("\n----Entered Chatbot-----\n")

    #Created a model to fit the training_set
    trained = count_vec.fit_transform(training_Set)

    #Normalizing the trained model
    normal = normalized_text.fit_transform(trained)

    #Created a Random Forest Classifer and fitted the normal and labels dataset
    clf = RandomForestClassifier().fit(normal, labels)
    docs_new = [predict_message]
    X_new_counts = count_vec.transform(docs_new)
    X_new_tfidf = normalized_text.transform(X_new_counts)
    x = clf.predict(X_new_tfidf)
    post_facebook_messages(sender_id,str(x[0]))
    return

def pay(sender_id,verbose=False):
    if verbose==True:
        print("\n--------Entered Payment Initiation--------\n")
    prompt = "Thanks for using Romeo. Please type the amount to be payed: "
    post_facebook_messages(sender_id,str(prompt))
    return

def pay_ask_image(sender_id, verbose=False):
    if verbose==True:
        print("\n--------Entered Payment Image Init--------\n")
    prompt = "You can now send the persons account image: "
    post_facebook_messages(sender_id, str(prompt))
    return

def payment_image(sender_id, attachment_image, verbose=False):
    global clf
    global STANDARD_SIZE
    if verbose==True:
        print("\n--------Entered Payment Image-------\n")
    for attached in attachment_image:
        if verbose==True:
            print("\n-----Entered Attaachment------\n")
        imageurl = str(attached["payload"]["url"])

        #Receive Image
        image_filename = "customer.jpg"
        urllib.urlretrieve(imageurl, image_filename)
    prompt = "Image Received!. Processing Transaction"
    post_facebook_messages(sender_id, str(prompt))
    image_name = pca_pred(clf, image_filename, STANDARD_SIZE, True)
    post_facebook_messages(sender_id, str(image_name))
    return

#------------------------------- Original Code ------


#
# user_ids = {
# 'Rommel': "1280262622045342",
# 'Francisc':"1173757599378036",
# }

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
    "Checkout"
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

# trained = count_vec.fit_transform(training_Set)
# normal = normalized_text.fit_transform(trained)
# clf = RandomForestClassifier().fit(normal, labels)
#
# x = TfidfTransformer()

# downloadImage = urllib.URLopener()



# class index(generic.View):
#
#     def get(self, request, *args, **kwargs):
#         if self.request.GET['hub.verify_token'] == '5244680129':
#             return HttpResponse(self.request.GET['hub.challenge'])
#         else:
#             return HttpResponse('Error, Invalid Token')
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return generic.View.dispatch(self, request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         incoming_message = json.loads(self.request.body.decode('utf-8'))
#         print("\n-------------------Incoming---------------------------")
#         print(incoming_message)
#         print("\n---------------------END------------------------------")
#         for entry in incoming_message['entry']:
#             for message in entry['messaging']:
#                 if ('message' in message) and ('attachments' not in message['message']):
#                     print("----Entered Message-----")
#                     pprint(message)
#
#                     #Train using the count_vec method
#                     trained = count_vec.fit_transform(training_Set)
#
#                     #Normalizing the trained model
#                     normal = normalized_text.fit_transform(trained)
#
#                     clf = RandomForestClassifier().fit(normal, labels)
#                     docs_new = [message['message']['text']]
#                     X_new_counts = count_vec.transform(docs_new)
#                     X_new_tfidf = normalized_text.transform(X_new_counts)
#                     x = clf.predict(X_new_tfidf)
#                     checking_customized = " "
#                     post_facebook_messages(message['sender']['id'],str(x[0]))
#
#                 elif ('message' in message) and ('attachments' in message['message']):
#                     print("\n-----------Entered Attachment-------------------------")
#                     pprint(message)
#                     senderid = message["sender"]["id"]
#                     print("--senderid----")
#                     print(str(senderid))
#                     for attached in message["message"]["attachments"]:
#                         print("--entered attached--")
#                         imageurl = attached["payload"]["url"]
#
#                         # Image Received
#                         urllib.urlretrieve(imageurl,"test.jpg")
#
#                         return_image(senderid, imageurl)
#                     print("\n-----------Leaving Attachment-------------------------")
#         print("\n---------------------END OF CONVERSATION---------------")
#         return HttpResponse()


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
            X_new_counts = count_vec.transform([training_Set[random.randint(0, len(training_Set)-1)]])

            X_new_tfidf = normalized_text.transform(X_new_counts)
            x = clf.predict(X_new_tfidf)
            # answer = clf.predict()
            post_facebook_messages(user_ids['Francisc'], str(x[0]))
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

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())
    return

def post_facebook_messages_with_button(fbid, received_messages):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    response_msg = json.dumps(
        {
            "recipient": {"id":fbid},
            "message":{
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":received_messages,
                        "buttons":[
                            {
                                "type":"web_url",
                                "url":"https://2a44f461.ngrok.io/home/",
                                "title":"LITE PLAN 1899"
                            },
                            {
                                "type":"postback",
                                "title":"I want to inquire",
                                "payload":"POWER PLUS PLAN 2899"
                            },
                            {
                                "type":"postback",
                                "title":"Power Plus Plan 3500",
                                "payload":"POWER PLUS PLAN 3500"
                            }
                        ]
                    }
                }
            } })
    print('-----')
    print(response_msg)
    # files = {'file': open('./2.jpeg', 'rb')}

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg, )
    pprint(status.json())

def return_image(fbid, received_image_link):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    response_msg = json.dumps(
    {
        "recipient": {"id":fbid},
        "message":{
            "attachment":[
            {
                "type": "image",
                "payload": {
                    "url": received_image_link
                }
            }]
        }
    })

    print('-----')
    print(response_msg)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg, )
    pprint(status.json())
