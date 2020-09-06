import vk_api
import time
import classvk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

VapeBot = classvk.VapeBot("861c2d4af8cbb1af9f959c32f4c27f6fbffcd4c51ffc6d63431ad0044ca2463b71d72e086b988953adcf7")
vk = VapeBot.vk

while True:
    massages=vk.messages.getDialogs(count=5,unread=1)

    if massages['count']>0:

        print('Сообщение от', massages['items'][0]['message']['user_id'])

        uid = massages['items'][0]['message']['user_id']
        
        body=massages['items'][0]['message']['body']

        VapeBot.PrepareUser(uid)

        if body == 'Начать':
            VapeBot.ShowMainKeyboard(uid)
            VapeBot.SendMessage(uid,"Привет это бот для удобной продажи ваших устройств! И тут типо описание всего происходящего...")
            continue

        if body == 'Отмена':
            VapeBot.BackScript(uid)
            continue

        if body == 'Продажа':
            VapeBot.StartSell(uid)
            continue

        if VapeBot.SellScript(uid,body):
            continue

        VapeBot.SendMessage(uid,"Не понял, нажимай кнопки!")

    time.sleep(1)