import logging

from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from django.conf import settings  # calls the object written in settings.py
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from django.http import HttpResponse

from apps.line_app.models import LineChannel


def index(request):
    return HttpResponse("test response")


@csrf_exempt
def callback(request, line_channel_id):
    if request.method == "POST":

        line_channel = LineChannel.objects.get(id=line_channel_id)
        line_bot = line_channel.get_bot()

        signature = request.headers['X-Line-Signature']
        request_data = request.body.decode('utf-8')

        # global domain
        # domain = request.META['HTTP_HOST']

        try:
            line_bot.handle(request_data, signature)
        except InvalidSignatureError:
            logging.error("Invalid signature. Please check your channel access token/channel secret.")
            return HttpResponse(status=400)  # Bad Request
        except Exception as e:
            logging.error(str(e))
            return HttpResponse(status=500)  # Server Error

        return HttpResponse(status=200)  # OK

    elif request.method == "GET":
        return HttpResponse("got ur GET, now better do a POST")
