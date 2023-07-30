"""**************************************************************
*   Desciribe:                                                  *
*       The function to acess database                          *
*                                                               *
*   Date    : 2023/07/29                                        *
*   Author  : YongHong, Liu                                     *
*                                                               *
**************************************************************"""
#======import part=================================================================================
import sqlite3

#==================================================================================================
#======variable declare============================================================================


#==================================================================================================
#======function declare============================================================================
class DataBase():
    def __init__(self):
        self.conn = sqlite3.connect('db/myLinebot.db')
        print ("資料庫連線成功")
        self.c = self.conn.cursor()
    #-------------------------------------------------------------------------
    def __del__(self):
        self.conn.close()
        print("close db connection")
    #-------------------------------------------------------------------------
    def createUserTable(self):
        self.c.execute('''CREATE TABLE USERS(
            USER_ID TEXT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            PERMISSIONS            CHAR(32)     NOT NULL
            )''') 
        print ("Table 建立成功")
        self.conn.commit()

    #-------------------------------------------------------------------------
    def queryPermissions(self, userid):
        sql="""SELECT u.NAME, u.PERMISSIONS FROM USERS u
        WHERE USER_ID = ?""".format(userid)
        print(userid)
        print(sql)
        results = self.c.execute(sql)
        ret = results.fetchone()
        return ret
        # if ret is not None:
        #         return ret
        #     else:
        #         return None
    #-------------------------------------------------------------------------
    def addPermissions(self, userid, name, permissions):
        if self.queryPermissions(userid) is None:
            sql="""INSERT INTO USERS(USER_ID, NAME, PERMISSIONS)
                VALUES (?, ?, ?)""".format(userid,name, permissions)
            self.c.execute(sql)
            self.conn.commit()
            return "註冊成功!"
        else:
            return "已經註冊過了!"

#==================================================================================================
#==================================================================================================