from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")

def delivery(request):
    return render(request, "pages/delivery.html")

def contacts(request):
    return render(request, "pages/contacts.html")

def catalog(request):
    return render(request, "pages/catalog.html")
