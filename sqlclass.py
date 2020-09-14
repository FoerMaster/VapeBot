import pymysql.cursors

color = {
        'HEADER':'\033[95m',
        'OKBLUE':'\033[94m',
        'OKGREEN':'\033[92m',
        'WARNING':'\033[93m',
        'FAIL':'\033[91m',
        'ENDC':'\033[0m',
        'BOLD':'\033[1m',
        'UNDERLINE':'\033[4m',
    }
    
class DataBase:

    cache = {"user":{},"post":{}}

    def MsgC(self,message,color):
        print(color + "[SQL] " + message)

    def __init__(self,host,logind,password,database):
        '''self.mysql = pymysql.connect(host=host,user=logind,password=password,db=database,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        try:
            with self.mysql.cursor() as cursor:
                sql = "CREATE TABLE IF NOT EXISTS `Main` (`id` longtext CHARACTER SET utf8 NOT NULLL,`uid` bigint(255) NOT NULL,`post_id` int(255) NOT NULL,`delete` int(255) NOT NULL,`posted` int(255) NOT NULL)"
                cursor.execute(sql)
            self.mysql.commit()
            self.MsgC("База данных подключена!", color['OKGREEN'])
        except:
            self.MsgC("База данных недоступна!", color['FAIL'])'''

    def GetUserPosts(self,uid):
        if not uid in self.cache["user"]:
            self.cache["user"][uid] = {}

        founded = []

        for v in self.cache["user"][uid]:
            founded.append(v)

        return founded

    def GetPostData(self,postid):
        if postid in self.cache["post"]:
            return self.cache["post"][postid]
            
        return False

    def AddPost(self,id,uid,post_id,name):
        if not uid in self.cache["user"]:
            self.cache["user"][uid] = {}

        if not id in self.cache["post"]:
            self.cache["post"][id] = {}

        self.cache["post"][id] = {
            'id':id,
            'name':name,
            'uid':uid,
            'post':post_id,
            'delete':False,
            'posted':False
        }

        self.cache["user"][uid][id] = True

    def DeletePost(self,post_id):
        if not post_id in self.cache["post"]:
            self.cache["post"][post_id] = {}

        self.cache["post"][post_id]['delete'] = True

    def PostingPost(self,post_id):
        if not post_id in self.cache["post"]:
            self.cache["post"][post_id] = {}

        self.cache["post"][post_id]['posted'] = True