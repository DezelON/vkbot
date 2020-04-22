# import requests
import configs
import logging
import requests
import vk_api

vk_session = vk_api.VkApi(token=configs.tokenVK)
vk = vk_session.get_api()

def convertResponseToMessage(response):
    data = response.json()['data']
    answer = None

    if len(data) != 0:
        for d in data:
            if d['type'] == 'live':
                answer = "Кажется, тут стрим начался😏<br>Название стрима: ""{0}""<br>Игра: ""{1}""<br>Ссылочка: {2}".format(d['title'], getNameGame(d['game_id']), "https://www.twitch.tv/grandleon")

    return answer

def getPhotoFromAlbum(album=269279886):
    # session = vk.Session()
    # api = vk.API(session, v=5.50)

    answer = []

    # response = api.photos.get(access_token=configs.tokenUserVK, owner_id=-18343283, album_id=str(album), count=1000)

    # if 'items' in response:
    #     for photodata in response["items"]:
    #         answer.append("photo{0}_{1}".format(photodata["owner_id"], photodata["id"]))
    # else:
    #     return ["photo-18343283_456242796"]

    return answer


def stream_started(login=None):
    get_header = {
        'Client-ID': configs.twitch_tokenID,
    }

    if not login is None:
        response = requests.get("https://api.twitch.tv/helix/streams?user_login={}".format(login), headers=get_header)
    else:
        response = requests.get("https://api.twitch.tv/helix/streams?user_id={}".format(configs.twitch_LeonID), headers=get_header)

    return convertResponseToMessage(response)

def getNameGame(game_id):
    get_header = {
        'Client-ID': configs.twitch_tokenID,
    }

    response = requests.get("https://api.twitch.tv/helix/games?id={}".format(game_id), headers=get_header)
    data = response.json()['data']

    if len(data) != 0:
        return str(data[0]['name'])
    else:
        return "Неизвестная игра"

def getAllowersMembers(group_id=18343283):

    users_Allowed = []

    # need_answer_api = api.messages.getConversations(access_token=configs.tokenVK, group_id=str(group_id))

    # count_ans = int(need_answer_api["count"])//200

    # if int(need_answer_api["count"])%200 != 0:
    #     count_ans+= 1

    # for i in range(count_ans):
    #     answer_api = api.messages.getConversations(access_token=configs.tokenVK, group_id=str(group_id), offset=str(i*200), count=str(200))
    #     items_answer = answer_api['items']
    #     for elem in items_answer:
    #         conversation_answer = elem['conversation']
    #         if conversation_answer['can_write']['allowed']:
    #             users_Allowed.append(conversation_answer['peer']['id'])

    return users_Allowed

def returncode(ids, message, attachment = None):
    code = 'API.messages.send({'
    code += '"user_ids": "' + str(ids) + '", '
    code += '"message": "' + str(message) + '", '
    code += '"dont_parse_links": "' + str(1) + '", '
    if not attachment is None:
        code += '"attachment": "' + str(attachment) + '", '
    code += '});'
    return code

def SplitArray100(array_ids):
    i = 1

    mass_answ_array = []
    answ_array = []
    for id in array_ids:
        if i == 100:
            mass_answ_array.append(answ_array)
            answ_array = []
            i = 1
        answ_array.append(id)
        i += 1
    mass_answ_array.append(answ_array)

    return mass_answ_array

def mailingMessages(ids, message = "Тут, кажется, стрим начался :3", attachment = None):
    # session = vk.Session()
    # api = vk.API(session, v=5.50)

    # if len(ids) == 0:
    #     return None

    # str_id = ""
    # i_code = 1
    # code = ""
    answ = ""

    # for array_ids in SplitArray100(ids):
    #     str_id = ""
    #     if i_code == 25:
    #         api.execute(access_token=configs.tokenVK, code = code)
    #         code = ""
    #         i_code = 1
    #     for id in range(len(array_ids)):
    #         if id != range(len(array_ids)):
    #             str_id+= str(array_ids[id])+", "
    #         else:
    #             str_id+= str(array_ids[id])
    #     i_code +=1
    #     code += returncode(str_id, message, attachment)
    # answ = api.execute(access_token=configs.tokenVK, code = code)
    return answ

def build_url(scope):
    return "{0}?client_id={1}&response_type={2}&redirect_uri={3}&scope={4}".format("https://id.twitch.tv/oauth2/authorize", configs.twitch_ClientID, "code", configs.redirect_uri, scope)

def getAppToken():

    post_data = {
        "client_id": configs.twitch_tokenID,
        "client_secret": configs.twitch_tokenSecret,
        "grant_type": "client_credentials",
        "scope": ["analytics:read:extensions"],
    }

    response = requests.post("https://id.twitch.tv/oauth2/token", data=post_data)

    return response.text