from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("", index, name="index"),
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("logout/", out, name="out"),
    path("job/<int:id>/", job, name="job"),
    path("faq/", faq, name="faq"),
    path("terms/", terms, name="terms"),
    path("help/", help, name="help"),
    path("chat/", messages, name="chat"),
    path("chat/<int:id>/", chat, name="chatc"),
    path("sendmessage/", sendmessage, name="sendmessage"),
    path("refreshchat/", refreshchat, name="refreshchat"),
    path("searchpage/", searchpage, name="searchpage"),
    path("hook/", paypal_webhook, name="hook"),
    path("nots/", nots, name="nots"),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)