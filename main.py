from DBcm import UseDatabase
from prettytable import PrettyTable

class MyWorkList:
    '''Класс, создающий списко работ'''
    def __init__(self):
        #Конфигурация для подключения к базе данных
        self.connection = {'user': 'postgres',
                           'password': '111111',
                           'host': '127.0.0.1',
                           'port': '5432',
                           'database': 'WorkList'}

        with UseDatabase(self.connection) as cursor:
            #Создание базы данных при первичной инициализации
            try:
                _SQL = '''CREATE TABLE test
                         (ID                    SERIAL,
                          VERSION               INT,
                          NAME                  TEXT,
                          START                 TEXT,
                          FINISH                TEXT); '''
                cursor.execute(_SQL)
            #Если бпзп данных уже существует, то ловим ошибку и идём дальше
            except Exception:
                pass

    def show(self, th, td):
        #Для табличного вывода в консоль
        table = PrettyTable(th)  # Определяем таблицу.
        for x in td:
            x = list(x)
            table.add_row(x)
        print(table)  # Печатаем таблицу

    def get_works(self):
        #Метод выводит список всех работ с последними версиями изменений
        with UseDatabase(self.connection) as cursor:
            _SQL = '''SELECT VERSION, NAME, START, FINISH 
                      FROM TEST WHERE VERSION = (SELECT MAX(VERSION) 
                      FROM TEST AS T WHERE T.NAME = TEST.NAME);'''
            cursor.execute(_SQL)
            new_work_list = cursor.fetchall()
            table_name = ['Версия', 'Название', 'Начало работ', 'Окончание работ']
            self.show(table_name, new_work_list)

    def set_work(self):
        #Метод  создаёт работу с нулевой версией, если она не была до этого создана
        name = input('Название: ')
        start = input('Начало работы: ')
        finish = input('Завершение работы: ')
        with UseDatabase(self.connection) as cursor:
            _SQL = '''SELECT NAME FROM test WHERE NAME = '{}'; '''.format(name)
            cursor.execute(_SQL)
            get_name = cursor.fetchall()
            if get_name:
                print('Такая работа уже создана')
            else:
                version = 0
                _SQL = '''INSERT INTO test
                          (VERSION, NAME, START, FINISH)
                          VALUES (%s,%s,%s,%s);'''
                cursor.execute(_SQL, (version, name, start, finish))

    def update_work(self):
        # Метод орбнавляет существующую раюботу, также изменяя версию
        name = input('Название: ')
        start = input('Новый срок начала работы: ')
        finish = input('Новый срок завершения работы: ')
        with UseDatabase(self.connection) as cursor:
            _SQL = '''SELECT MAX(VERSION) FROM test WHERE NAME = '{}'; '''.format(name)
            cursor.execute(_SQL)
            version = cursor.fetchall()
            if version:
                version = version[0][0]
                version += 1
                _SQL = '''INSERT INTO test
                      (VERSION, NAME, START, FINISH)
                      VALUES (%s,%s,%s,%s);'''
                cursor.execute(_SQL, (version, name, start, finish))
            else:
                print('Такой работы нет')

    def delete_work(self):
        #Метод удаляет все версии работы из базы данных
        name = input('Название: ')
        with UseDatabase(self.connection) as cursor:
            _SQL = '''DELETE FROM test WHERE NAME = '{}'; '''.format(name)
            cursor.execute(_SQL)

    def all_versions(self):
        #Метод выводлит все версии работы по её названию
        name = input('Название: ')
        with UseDatabase(self.connection) as cursor:
            _SQL = '''SELECT VERSION, NAME, START, FINISH FROM test WHERE NAME = '{}'; '''.format(name)
            cursor.execute(_SQL)
            new_work_list = cursor.fetchall()
            table_name = ['Версия', 'Название', 'Начало работ', 'Окончание работ']
            self.show(table_name, new_work_list)

    def one_version(self):
        # Метод выводлит конкретную версию раюоты по её названию
        name = input('Название: ')
        version = input('Версия: ')
        with UseDatabase(self.connection) as cursor:
            _SQL = '''SELECT VERSION, NAME, START, FINISH FROM test WHERE NAME = '{}' AND VERSION = {}; '''.format(name,version)
            cursor.execute(_SQL)
            new_work_list = cursor.fetchall()
            table_name = ['Версия', 'Название', 'Начало работ', 'Окончание работ']
            self.show(table_name, new_work_list)


WorkList = MyWorkList()

print('1: Получить список работ')
print('2: Создать работу')
print('3: Обновить работу')
print('4: Удалить работу')
print('5: Получение всех версий работы')
print('6: Получение работы по определенной версии')

while True:
    step = int(input('Выберите действие: '))

    if step == 1:
        WorkList.get_works()
    elif step == 2:
        WorkList.set_work()
    elif step == 3:
        WorkList.update_work()
    elif step == 4:
        WorkList.delete_work()
    elif step == 5:
        WorkList.all_versions()
    elif step == 6:
        WorkList.one_version()
