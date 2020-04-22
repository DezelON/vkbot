import vk_api
import vk_api.utils as Utils
import random
import logging

import configs
import userApi

from vk_api.keyboard import VkKeyboard

vk_session = vk_api.VkApi(token=configs.tokenVK)
vk = vk_session.get_api()

def getMessage(id, message):
    userCursor = userApi.getCursorMessageUser(id)

    if userCursor is None:
        userApi.createUser(id)
        if "startkeyboard" in configs.AnswerTree["const"]:
            keyboard = creareKeyboard(configs.AnswerTree["const"]["startkeyboard"], False)
        else:
            keyboard = None

        if "startattachment" in configs.AnswerTree["const"]:
            attachment = configs.AnswerTree["const"]["startattachment"]
        else:
            attachment = None
        createAnswer(id, configs.AnswerTree["const"]["startmessage"], keyboard, attachment)
        return

    if not userApi.canWrite(id):
        if message.lower() == configs.AnswerTree["enable"]["name"][0].lower():
            botFunc = BotFunc()
            method = getattr(botFunc, configs.AnswerTree["enable"]["funcmessage"])
            message, keyboard, attachment = method(id)
            createAnswer(id, message, keyboard, attachment)
            return
        else:
            return

    if not userCursor in configs.AnswerTree:
        userCursor = "0"

    itsCustomBranch = False

    if "customanswer" in configs.AnswerTree[userCursor] and configs.AnswerTree[userCursor]["customanswer"]:
        itsCustomBranch = True

    answerbranch = None
    if "allowbranch" in configs.AnswerTree[userCursor]:
        for idbranch in configs.AnswerTree[userCursor]["allowbranch"]:
            for name in configs.AnswerTree[idbranch]["name"]:
                if message.lower() == name.lower():
                    answerbranch = idbranch
            if not answerbranch is None:
                break

    if answerbranch is None:
        for idbranch in configs.AnswerTree["const"]["allowbranch"]:
            for name in configs.AnswerTree[idbranch]["name"]:
                if message.lower() == name.lower():
                    answerbranch = idbranch
            if not answerbranch is None:
                break

    if answerbranch is None and not itsCustomBranch:
        if "keyboard" in configs.AnswerTree[userCursor]:
            if configs.AnswerTree[userCursor]["keyboard"] is None:
                keyboard = None
            else:
                keyboard = creareKeyboard(configs.AnswerTree[userCursor]["keyboard"])
        else:
            keyboard = creareKeyboard(configs.AnswerTree["const"]["keyboard"])

        if "errormessage" in configs.AnswerTree[userCursor]:
            createAnswer(id, configs.AnswerTree[userCursor]["errormessage"], keyboard)
        else:
            createAnswer(id, configs.AnswerTree["const"]["errormessage"], keyboard)
        return

    if itsCustomBranch and answerbranch is None:
        userApi.setCursorMessageUser(id, configs.AnswerTree[answerbranch]["redirect"])
    else:
        if "funcs" in configs.AnswerTree[answerbranch]:
            logging.error("func присутствует")

        if "funcmessage" in configs.AnswerTree[answerbranch]:
            botFunc = BotFunc()
            method = getattr(botFunc, configs.AnswerTree[answerbranch]["funcmessage"])
            message, keyboard, attachment = method(id)

            if "redirect" in configs.AnswerTree[answerbranch] and keyboard is None:
                if "keyboard" in configs.AnswerTree[configs.AnswerTree[answerbranch]["redirect"]]:
                    if configs.AnswerTree[configs.AnswerTree[answerbranch]["redirect"]]["keyboard"] is None:
                        keyboard = None
                    else:
                        keyboard = creareKeyboard(configs.AnswerTree[configs.AnswerTree[answerbranch]["redirect"]]["keyboard"])
                else:
                    keyboard = creareKeyboard(configs.AnswerTree["const"]["keyboard"])
            elif "keyboard" in configs.AnswerTree[answerbranch] and keyboard is None:
                if configs.AnswerTree[answerbranch]["keyboard"] is None:
                    keyboard = None
                else:
                    keyboard = creareKeyboard(configs.AnswerTree[answerbranch]["keyboard"])

            createAnswer(id, message, keyboard, attachment)
        elif "message" in configs.AnswerTree[answerbranch]:
            if "redirect" in configs.AnswerTree[answerbranch]:
                if "keyboard" in configs.AnswerTree[configs.AnswerTree[answerbranch]["redirect"]]:
                    if configs.AnswerTree[configs.AnswerTree[answerbranch]["redirect"]]["keyboard"] is None:
                        keyboard = None
                    else:
                        keyboard = creareKeyboard(configs.AnswerTree[configs.AnswerTree[answerbranch]["redirect"]]["keyboard"])
                else:
                    keyboard = creareKeyboard(configs.AnswerTree["const"]["keyboard"])
            elif "keyboard" in configs.AnswerTree[answerbranch]:
                if configs.AnswerTree[answerbranch]["keyboard"] is None:
                    keyboard = None
                else:
                    keyboard = creareKeyboard(configs.AnswerTree[answerbranch]["keyboard"])
            else:
                keyboard = creareKeyboard(configs.AnswerTree["const"]["keyboard"])

            if "attachment" in configs.AnswerTree[answerbranch]:
                attachment = configs.AnswerTree[answerbranch]["attachment"]
            else:
                attachment = None

            if  "randommessage" in configs.AnswerTree[answerbranch] and configs.AnswerTree[answerbranch]["randommessage"]:
                createAnswer(id, configs.AnswerTree[answerbranch]["message"][random.randint(0, len(configs.AnswerTree[answerbranch]["message"])-1)], keyboard, attachment)
            else:
                createAnswer(id, configs.AnswerTree[answerbranch]["message"][0], keyboard, attachment)
        else:
            createAnswer(id, configs.AnswerTree["const"]["message"])

        if "redirect" in configs.AnswerTree[answerbranch]:
            userApi.setCursorMessageUser(id, configs.AnswerTree[answerbranch]["redirect"])
        else:
            userApi.setCursorMessageUser(id, answerbranch)

