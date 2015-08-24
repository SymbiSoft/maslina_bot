#coding:utf-8
import requests
import json
import time
import random

#author - SymbiSoft
#email - stalkernya.1@gmail.com
#telegram - @SymbiSof
#vkontakte - SymbiSoft

#В нем утекает память.... Кажись это все изза JSON. Вообщем я предупридил. ПОФИКШЕНО!!!
#И тут все писалось что бы работало хоть как, по этому лучше сделать рефаторинг!
#Вообщем все почти работает. Пожалуйста, укажите меня как автор в окошке ABOUT) Не зря же я все делал)
#Удачи разобратся в моем коде


bot_mode=0 #По умолчания режим бота - Нормальный т.е. любое число, которое отличается от еденицы.

URL = 'https://api.telegram.org/bot'
TOKEN = "ТОКЕН ТЕЛЕГРАМА ВСТАВЛЯЕТСЯ ТУТ"

"""
__          __     _____  _   _ _____ _   _  _____ _ 
\ \        / /\   |  __ \| \ | |_   _| \ | |/ ____| |
 \ \  /\  / /  \  | |__) |  \| | | | |  \| | |  __| |
  \ \/  \/ / /\ \ |  _  /| . ` | | | | . ` | | |_ | |
   \  /\  / ____ \| | \ \| |\  |_| |_| |\  | |__| |_|
    \/  \/_/    \_\_|  \_\_| \_|_____|_| \_|\_____(_)

"""
#С ЭТОГО МОМЕНТА ЛУЧШЕ НИЧЕГО НЕ ТРОГАТЬ
photo_about_stalker=["85291460", "8109175", "38635106", "17035846", "96812503", "23289884", "57579356", "92212978", "42278444"] #В этом списке OWNER ID групп в ВК. Например- vk.com/photo-xxxxxxxx
prikol = json.loads(open("words.json","r").read()) #Загружает фразы
zona_humor = json.loads(open("zona_humor.json","r").read()) #Тут берутся шутки
log = open('bot.log', 'w')#Сюда пишется лог
  
def sendMessage(to, text): #Функция отправки СМСок
  log.write("sendMessage: to = {0}, text = {1}\n".format(to, text))
  log.flush()
  request = requests.post(URL + TOKEN + "/sendMessage", data = {'text': text, 'chat_id': to})
  if not request.status_code == 200:
    log.write("error {0}\n".format(request.status_code))
    log.flush()
    return False
  return True

offset = 0
def checkUpdates():
  global offset, bot_mode
  try:
    request = requests.post(URL + TOKEN + '/getUpdates', data = {
      'offset': offset + 1,
      'limit': 100,
      'timeout': 0
    })
  except Exception as e:
    log.write("exception {0}\n".format(e))
    log.flush()
    return False
  
  if not request.status_code == 200:
    log.write("request error {0}\n".format(request.status_code))
    log.flush()
 
  result = request.json()
 
  if not result['ok']:
    log.write("invalid response: {0}\n".format(json.dumps(result)))
    log.flush()
 
  for update in result['result']:
    offset = update['update_id']
    message = update['message']
    log.write("message text: {0}\n".format(message['text']))
    log.flush()
