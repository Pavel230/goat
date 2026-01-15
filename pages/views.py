from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme

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



def set_currency(request, code: str):
    code = (code or "").upper()
    if code in ("KZT", "USD"):
        request.session["currency"] = code

    nxt = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        nxt = "/"
    return redirect(nxt)
