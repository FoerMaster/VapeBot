import vk_api
import time
import classvk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import lang
langs = lang.lang()

VapeBot = classvk.VapeBot("861c2d4af8cbb1af9f959c32f4c27f6fbffcd4c51ffc6d63431ad0044ca2463b71d72e086b988953adcf7","732044da1b8f01f4719ff4a5a39e580d3aadda23e786df740d745cccdd0292787b20065a36001f878c42a")
session = VapeBot.session
longpoll = VkLongPoll(session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.from_user:

            print('Сообщение от: ', event.user_id)

            uid = event.user_id
            
            message = event.text

            attachments = event.attachments
            
            photo = []

            if len(attachments) > 0:
                count = int(len(attachments) / 2)
                for attach in range(count-1):
                    attach = attach + 1
                    if attachments['attach' + str(attach) + "_type"] == "photo":
                        photo.append("photo{}".format(attachments['attach' + str(attach)]))

            if len(photo) == 0:
                photo = False

            VapeBot.PrepareUser(uid)

            if message == 'Начать':
                VapeBot.ShowMainKeyboard(uid)
                VapeBot.SendMessage(uid,langs.hello)
                continue

            if message == langs.back:
                VapeBot.BackScript(uid)
                continue

            if message == langs.sell:
                VapeBot.StartSell(uid)
                continue

            if message == langs.buy:
                VapeBot.StartBuy(uid)
                continue

            if VapeBot.SellScript(uid,message,photo):
                continue

            if VapeBot.BuyScript(uid,message):
                continue


            VapeBot.SendMessage(uid,langs.unk_command)