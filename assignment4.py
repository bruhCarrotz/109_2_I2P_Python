from pycategory import Categories 
from pyrecord import Records 
from tkinter import *
from tkinter import messagebox as mbox

cat = Categories()
fixedRecords = Records()

data = []

root = Tk()
root.geometry('450x200')
root.title('PyMoney')

'''display categories'''
listbox = Listbox(root, height=6, width=20)
listbox.grid(row=1,column=1)
WidgetNames = ['expense', 'food', 'meal', 'snack', 'drink', 'transportation', 'bus', 'railway', 'income', 'salary', 'bonus']       
listbox.insert(END,'List of categories:')
listbox.insert(END,*WidgetNames)

'''top'''
labelText=StringVar()
labelText.set("How much money do you have?")
labelDir=Label(root, textvariable=labelText)
labelDir.grid(row=0, column=0, sticky='W')

money = Entry(root,width=20)
money.grid(row=0, column=1)

start = Button(text="Ok", command = lambda: init())
start.grid(row=0, column=2)

'''list box'''
l = Listbox(root, height=6, width=45, selectmode=MULTIPLE)
l.grid(row=1,column=0)

'''new label'''
lbl = StringVar()
lbl.set("What would you like to do?")
labelz=Label(root, textvariable=lbl)
labelz.grid(row=2, column=0, sticky='W')

'''add box'''
addbox=Entry(root,width=25)
addbox.grid(row=3, column=0, sticky='W')

for i in range(1):
    gridframe = Frame(root)
    for j in range(1):
        Button(gridframe, text='Add', command= lambda: add()).pack(side=LEFT)
        Button(gridframe, text='Delete', command = lambda: delete()).pack(side=LEFT)
    gridframe.grid(row=3, column=i, sticky='E')

'''find box'''
findbox=Entry(root,width=25)
findbox.grid(row=4, column=0, sticky='W')

for i in range(1):
    gridframe = Frame(root)
    for j in range(1):
        Button(gridframe, text='Find', command = lambda: find()).pack(side=LEFT)
        Button(gridframe, text='Save', command = lambda: save()).pack(side=LEFT)
    gridframe.grid(row=4, column=i, sticky='E')

'''view button'''
viewbtn = Button(text="View", command = lambda: view())
viewbtn.grid(row=3, column=1, sticky='W')

'''quit button'''
quitbtn = Button(text="Quit", command = lambda: quit())
quitbtn.grid(row=4, column=1, sticky='W')

def quit():
    save()
    root.destroy()

def delete():
    select = l.curselection()
    for i in select[::-1]:
        l.delete(i)
        fixedRecords._records.pop(int(i)-1)
    save()

def add():
    data.clear()
    x = addbox.get()
    fixedRecords.add(x)
    if '/' in list(x):
        mbox.showerror('Wrong format!','The format of a date should be YYYY-MM-DD.\nFail to add a record.')
        del fixedRecords._records[-1]        
    view()
    for i in data:
        if i[1] not in WidgetNames:
            mbox.showerror('Wrong format!','Category is not found.\nFail to add a record.')
            del fixedRecords._records[-1]        
    save()
            
def save():
    fixedRecords.save()

def init():
    fixedRecords.__init__()
    try:
        x = int(money.get())
        fixedRecords._initialMoney = x
    except ValueError:
        mbox.showerror('Invalid value!','Invalid value. Please enter an integer.\nSet initial money to 0.')
    save()
    view()

def find():
    find_input = str(findbox.get())
    target_categories = cat.find_subcategories_gen(find_input)
    l.delete(0,END)
    l.insert(END, 'Here\'s your "{}" records:'.format(find_input))
    total = 0
    for w,x,y,z in data:
        if x in target_categories:
            test = '{:<14s}{:<20s}{:<15s}{:<8d}'.format(w,x,y,z)
            total += z
            result = int(fixedRecords._initialMoney) + int(total)
            l.insert(END, test)
    res = 'Now you have {} dollars.'.format(result)
    l.insert(END,res)

def view():
    data.clear()
    for i in fixedRecords._records:
        data.append([i._date, i._category, i._desc, i._amount])
    l.delete(0,END)
    l.insert(END,'Here\'s your expense and income records:')
    total = 0
    for w,x,y,z in data:
        test = '{:<14s}{:<20s}{:<15s}{:<8d}'.format(w,x,y,z)
        total += z
        result = int(fixedRecords._initialMoney) + int(total)
        l.insert(END, test)
    res = 'Now you have {} dollars.'.format(result)
    l.insert(END,res)

root.mainloop()