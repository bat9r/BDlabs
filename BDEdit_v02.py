import pymysql
from tkinter import *

#Cursor for working with database
_conn = pymysql.connect(host='localhost', user='root', passwd='', db='mysql')
_nameDataBase = ""
_nameTable = ""

class MainGUI():
    #class vars
    _rowIndes = 0
    _colName = ''

    def __init__(self):
        #Settings of Window
        self.root = Tk()
        self.root.title('BDEdit')
        self.root.geometry('1200x530')

        #TODO delete global varible closeWindow in ChangerGUI
        global _MainGUISelf
        _MainGUISelf = self

        #Create frames (flexible grid)
        self.topMenuFrame = Frame(self.root, height=30, bg='lightgrey')
        self.rigthMenuFrame = Frame(self.root, height=340, width=200, bg ='lightblue')
        self.textFrame = Frame(self.root, height=500, width=1000)
        self.textTopFrame = Frame(self.textFrame, height=400, width=1000, bg='white')
        self.textBottomFrame = Frame(self.textFrame, height=50, width=1000, bg='lightgrey')

        #Pack frames
        self.topMenuFrame.pack(side='top', fill='x')
        self.rigthMenuFrame.pack(side='right', fill='both', expand=1)
        self.textFrame.pack(side='left', fill='both', expand=1)
        self.textTopFrame.pack(fill='both', expand=1)
        self.textBottomFrame.pack(fill='both')

        #Create and pack buttons for right menu
        self.findButton = Button(self.rigthMenuFrame, text='Find')
        self.findButton.bind('<Button-1>', self.findById)
        self.findButton.bind('<Control-f>', self.findById)
        self.findButton.pack(side='top', fill='x')

        self.insertButton = Button(self.rigthMenuFrame, text='Insert')
        self.insertButton.bind('<Button-1>', self.insertById)
        self.insertButton.bind('<Control-i>', self.insertById)
        self.insertButton.pack(side='top', fill='x')

        self.deleteButton = Button(self.rigthMenuFrame, text='Delete')
        self.deleteButton.bind('<Button-1>', self.deleteById)
        self.deleteButton.bind('<Control-d>', self.deleteById)
        self.deleteButton.pack(side='top', fill='x')

        self.updateButton = Button(self.rigthMenuFrame, text='Update')
        self.updateButton.bind('<Button-1>', self.updateById)
        self.updateButton.bind('<Control-u>', self.updateById)
        self.updateButton.pack(side='top', fill='x')

        #Create and pack buttons for top menu
        self.openButton = Button(self.topMenuFrame, text='Open')
        self.openButton.bind('<Button-1>', self.openDB)
        self.openButton.bind('<Shift-Up>', self.openDB)
        self.openButton.pack(side='left', fill='y')

        self.saveButton = Button(self.topMenuFrame, text='Save')
        self.saveButton.bind('<Button-1>', self.saveDB)
        self.saveButton.bind('<Control-s>', self.saveDB)
        self.saveButton.pack(side='left', fill='y')

        #Create bootom text for input info
        self.textBottomBox = Text(self.textBottomFrame, height=1)
        self.textBottomBox.insert('1.0', "Input information...")
        self.textBottomBox.bind('<Button-1>', self.clearTextBottomBox)
        self.textBottomBox.pack(side='left', fill='x', expand=1)

        #Call func
        try:
            self.printAll()
        except pymysql.err.ProgrammingError:
            print ('Error')

        #Root mainloop
        self.root.mainloop()

    #For scrol main output (do not delete and replace)
    def OnVsb(self, *args):
        #Get columns count
        cur = _conn.cursor()
        cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '"+_nameDataBase+"' AND table_name ='"+_nameTable+"';")
        for i in cur:
            colsCount = i[0]
        #Scrolling
        for y in range(colsCount):
            self.columnsListboxes[y].yview(*args)
        cur.close()

    def clearTextBottomBox(self, event):
        self.textBottomBox.delete('1.0', 'end')

    def getSelectedIndex(self, event):
        #Catch user click choose row and column
        index = int(event.widget.curselection()[0])
        global _rowIndex
        _rowIndex = index-1
        global _colName
        _colName = ''.join(event.widget.get(0))

    def printAll(self):
        #Get table from DB and translate to matrix(res)
        cur = _conn.cursor()
        print(_nameDataBase)
        cur.execute("use "+_nameDataBase+";")
        res=[[]]
        #Get count of columns
        cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '"+_nameDataBase+"' AND table_name ='"+_nameTable+"';")
        for i in cur:
            colsCount = i[0]
        #Get table and transform it to matrix
        cur.execute("SELECT * FROM "+_nameTable+";")
        it=0
        for r in cur:
            for i in range(colsCount):
                res[it].append(str(r[i]))
            res.append([])
            it+=1
        res.remove([])
        #Sort res
        res = sorted(res ,key = lambda row: int(row[0]), reverse=True)
        #Get count of rows
        cur.execute("SELECT COUNT(*) FROM "+_nameTable+";")
        for j in cur:
            rowsCount = j[0]
        #Print names of columns
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '"+_nameDataBase+"' AND table_name ='"+_nameTable+"';")
        colsNamesList = []
        for r in cur:
            colsNamesList.append(str(r[0]))
        print (colsNamesList)
        #Kill textTopFrame childrens <3
        try:
            self.vsb.destroy()
        except AttributeError:
            print('killing vsb')
        for child in self.textTopFrame.winfo_children():
            child.destroy()
        #Create Listbox columns
        self.vsb = Scrollbar(orient="vertical", command = self.OnVsb)
        self.columnsListboxes = []
        for colsIndex in range(colsCount):
            self.columnsListboxes.append(Listbox(self.textTopFrame, selectmode='BROWSE', bd=0, yscrollcommand=self.vsb.set ))
        self.vsb.pack(side="right",fill="y")
        for colsIndex in range(colsCount):
            self.columnsListboxes[colsIndex].pack(side='left', fill='both')
        for colsIndex in range(colsCount):
            self.columnsListboxes[colsIndex].insert(0,colsNamesList[colsIndex])
            self.columnsListboxes[colsIndex].insert(1,"---"*30)
            for rowsIndex in range(rowsCount):
                self.columnsListboxes[colsIndex].insert(2,res[rowsIndex][colsIndex])
            self.columnsListboxes[colsIndex].bind('<<ListboxSelect>>', self.getSelectedIndex)

        cur.close()

    def findById(self, event):
        pass

    def insertById(event):
        pass

    def updateById(self, event):
        cur = _conn.cursor()
        cur.execute("use "+_nameDataBase+";")
        #Some thinks about value, this guy returns for us one extra character we cut this bastard
        value = str(self.textBottomBox.get('1.0', 'end'))[:-1]
        cur.execute("UPDATE "+_nameTable+" SET "+_colName+"='"+value+"' WHERE id = "+str(_rowIndex)+";")
        self.printAll()
        cur.close()

    def deleteById(self, event):
        cur = _conn.cursor()
        cur.execute("use "+_nameDataBase+";")
        cur.execute("DELETE FROM "+_nameTable+" WHERE id = "+str(_rowIndex)+";")
        self.printAll()
        cur.close()

    def saveDB(self, event):
        _conn.commit()

    def openDB(self, event):
        #Do it like a boss, destroy and create all
        changerGUI = ChangerGUI()


