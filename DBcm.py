import psycopg2


class DataBaseError(Exception):
    pass


class DataBaseDouble(Exception):
    pass


class UseDatabase:
    '''Диспетчер контекста для работы с базой данных'''
    def __init__(self, config: dict):
        self.configuration = config

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(**self.configuration) #установка соединения
            self.cursor = self.conn.cursor()                   #открытие курсора
            return self.cursor
        except psycopg2.Error as err:
            raise DataBaseError(err)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit() #коммит изменения
        self.cursor.close()#закрытие соединения
        self.conn.close()
        if exc_type is psycopg2.errors.DuplicateTable:
            print('Таблица уже существует')
            raise DataBaseDouble
        elif exc_type:
            raise exc_type(exc_val)


