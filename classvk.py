import vk_api
import lang
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

langs = lang.lang()

class VapeBot:

    cache = {}

    def __init__(self,token):
        self.token = token
        self.vk = vk_api.VkApi(token=token).get_api()

    def PrepareUser(self,uid):
        if not uid in self.cache:
            self.cache[uid] = {"activity":0}

    def SetActivity(self,uid,id):
        self.cache[uid]["activity"] = id

    def GetActivity(self,uid):
        return self.cache[uid]["activity"]

    def SetLocal(self,uid,key,value):
        self.cache[uid][key] = value

    def GetLocal(self,uid,key):
        return self.cache[uid][key]

    def SendMessage(self,uid,text):
        self.vk.messages.send(peer_id=int(uid),random_id=get_random_id(),message=text)

    def ShowMainKeyboard(self,uid):
        k = VkKeyboard(one_time=False)
        k.add_button(langs.sell, color=VkKeyboardColor.POSITIVE)
        k.add_button(langs.buy, color=VkKeyboardColor.POSITIVE)
        k.add_line()
        k.add_button(langs.items, color=VkKeyboardColor.PRIMARY)
        self.vk.messages.send(peer_id=int(uid),random_id=get_random_id(),message=langs.menu,keyboard=k.get_keyboard())
        self.SetActivity(uid,0)
        
    def StartSell(self,uid):
        k = VkKeyboard(one_time=False)
        k.add_button(langs.back, color=VkKeyboardColor.NEGATIVE)
        self.vk.messages.send(peer_id=int(uid),random_id=get_random_id(),message=langs.sell_stage_1,keyboard=k.get_keyboard())
        self.SetActivity(uid,11)

    def BackScript(self,uid):
        if self.GetActivity(uid) > 0:
            self.ShowMainKeyboard(uid)


    def SellScript(self,uid,message):

        if self.GetActivity(uid) == 11:
            if len(message) > 4:
                self.SetLocal(uid,"POD_NAME",message)
                self.SetActivity(uid,12)
                self.SendMessage(uid,langs.sell_stage_2)
                return 1
            else:
                self.SendMessage(uid,langs.sell_stage_1_error)
                return 1

        if self.GetActivity(uid) == 12:
            if len(message) > 10:
                self.SetLocal(uid,"POD_DESC",message)
                self.SetActivity(uid,13)
                self.SendMessage(uid,langs.sell_stage_3)
                return 1
            else:
                self.SendMessage(uid,langs.sell_stage_2_error)
                return 1

        if self.GetActivity(uid) == 13:
            if message.isdigit():
                self.SetLocal(uid,"POD_PRICE",message)
                #self.SetActivity(uid,14)
                #self.SendMessage(uid,langs.sell_stage_4)

                self.BackScript(uid)
                self.SendMessage(uid,langs.sell_finish)
                return 1
            else:
                self.SendMessage(uid,langs.sell_stage_3_error)
                return 1

        #if self.GetActivity(uid) == 14:
        #    if type(message) == dict:
        #        self.SetLocal(uid,"POD_IMAGE",message)
        #        self.BackScript(uid)
        #        self.SendMessage(uid,langs.sell_finish)
        #        return 1
        #    else:
        #        self.SendMessage(uid,langs.sell_stage_4_error)
        #        return 1

        return False
            