class ChangerGUI(MainGUI):
    def __init__(self):
        #Open cursor
        self.cursor = _conn.cursor()

        #Create root window
        self.root = Toplevel()
        self.root.title('Select')
        self.root.geometry('300x200')

        #Bind widgets
        self.databasesListBox = Listbox(self.root, selectmode='BROWSE', name='databasesListBox')
        self.databasesListBox.place(x=10, y=10, width=135, height=160)

        self.tablesListBox = Listbox(self.root, selectmode='BROWSE', name='tablesListBox')
        self.tablesListBox.place(x=150, y=10, width=135, height=160)

        self.chooseButton = Button(self.root, text='Choose')
        self.chooseButton.bind('<Button-1>', self.closeWindow)
        self.chooseButton.pack(side='bottom')

        #Call functions
        self.selectDB()

    def changeDB(self, event):
        #Catch user click choose DB
        index = int(event.widget.curselection()[0])
        global _nameDataBase
        _nameDataBase = ''.join(event.widget.get(index))
        self.cursor.execute('use '+ _nameDataBase+';')
        #Call function selectTable after selecting DB
        self.selectTable()
        print(_nameDataBase)

    def changeTable(self, event):
        #Catch user click choose table
        index = int(event.widget.curselection()[0])
        global _nameTable
        _nameTable = ''.join(event.widget.get(index))
        print(_nameTable)

    def selectDB(self):
        #Create list with names of databases
        databasesList = []
        #Create box
        self.cursor.execute("show databases;")
        for i in self.cursor:
            databasesList.append(i)
        #Insert in databasesListBox
        for item in databasesList:
            self.databasesListBox.insert(END, item)
        self.databasesListBox.bind('<<ListboxSelect>>', self.changeDB)

    def selectTable(self):
        #Clear box after select new DB
        self.tablesListBox.delete(0,END)
        #Create list with names of tables
        tablesList = []
        #Create box select table
        self.cursor.execute("show tables;")
        for i in self.cursor:
            tablesList.append(i)
        #Insert in tablesListBox
        for item in tablesList:
            self.tablesListBox.insert(END, item)
        self.tablesListBox.bind('<<ListboxSelect>>', self.changeTable)

    def closeWindow(self, event):
        #Close root window
        self.root.destroy()
        MainGUI.printAll(_MainGUISelf)

def main():
    mainGUI = MainGUI()
    #ChangerGUI = ChangerGUI()

if __name__ == "__main__":
    main()
