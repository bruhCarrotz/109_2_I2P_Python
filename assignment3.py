class Record:
    """Represent a record."""
    def __init__(self,category,desc,amount):
        self._category = category
        self._desc = desc
        self._amount = int(amount)
    @property
    def amount(self):
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """A function that reads the saved .txt file when the program starts."""
        self._initialMoney = 0
        self._records = []
        try:
            with open(file='records.txt',mode='r') as fh:
                for i in fh.readlines():
                    if ' ' not in i:
                        self._initialMoney = int(i.strip())
                    else:
                        lines = i.strip()
                        category, desc, amount = lines.split(' ')
                        self._records.append(Record(category, desc, amount))
                print('Welcome back!')
        except OSError:
            x = input('How much money do you have? ')
            if x.isnumeric():
                self._initialMoney = int(x)
            else:
                print('Invalid value for money. Set to 0 by default.')
                self._initialMoney = 0
                self._records = []
        except ValueError:
            x = input('How much money do you have? ')
            self._initialMoney = x
            self._records = []

    def add(self,record):
        """A function that allows user to type input to add expenses or income."""
        try:
            category, desc, amount = record.split(' ')
            if cat.is_category_valid(category) == True:
                self._records.append(Record(category,desc,amount))
            else:
                print('The specified category is not in the category list.')
                print('You can check the category list by command "view categories".')
                print('Fail to add a record.')
        except ValueError:
            if ' ' not in record:
                print('The format of a record should be like this: breakfast -50.\nFail to add a record.')
            else:
                print('Invalid money. Fail to add a record.')
                
    def view(self):
        """A function that allows the user to view all the recorded records."""
        total = 0
        print('Here\'s your expense and income records:')
        print('Num      Category         Description        Expense/Income')
        print('===========================================================')
        for i,j in enumerate(self._records):
            cat = j._category
            desc = j._desc
            exp = j._amount
            print('{idx:<9d}{Cat:<17s}{Desc:<19s}{Exp}'.format(idx=i+1,Cat=cat,Desc=desc,Exp=exp))
            total = total + exp
        print('===========================================================')
        result = int(self._initialMoney) + int(total)
        print('Now you have {} dollars.'.format(result))
        return

    def delete(self, num):
        """A function that allows the user to delete specific records."""
        try:
            self._records.pop(int(num)-1)
            print('Item deleted!')
            return
        except ValueError:
            print('The format of deletion should be like this: breakfast 1\nFail to delete a record.')
            return
        except IndexError:
            print('There\'s no record \'{}\' found in {}th order. Fail to delete a record.'.format(wantDelete,num))
            return

    def save(self):
        """A function that allows the user to save the records to a txt file."""
        new = []
        with open(file='records.txt', mode='w') as fh:
            fh.write(str(self._initialMoney) + '\n')
            for i in self._records:
                   new.append([i._category, i._desc, i._amount])
            for i in range(len(new)):
                line = '{} {} {}\n'.format(new[i][0], new[i][1], new[i][2])
                fh.writelines(line)
        return

    def find(self):
        """A function that allows the user to find a certain records according to their categories or subcategories."""
        total = 0
        print('Here\'s your expense and income records under category "{}":'.format(find_input))
        print('Num      Category         Description        Expense/Income')
        print('===========================================================')
        for i,j in enumerate(self._records):
            cat = j._category
            desc = j._desc
            exp = j._amount
            if cat in target_categories:
                print('{idx:<9d}{Cat:<17s}{Desc:<19s}{Exp}'.format(idx=i+1,Cat=cat,Desc=desc,Exp=exp))
                total = total + exp
        print('===========================================================')
        result = int(self._initialMoney) + int(total)
        print('Now you have {} dollars.'.format(result))
        return

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """A function that initialize the list of categories."""
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
 
    def view(self):
        """A function that displays the list of categories with its subcategories."""
        def init_cat(catlist,level=0):
            if type(catlist) in {list,tuple}:
                for i in catlist:
                    init_cat(i,level+1)
            else:
                print(f'{" "*2*level}{catlist}')
        self._catlist = self._categories
        init_cat(self._catlist)

    def is_category_valid(self,category):
        """A function that checks whether the target category is in the list of categories."""
        def check(x, string):
            if not x:
                return False
            return x[0] == string or check(x[1:], string) 
        categories = ['expense', 'food', 'meal', 'snack', 'drink', 'transportation', 'bus', 'railway', 'income', 'salary', 'bonus']       
        self._check = check(categories, category)
        return self._check

    def find_subcategories_gen(self,category):
        """A generator which finds the target category in a list of categories."""
        def find_sub(category, categories, found=False):
            if type(categories) == list and found == False:
                for index, child in enumerate(categories):
                    yield from find_sub(category, child, False)
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        yield from find_sub(category, categories[index+1], True)
            else:
                if categories == category or found == True:
                    if type(categories) != list:
                        cat_gen.append(categories)
                    else:
                        for i in categories:
                            if type(i) != list:
                                cat_gen.append(i)
                            else:
                                for j in i:
                                    if type(j)!=list:
                                        cat_gen.append(j)
                    yield cat_gen
        cat_gen = []
        self._find = [i for i in find_sub(category, self._categories)][0]
        self.__init__()
        return self._find


import sys

cat = Categories()
fixedRecords = Records()

while True:
    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if command == 'add':
        record = input('Add an expense or income record with category, description, and amount (separate by spaces):\n')
        fixedRecords.add(record)
        continue
    if command == 'view':
        fixedRecords.view()
        continue
    if command == 'delete':
        wantDelete, num = input('Which record do you want to delete? (format: description num)\n').split(' ')
        fixedRecords.delete(num)
        continue
    if command == 'view categories':
        cat.view()
        continue
    if command == 'find':
        find_input = input('Which category do you want to find? ')
        target_categories = cat.find_subcategories_gen(find_input)
        fixedRecords.find()
        continue
    if command == 'exit':
        fixedRecords.save()
        break
    sys.stderr.write('Invalid command. Try again.\n')