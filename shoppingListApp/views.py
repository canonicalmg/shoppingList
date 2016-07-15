from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.template.defaultfilters import slugify
from .models import list, listEntry, profile
from twilio.rest import TwilioRestClient
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import redirect, get_object_or_404, render
# Create your views here.

@csrf_exempt
def incomingSMS(request):
    if request.method == "POST":
        fromNum = request.POST.get('From', '')
        content = request.POST.get('Body', '')
        #if phoneNumber not recognized, prompt to create new account or associate # with account
        try:
            person = profile.objects.get(number=fromNum[2:])
            routeResponse(fromNum, content, person)
        except:
            print "new user"
            newUserMessage = "Welcome to shoppingList. We don't recognize your phone number. If you would like to use this service please respond with 'NewUser *username* *password* *firstname* *lastname*'"
            sendSMSServer(newUserMessage, fromNum)
        return HttpResponse("done")

def routeResponse(fromNum, content, person):
    content = content.split()
    if content[0] == "createList":
        sendSMSServer("Creating list", fromNum)
        createList(fromNum, content, person)
    elif content[0] == "get":
        sendSMSServer("Getting List", fromNum)
        getList(fromNum, content, person)
    elif content[0] == "clear":
        sendSMSServer("Clearing list", fromNum)
        clearList(fromNum, content, person)
    elif content[0] == "add":
        sendSMSServer("Adding to list", fromNum)
        addToList(fromNum, content, person)
    elif content[0] == "deleteList":
        sendSMSServer("Deleting list", fromNum)
        deleteList(fromNum, content, person)

def createList(fromNum, content, person):
    #createList Groceries
    listName = content[1]
    newList = list.objects(listName = listName, owner=person)
    newList.save()
    sendSMSServer("List: " + listName + " has been created by " + person.user.username, fromNum)

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
        currentProfile = profile.objects.get(user=request.user)
        allLists = list.objects.filter(owner=currentProfile)
        currentList = list.objects.get(owner=currentProfile, slug=string)
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

def homeNone(request):
    if request.user.is_authenticated():
        template = loader.get_template('home.html')
        currentProfile = profile.objects.get(user=request.user)
        allLists = list.objects.filter(owner=currentProfile)
        currentList = allLists.first()
        currentSlug = currentList.slug
        listItems = listEntry.objects.filter(listActual=currentList)
        context = {
            "currentListName": currentList.listName,
            "currentSlug": currentSlug,
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
            currentProfile = profile.objects.get(user=request.user)
            currentList = list.objects.get(owner=currentProfile, slug=slug) #change this later
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

def sendSMSServer(message, sendTo):
    account_sid = "AC60484fbea67e2c83280f90f9aa53c390"
    auth_token = "ebb9a82b47931ff2d02fb287c72d4ea3"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(to=sendTo, from_="+19258607247",
                                    body=message)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")