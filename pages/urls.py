from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("delivery/", views.delivery, name="delivery"),
    path("contacts/", views.contacts, name="contacts"),

    # currency switcher остаётся в pages (как раньше)
    path("currency/<str:code>/", views.set_currency, name="set_currency"),
]
