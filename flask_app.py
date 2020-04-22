import vk_api
import vk_api.utils as Utils
import logging
import requests
import random

import configs
import twitchApi
import userApi
import botApi

from datetime import datetime, timedelta
from time import mktime

from flask import Flask, request, json, redirect

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Что тебе тут нужно?"

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'message_new':
        user_id = data['object']['user_id']

        # if int(user_id) == 119144881 or int(user_id) == 15574680:
        botApi.getMessage(user_id, data['object']['body'])

        return 'ok'
    if data['type'] == 'confirmation':
        return "28accafe"
    return 'WTF?!'

@app.route('/vkbot')
def vkbot():
    response = request.args
    if 'login' in response:
        message = twitchApi.stream_started(response['login'])
        if not message is None and not configs.twitch_LeonStream:
            configs.twitch_LeonStream = True
            members = botApi.getCanWriteMembers(botApi.getAllMembers(18343283))
            botApi.bulkMailing(members, message)
            return "Stream started!!"
        elif configs.twitch_LeonStream and message is None:
            if configs.timeEndStream == 0:
                configs.timeEndStream = int(mktime((datetime.now()).timetuple()))+900
                return "Stream moved to the end stage!!"
            elif configs.timeEndStream <= int(mktime((datetime.now()).timetuple())):
                configs.timeEndStream = 0
                configs.twitch_LeonStream = False
                return "Stream ended!!"
            else:
                return "Stream at the end!!"
    else:
        logging.error(response)
    if configs.twitch_LeonStream:
        return "There is a live broadcast!!"
    else:
        return "There is no stream!!"

# @app.route('/callback')
# def callback():
#     # data = request.args

#     userApi.setCursorMessageUser(119144881, 10)

#     return str(userApi.getUser(119144881))

# @app.route('/check')
# def check():

#     # return twitchApi.getAppToken()

#     get_header = {
#         'Client-ID': configs.twitch_tokenID,
#         "Authorization": 'Bearer {}'.format(configs.twitch_bearerToken)
#     }

#     response = requests.get("https://api.twitch.tv/helix/webhooks/subscriptions", headers=get_header)

#     return response.text

# @app.route('/test')
# def test():
#     post_header = {
#         'Client-ID': configs.twitch_tokenID,
#     }

#     post_data = {
#         "hub.callback": configs.redirect_uri,
#         "hub.mode": "subscribe",
#         "hub.topic": "https://api.twitch.tv/helix/streams?user_id={}".format(configs.twitch_LeonID),
#         "hub.lease_seconds": 864000
#     }

#     requests.post("https://api.twitch.tv/helix/webhooks/hub", headers=post_header, data=post_data)
#     return "ok"

@app.route("/ping")
def ping():
    return "ok"
