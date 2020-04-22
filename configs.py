# tokenVK = '***'
tokenVK = '***'
tokenUserVK = '***'

twitch_tokenID = "***"
twitch_tokenSecret = "***"
twitch_bearerToken = "***"

timeEndStream = 0

twitch_LeonID = 38964111

twitch_LeonStream = False

timerstart = False

redirect_uri = 'http://dezelon.pythonanywhere.com/callback'

dbName = "Meido$db_vkbot"
dbHost = "Meido.mysql.pythonanywhere-services.com"
dbUser = "Meido"
dbPassword = "***"

AnswerTree = {
    "const":{
        "startmessage": "Привет! Это первое сообщение, которое получает автоматически каждый кто пишет сообщение в группу. Вы можете включить бота для дополнительной информации использовав кнопочку снизу, а также вам будут приходить анонсы старта стримов на Twitch. Если же вы хотите просто оставить сообщение в группу, то бота включать не обязательно :3<br>Приятного вам дня!",
        "startkeyboard": [["enable"]],
        "startattachment": None,
        "keyboardname": 0, #Какой элемент будет браться в случае отсутствия данного поля
        "keyboardcolor": "primary",
        "errormessage": "Кажется ты где-то ошибся", #Сообщение если произошла какая-то ошибка, а erroranswer=None
        "message": ["И вот тут что-то пошло не так"],
        "allowbranch": ["0", "disable"], #Всегда разрешённые ветки
        "keyboard": [["0", "disable"]], #Выводит данный keyboard, если стандартный отсутствует
    },
    "disable": {
        "name": ["Выключить бота"],
        "keyboardcolor": "negative",
        "funcmessage": "disablebot",
        "keyboard": [["enable"]],
        "redirect": "0",
    },
    "enable": {
        "name": ["Включить бота"],
        "keyboardcolor": "positive",
        "funcmessage": "enablebot",
        "redirect": "0",
    },
    "0": {
        "name": ["Главное меню"], #Что нужно вводить, чтобы попать сюда | Обязательно!!
        "allowbranch": ["1"], #Ветки на которые можно перейти | Обязательно!! (если нет redirect)
        "keyboardname": 0, #Как будет отображаться на keyboard кнопка (id элемента массива из name или текстовое обозначение)
        "keyboardcolor": "negative", #Какой цвет будет иметь кнопка
        "message": ["Ты снова в главном меню"], #Сообщение при переходе на данную ветку
        "errormessage": "Кажется ты где-то ошибся", #Сообщение в случае ошибочного ввода
        "keyboard": [["1"], ["disable"]], #Клавиатура данной ветки
        # "funcs": ["gohome"] #Функция, вызываемая при переходе на данную ветку
    },
    "1": {
        "name": ["Информация"],
        "message": ["Leon, он же Льев, занимается контентмейкерством с февраля 2012 года и за это время было много всего интересного:<br>YouTube (2012) https://www.youtube.com/user/GrandLeonTV<br>Twitch (2017) https://www.twitch.tv/grandleon<br>Discord Grand Club https://discordapp.com/invite/RdzDDVW<br>Основная страница Льва ВК https://vk.com/grandleon<br>Сталкер страйк YT (2016) https://is.gd/ds7rgw<br>GTA Role Play Universe (2017) https://www.youtube.com/user/HAMHEHADO<br>Rust F3 Server (2015-2017 Завершен) https://vk.com/f3rust<br>MineCraft Server Strange World (2019) https://strangeworld.herokuapp.com<br>Записи стримов YT https://www.youtube.com/user/GrandLeonLive<br>Записи стримов VK (ВСЕ) https://vk.com/leoscomeback<br>Клипы и цитаты https://vk.com/grandcitation<br>И многое другое по мелочи вы можете найти в группе ВК https://vk.com/grandleontv"],
        # "redirect": "0",
        # "randommessage": True,
        # "attachment": "photo-18343283_456242796",
        # "allowbranch": ["0"],
        "keyboard": [["0", "disable"]],
    },
    # "2": {
    #     "name": ["Информация обо мне"],
    #     "funcmessage": "infoaboutuser", #Ответ в виде функции
    #     "redirect": "0", #Переход на другую ветку без вывода сообщения данной ветки, но с выводом keyboard
    # },
    # "3": {
    #     "name": ["Test"],
    #     "customanswer": True,
    #     "funcmessage": ["Test"],
    # }
}