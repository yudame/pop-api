from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from django.conf import settings # calls the object written in settings.py
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from django.http import HttpResponse
from apps.shop.models import Shop


shop = Shop.objects.get(id=1)  # croco pizza
line_bot_api = LineBotApi(shop.line_channel.access_token)
handler = WebhookHandler(shop.line_channel.secret)


def index(request):
    return HttpResponse("test response")


@csrf_exempt
def callback(request):
    if request.method == "POST":
        signature = request.headers['X-Line-Signature']
        # global domain
        # domain = request.META['HTTP_HOST']
        body = request.get_data(as_text=True)
        # body = request.body.decode('utf-8')
        # logger.debug("Request body: " + body)
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            return HttpResponse(status=400)  # Bad Request

        return HttpResponse(status=200)  # OK

    elif request.method == "GET":
        return HttpResponse("got ur GET, now better do a POST")


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