def creareKeyboard(confkeyboard, param=True):
    keyboard = VkKeyboard(param)
    id = 0
    for line in confkeyboard:
        if len(line) > 0:
            id += 1
            for buttonid in line:
                if "keyboardname" in configs.AnswerTree[buttonid]:
                    if type(configs.AnswerTree[buttonid]["keyboardname"]) == int:
                        if len(configs.AnswerTree[buttonid]["name"])-1 < configs.AnswerTree[buttonid]["keyboardname"]:
                            textbutton = configs.AnswerTree[buttonid]["name"][configs.AnswerTree["const"]["keyboardname"]]
                        else:
                            textbutton = configs.AnswerTree[buttonid]["name"][configs.AnswerTree[buttonid]["keyboardname"]]
                    else:
                        textbutton = configs.AnswerTree[buttonid]["keyboardname"]
                else:
                    textbutton = configs.AnswerTree[buttonid]["name"][configs.AnswerTree["const"]["keyboardname"]]

                if "keyboardcolor" in configs.AnswerTree[buttonid]:
                    colorbutton = configs.AnswerTree[buttonid]["keyboardcolor"]
                else:
                    colorbutton = configs.AnswerTree["const"]["keyboardcolor"]

                keyboard.add_button(textbutton, colorbutton)
            if len(confkeyboard) != id:
                keyboard.add_line()

    return keyboard.get_keyboard()

def createAnswer(user_id, message, keyboard=None, attachment=None):
    vk.messages.send(
        user_id=str(user_id),
        random_id=Utils.get_random_id(),
        message= message,
        keyboard = keyboard,
        attachment = attachment)

def createAnswers(user_ids, message, keyboard=None, attachment=None):
    vk.messages.send(
        user_ids = str(user_ids),
        random_id = Utils.get_random_id(),
        message = message,
        # keyboard = keyboard,
        attachment = attachment,
        dont_parse_links = str(1))

def getAllMembers(group_id):
    users_Allowed = []
    i = 0
    conversations = vk.messages.getConversations(access_token=configs.tokenVK, group_id=str(group_id), offset=i*200, count=200)
    while len(conversations['items']) != 0:
        items_conversations = conversations['items']
        for elem in items_conversations:
            if elem['conversation']['can_write']['allowed']:
                users_Allowed.append(elem['conversation']['peer']['id'])
        i+=1
        conversations = vk.messages.getConversations(access_token=configs.tokenVK, group_id=str(group_id), offset=i*200, count=200)
    return users_Allowed

def getCanWriteMembers(users):
    users_Allowed = []
    users100 = []
    for user in users:
        if userApi.canWrite(user):
            users100.append(user)
            if len(users100) == 100:
                    users_Allowed.append(users100)
                    users100 = []
    if len(users100) != 0:
        users_Allowed.append(users100)
    return users_Allowed

def bulkMailing(musers, message):
    if len(musers) != 0:
        photos = getPhotosFromAlbum()
        attachment = photos[random.randint(0, len(photos)-1)]
        for users in musers:
            strusers = ', '.join(map(str, users))
            createAnswers(strusers, message, attachment=attachment)

def getPhotosFromAlbum(album=269279886):
    vk_user_session = vk_api.VkApi(token=configs.tokenUserVK)
    vk_user = vk_user_session.get_api()
    answer = []
    response = vk_user.photos.get(owner_id=-18343283, album_id=str(album), count=1000)

    if 'items' in response:
        for photodata in response["items"]:
            answer.append("photo{0}_{1}".format(photodata["owner_id"], photodata["id"]))
    else:
        return ["photo-18343283_456242796"]

    return answer

class BotFunc:

    def infoaboutuser(self, id, **kwargs):
        user = userApi.getUser(id)
        if user is None:
            return "Странно, но я не могу найти такого пользователя"
        answer = ""
        for key, value in user.items():
            answer += str(key) + " = " + str(value)+"<br>"
        return answer, None, None #Message, KeyBoard, Attachment

    def enablebot(self, id, **kwargs):
        user = userApi.getUser(id)
        if user is None:
            return "Странно, но я не могу найти такого пользователя"
        userApi.allowWriteUser(id)
        userApi.setCursorMessageUser(id, configs.AnswerTree["enable"]["redirect"])
        keyBoard = creareKeyboard(configs.AnswerTree["0"]["keyboard"])
        answer = "Бот был успешно включен!<br>Сейчас вы находитесь в главном меню :3"
        return answer, keyBoard, None #Message, KeyBoard, Attachment

    def disablebot(self, id, **kwargs):
        user = userApi.getUser(id)
        if user is None:
            return "Странно, но я не могу найти такого пользователя"
        userApi.disableWriteUser(id)
        userApi.setCursorMessageUser(id, configs.AnswerTree["disable"]["redirect"])
        answer = "Эх, как жаль, что ты решил меня выключить :c<br>Но я ничего не могу с этим поделать.. Просто знай, что ты всегда можешь снова ко мне вернуться нажав на кнопочку снизу :3"
        keyBoard = creareKeyboard(configs.AnswerTree["disable"]["keyboard"], False)
        return answer, keyBoard, None #Message, KeyBoard, Attachment