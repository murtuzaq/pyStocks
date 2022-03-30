import bs4 as bs
import requests
import os

STOCK_TYPE_SP500 = 0
STOCK_INDEX_DOWJONES = 1

STOCK_LIST_TYPE = ['sp500', 'DowJones']
STOCK_LIST_WEB_LINK = ['http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                       'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average']
STOCK_LIST_FILE_NAME = ['sp500_stocks.txt', 'dowjones_stocks.txt']


class StockMarketIndex:
    def __init__(self, stock_type=0):
        self.__stock_type = int(stock_type)
        self.__stock_list = []
        self.__create_stock_list()

    def get_stock_list(self):
        return self.__stock_list

    def __create_stock_list(self):
        if self.__does_stock_file_exist():
            self.__create_list_from_text_file()
            return

        self.__create_list_from_website()
        self.__write_stock_list_to_file()
        return

    def __does_stock_file_exist(self):
        list_type = self.__stock_type
        txt_file = STOCK_LIST_FILE_NAME[list_type]
        if os.path.isfile(txt_file):
            return True
        return False

    def __create_list_from_text_file(self):
        list_type = self.__stock_type
        txt_file = STOCK_LIST_FILE_NAME[list_type]
        with open(txt_file) as file:
            for line in file:
                self.__stock_list.append(line.strip())
        return

    def __create_list_from_website(self):
        if self.__stock_type == STOCK_TYPE_SP500:
            self.__create_sp500_list_from_website()
        else:
            self.__create_dowjones_list_from_website()
        return

    def __create_sp500_list_from_website(self):
        sp500_data_website = STOCK_LIST_WEB_LINK[STOCK_TYPE_SP500]
        resp = requests.get(sp500_data_website)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})

        for row in table.findAll('tr')[1:]:
            stock = row.findAll('td')[0].text
            self.__stock_list.append(stock.strip())
        return

    def __create_dowjones_list_from_website(self):
        dowjones_data_website = STOCK_LIST_WEB_LINK[STOCK_INDEX_DOWJONES]
        resp = requests.get(dowjones_data_website)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})

        for row in table.findAll('tr')[1:]:
            stock = row.findAll('td')[1].text
            self.__stock_list.append(stock.strip())
        return

    def __write_stock_list_to_file(self):
        list_type = self.__stock_type
        txt_file = STOCK_LIST_FILE_NAME[list_type]
        file = open(txt_file, "w")
        for stock in self.__stock_list:
            file.write(stock + '\n')
