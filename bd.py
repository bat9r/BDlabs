import pymysql

class DB:
    _conn = pymysql.connect(host='localhost', user='root', passwd=None, db='mysql')
    _nameDataBase = ""
    _nameTable = ""

    def __init__(self, whereGetInfo):
        cur = self._conn.cursor()
        if (whereGetInfo == "new"):
            columnsNames = []
            name = input("Write name DB: ")
            nameTable = input("Write name table: ") 
            countColumns = int(input("How many columns? " ))
            for row in range(countColumns):
                columnsNames.append(input("Name column and type #"+str(row)+" : "))
            valTypesStr = ",".join(columnsNames)
            cur.execute("CREATE DATABASE "+name+";")
            cur.execute("use "+name+";")
            cur.execute("CREATE TABLE "+nameTable+"("+valTypesStr+");")
            self._nameDataBase = name
            self._nameTable = nameTable
        else:
            cur.execute("use "+whereGetInfo+";")
            self._nameTable = input("Write name table: ") 
            self._nameDataBase = whereGetInfo

        cur.close()

    def closeConn(self):
        saves = input("Save changes? (y/n) ")
        if (saves=="y"):
            self._conn.commit()
        self._conn.close()

    def getAllTableLikeMatrix(self):
        cur = self._conn.cursor()
        cur.execute("use "+self._nameDataBase+";")
        res=[[]]

        cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '"+self._nameDataBase+"' AND table_name ='"+self._nameTable+"';")
        for i in cur:
            cols = i[0]

        cur.execute("SELECT * FROM "+self._nameTable+";")
        it=0
        for r in cur:
            for i in range(cols):
                res[it].append(str(r[i]))
            res.append([])
            it+=1
        res.remove([])
        
        cur.close()
        return res

    def printAll(self):
        cur = DB.getAllTableLikeMatrix(self)
        empty = []
        if (cur==empty):
            print("empty")
        for r in cur:
            print(r)

    def findById(self,value):
        cur = self._conn.cursor()
        cur.execute("use "+self._nameDataBase+";")
        cur.execute("SELECT * FROM "+self._nameTable+" WHERE id = "+str(value)+";")
        row=[]
        for i in cur:
            for j in i:
                row.append(j)
        print (row)
        cur.close()

    def deleteById(self,value):
        cur = self._conn.cursor()
        cur.execute("use "+self._nameDataBase+";")
        cur.execute("DELETE FROM "+self._nameTable+" WHERE id = "+str(value)+";")
        cur.close()

    def updateById(self,setId):
        cur = self._conn.cursor()
        column = input("Column - ")
        value = input("Value - ")
        cur.execute("use "+self._nameDataBase+";")
        cur.execute("UPDATE "+self._nameTable+" SET "+str(column)+"='"+str(value)+"' WHERE id = "+str(setId)+";")
        cur.close()

    def insertFromUser(self):
        cur = self._conn.cursor()
        cur.execute("use "+self._nameDataBase+";")
        cur.execute("SHOW COLUMNS FROM "+self._nameTable+";")
        
        #<UaStyle>> 
        colsNamesList = []
        colsValsList = []
        cur.execute("SELECT COUNT(*) FROM "+self._nameTable+";")
        for j in cur:
            rows = j[0]
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '"+self._nameDataBase+"' AND table_name ='"+self._nameTable+"';")
        for r in cur:
            colsNamesList.append(str(r[0]))
        colsNamesStr = ",".join(colsNamesList)
        for t in colsNamesList:
            temp = input(str(t)+" - ")
            try:
                int(temp)
            except ValueError:
                temp = "'"+temp+"'"
            colsValsList.append(str(temp))
        colsValsStr = ",".join(colsValsList)
        cur.execute("INSERT INTO "+self._nameTable+" ("+colsNamesStr+") VALUES ("+colsValsStr+");")
        #</UaStyle>

        cur.close()

class menu:
    def __init__(self):
        pass

    def mainLoop(self, obj):
        print(" 'p' - print table \n 'f' - find by id \n 'i' - insert \n 'd' - delete by id \n 'u' - update by id \n 'h' - help \n 'e' - exit \n")
        while True:
            cmd = input("-> ")
            if (cmd=="p"):
                obj.printAll()
            if (cmd=="f"):
                obj.findById(int(input("ID - ")))
            if (cmd=="i"):
                obj.insertFromUser()
            if (cmd=="d"):
                obj.deleteById(int(input("ID - ")))
            if (cmd=="u"):
                obj.updateById(int(input("ID - ")))
            if (cmd=="h"):
                print(" 'p' - print table \n 'f' - find by id \n 'i' - insert \n 'd' - delete by id \n 'u' - update by id \n 'h' - help \n 'e' - exit \n")
            if (cmd=="e"):
                break

if __name__ == "__main__":
    mainMenu = menu()
    database = DB(input("Write DB for open or 'new' for create "))    
    
    mainMenu.mainLoop(database)
    
    database.closeConn()
    del database
