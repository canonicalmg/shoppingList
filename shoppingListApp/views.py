from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.template.defaultfilters import slugify
from .models import list, listEntry

# Create your views here.
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