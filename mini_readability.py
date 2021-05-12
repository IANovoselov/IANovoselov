from bs4 import BeautifulSoup
import requests, os
from fake_useragent import UserAgent

link = input('Enter link: ')


class Filtr():
    def __init__(self, link):
        self.link = link
        self.out_put = []
        self.response = requests.get(self.link, headers={'User-Agent': UserAgent().chrome})
        self.response.encoding = 'utf-8'
        self.soup = BeautifulSoup(self.response.text, 'lxml')

    def fname(self):
        '''формируется имя файла по текущей директории + ссылка на статью'''
        return os.getcwd().replace('\\','_')+'_'+link.split('//')[1].replace('/','_') + '.txt'

    def href_getter(self, string):
        '''вытаскивает ссылки из контента, далее формируется словарь, где ключь - текст, а значение -
        ссылка для этого текста, в исходном контенте гиперссылки заменяются на текст + [ссылка]'''
        href_dict = {}
        string2 = string.text
        for a in string.find_all('a'):
            href_dict[a.text] = a['href']
        for key, value in href_dict.items():
            if key in string2:
                string2 = string2.replace(key, key + ' [{}]'.format(value))
        return string2

    def content_p(self, div):
        '''если в div более 2 p, то метод вытаскивыет текстовую информацию, предварительно вставив ссылки'''
        if 2 < len(div.find_all('p')) < 9:
            for p in div.find_all('p'):
                p = self.href_getter(p)
                self.out_put.append(p)
        return self.out_put

    def content_div(self, div):
        '''аналогично content_p, работает, если текст расположен в div'''
        if 100 < len(div.text) < 400:
            div = self.href_getter(div)
            self.out_put.append(div)
        return self.out_put

    def part_of_strings(self, string):
        '''возвращает строку длиной не более 80 символов'''
        if len(string) > 80:
            if string[80] == ' ':
                return string[0:80]
            else:
                for i in range(79, 0, -1):
                    if string[i] == ' ':
                        return string[0:i]
        else:
            return string

    def writer(self, string, file_name):
        '''принимает строку, делит на подстроки с помощью метода part_of_strings() и записывает в файл, отбивая абзац пустой строкой'''
        while string != '':
            ans = (self.part_of_strings(string))
            print(ans, file=file_name, end='\n')
            if len(ans) == len(string):
                string = ''
            else:
                string = string[len(ans):].lstrip()

    def finder(self):
        '''главный метод, осуществляет поиск таких эдементов разметки html, как article, div , p'''
        answer = []
        if self.soup.find('article'):
            for div in self.soup.find_all('article'):
                answer.extend(self.content_p(div))
            if len(answer) == 0:
                for div in self.soup.find_all('article'):
                    answer.extend(self.content_div(div))
        else:
            for div in self.soup.find_all('div'):
                answer.extend(self.content_p(div))
            if len(answer) == 0:
                for div in self.soup.find_all('div'):
                    answer.extend(self.content_div(div))

        new_out = []
        for x in answer:
            if x not in new_out and ('\n' or '\r' or '\t') not in x: #исключаем оставшися мусор по типу "\t\n\n\n\Подпишись!"
                new_out.append(x)

        with open(self.fname(), 'w') as fl: #открываем файл, записываем информацию
            self.writer(self.soup.title.text, fl)
            print('\n', file=fl, end='')
            for x in new_out:
                self.writer(x, fl)
                print('\n', file=fl, end='')


one = Filtr(link)
one.finder()
