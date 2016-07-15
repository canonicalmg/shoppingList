from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.template.defaultfilters import slugify
from .models import list, listEntry
#from twilio.rest import TwilioRestClient
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def incomingSMS(request):
    if request.method == "POST":
        #if phoneNumber not recognized, prompt to create new account or associate # with account

        #if recognized, parse message
            #create list "listname"
            #get list "listname"
            #clear list "listname"
            #add 3 eggs to "listname"

        # print "all =", request
        # print "PRINTING ", request.body
        # currentUser = User.objects.get(username="marcusg")
        # currentProfile = profile.objects.get(user=currentUser)
        # content = request.POST.get('Body', '') #action=wallpost, body="this is the body text"
        # content = json.loads(content)
        # action = content['action']
        # body = content['body']
        # if action == "wallpost":
        #     currentUser = User.objects.get(username="SMSBot")
        #     newPost = wallPost(postSender=currentUser, postReceiver=currentUser, content=body)
        #     newPost.save()
        # if action == "postuser":
        #     sendTo = User.objects.get(username=content['user'])
        #     currentUser = User.objects.get(username="SMSBot")
        #     newPost = wallPost(postSender=currentUser, postReceiver=sendTo, content=body)
        #     newPost.save()
        # #currentProfile.aboutMe = action + "%%" + body
        # currentProfile.save()
        return HttpResponse("done")

def signUpLogIn(request):
    if request.user.is_authenticated():
        #send them to /home
        return HttpResponseRedirect("home")
    else:
        template = loader.get_template('headerLogin.html')
        context = {

        }
        return HttpResponse(template.render(context, request))
        #render(request, 'headerLogin.html', context)

def headerSignIn(request):
    if request.is_ajax():
        if request.method == "POST":
            data = request.POST.getlist("data[]")
            user = authenticate(username=str(data[0]), password=str(data[1]))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("return this string")
            else:
                return HttpResponse("Does not match")

def home(request, string):
    if request.user.is_authenticated():
        template = loader.get_template('home.html')
        allLists = list.objects.filter(owner=request.user)
        currentList = list.objects.get(owner=request.user, slug=string)
        listItems = listEntry.objects.filter(listActual=currentList)
        context = {
            "currentListName": currentList.listName,
            "currentSlug": string,
            "listItems": listItems,
            "lists": allLists
        }
        return HttpResponse(template.render(context, request))
    else:
        #login
        return HttpResponseRedirect("/")

def addItemShoppingCart(request):
    if request.is_ajax():
        if request.method == "POST":
            data = request.POST.getlist("data[]")
            itemName = data[0]
            shopName = data[1]
            quantity = data[2]
            price = data[3]
            slug = data[4]

            currentList = list.objects.get(owner=request.user, slug=slug) #change this later
            entry = listEntry(itemName=itemName, shopName=shopName, quantity=quantity, price=price, listActual=currentList)
            entry.save()

            return HttpResponse("entry saved")

def clearAll(request):
    if request.is_ajax():
        if request.method == "POST":
            data = request.POST.get("data")
            currentList = list.objects.get(owner=request.user, slug=data) #change this later
            allEntries = listEntry.objects.filter(listActual=currentList)
            for eachEntry in allEntries:
                eachEntry.delete()

            return HttpResponse("entries deleted")

def sendSMS(request):
    if request.is_ajax():
        if request.method == "POST":
            # data = request.POST.getlist("data[]")
            # sendTo = data[0] #userName
            # print "sending to ", sendTo
            # sendTo = profile.objects.get(user=User.objects.get(username=sendTo)).phoneNumber
            # sendMessage = data[1]
            # account_sid = "ACcf14924e06a090cabdf9a228a951a09b"
            # auth_token = "8f6a198971603870cefc7855b4b31e62"
            # client = TwilioRestClient(account_sid, auth_token)
            #
            # message = client.messages.create(to="+1"+sendTo, from_="+12096907178",
            #                                 body=sendMessage + " - from " + request.user.username)
            return HttpResponse("Sent.")