#__          __     _____  _   _ _____ _   _  _____ _ 
#\ \        / /\   |  __ \| \ | |_   _| \ | |/ ____| |
# \ \  /\  / /  \  | |__) |  \| | | | |  \| | |  __| |
#  \ \/  \/ / /\ \ |  _  /| . ` | | | | . ` | | |_ | |
#   \  /\  / ____ \| | \ \| |\  |_| |_| |\  | |__| |_|
#    \/  \/_/    \_\_|  \_\_| \_|_____|_| \_|\_____(_)
#Аж до этого момента. Дале уже можно все исправлять как душе угодно


  if '/zona_humor' in message['text']:
    number_of_anektod=random.choice(zona_humor)#Выбирается рандомно шутка
    sendMessage(message['chat']['id'], number_of_anektod) #А тут она уже отсылается по команде /zona_humor(По аналогии работают и другие комманды)
    
  elif '/start' in message['text']: #Первая комманда описивает что можнет бот
    sendMessage(message['chat']['id'], "Привет.\r\nЯ Маслина-Бот. Если ты любител серии игр S.T.A.L.K.E.R. то я незаменим /U+1F60B .\r\nЯ уже кое чего умею, например фотки про сталкер кидать.Или рассказать анекдот про сталкер.\r\nНу, удачи тебе сталкер!")
      
  elif '/about' in message['text']: #Про бота
    sendMessage(message['chat']['id'], "Мой хозяин - @SymbiSoft\r\nСсылка на него - telegram.me/symbisoft\r\nМое имя в Телеграме - @maslina_bot\r\nА вдруг кому-то захочеш дать мою ссылку то вот - telegram.me/maslina_bot\r\nСпасибо за помощь Nikita aka @nsychev Sychev\r\nВерсия моей прошивки - 0.5 Open ")
      
  elif '/normal_mode' in message['text'] and message['from']['id'] == 120063211: #Цифры - ID владельца ботом или человека, который может включать режимы 
    bot_mode=0
    sendMessage(message['chat']['id'], "Режим флуда выключен")
      
  elif '/flood_mode' in message['text'] and message['from']['id'] == 120063211:#Аналогично прошлому
    bot_mode=1
    sendMessage(message['chat']['id'], "Режим флуда включен")

#Не работает      
#   elif '/super_flood_mode' in message['text'] and message['from']['id'] == 120063211: 
#      bot_mode=2
#      sendMessage(message['chat']['id'], "Режим супер флуда включен")
      
  elif '/radiation_zone' in message['text']:#Из сайта chernobyl-tour.com кидает радиоционную обстановку сейчас(картинка автоматом генерируется у них на сайте) 
    sendMessage(message['chat']['id'], "https://www.chernobyl-tour.com/uploads/inform_rad_v3.jpg") 
      
      
#Лень искать ссылки на музыку. Со spaces.ru долго кидает музыку    
#    elif '/music_zone' in message['text']:
#      r = requests.post(URL + TOKEN + "/sendChatAction", data = {'chat_id': message['chat']['id'], 'action': 'upload_audio'})    
#      r = requests.get("http://msxe.imagefiles.me/m/081058072102066061093013061030015147212172146045215173/1440231769/22698723/0/6e36fb97bfb402d6d26c94eda91acc43/Hollywood_Undead-Young-spaces.ru.mp3")
#      r2 = requests.post(URL + TOKEN + "/sendAudio", data = {'chat_id': message['chat']['id']}, files = {'audio': ('STALKER.mp3', r.content)})

#Так выполняются комманды с ключем. Например: "/weather_in_zone ЧАЭС" - param будет равен - ЧАЭС
#  elif message['text'].startswith('/weather_in_zone'):
#    param = message['text'][9:]


  elif '/photo_zone' in message['text']: #Рандомные фотки из пабликов в вк
    group_stalker_photo = random.choice(photo_about_stalker)#Тут он по рандомчику выбирает нашу жертву)
    r = requests.get("https://api.vk.com/method/photos.get?owner_id=-"+group_stalker_photo+"&album_id=wall")#Запрос ссылок на фото
    result = r.json()
    photo = random.choice(result["response"])
    url2 = photo["src_big"]
    sendMessage(message['chat']['id'], url2)
      
       
  elif bot_mode==1: #Собственно сам режим флуда. Вот он кажись и жрет так много оперативки и CPU'шку напрягает не хило
	   prikol_mess = random.choice(prikol) 
	   sendMessage(message['chat']['id'], prikol_mess)

      
      
while True:
  try:
    checkUpdates()
  except Exception as e:
    log.write("exception {0}\n".format(e))
    log.flush()
  time.sleep(0.3)
