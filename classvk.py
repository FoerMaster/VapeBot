import vk_api
import lang
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

langs = lang.lang()

class VapeBot:

    cache = {}

    def __init__(self,token,token2):
        self.token = token
        self.session = vk_api.VkApi(token=token)
        self.vk = self.session.get_api()
        self.user_vk = vk_api.VkApi(token=token2).get_api()

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

    def PostInWall(self,text,attach):
        if attach:
            self.user_vk.wall.post(
                message=text,
                owner_id="-198488448",
                from_group=1,
                attachments=','.join([str(elem) for elem in attach]) 
            )
        else:
            self.user_vk.wall.post(
                message=text,
                owner_id="-198488448",
                from_group=1,
            )

    def StartBuy(self,uid):
        k = VkKeyboard(one_time=False)
        k.add_button(langs.back, color=VkKeyboardColor.NEGATIVE)
        self.vk.messages.send(peer_id=int(uid),random_id=get_random_id(),message=langs.buy_stage_1,keyboard=k.get_keyboard())
        self.SetActivity(uid,21)
        
    def BuyScript(self,uid,message):
        if self.GetActivity(uid) == 21:
            if len(message) > 4:
                self.SendMessage(uid,"Ищу этот код, погоди пока")
                self.BackScript(uid)
                return 1
            else:
                self.SendMessage(uid,langs.buy_stage_1_error)
                return 1

    def SellScript(self,uid,message,photo):

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
                self.SetActivity(uid,14)
                self.SendMessage(uid,langs.sell_stage_4)
                return 1
            else:
                self.SendMessage(uid,langs.sell_stage_3_error)
                return 1

        if self.GetActivity(uid) == 14:
            if len(message) > 3:
                self.SetLocal(uid,"POD_CITY",message)
                self.SetActivity(uid,15)
                self.SendMessage(uid,langs.sell_stage_5)
                return 1
            else:
                self.SendMessage(uid,langs.sell_stage_4_error)
                return 1

        if self.GetActivity(uid) == 15:
            if photo:
                self.SetLocal(uid,"POD_IMAGE",photo)
                self.BackScript(uid)
                self.PostInWall("Название: " + self.GetLocal(uid,"POD_NAME") + "\n\n" + self.GetLocal(uid,"POD_DESC") + "\nЦена: " + self.GetLocal(uid,"POD_PRICE") + "руб" + "\n\n\nКод: TMN72441S41a",self.GetLocal(uid,"POD_IMAGE"))
                self.SendMessage(uid,langs.sell_finish)
                return 1
            else:
                self.SendMessage(uid,langs.sell_stage_5_error)
                return 1

        return False
            