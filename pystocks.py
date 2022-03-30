import pandas_datareader
import datetime
import matplotlib.pyplot as plt
import bs4 as bs
import requests
import os
import StockNasdaq

STOCK_TYPE_SP500 = 0
STOCK_INDEX_DOWJONES = 1
STOCK_TOTAL_TYPE = 2


class StockInfo:
    def __init__(self, stock=None):
        web = pandas_datareader.data
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=5 * 365)
        self.__df = web.DataReader(stock, "yahoo", start, end)
        self.__df.reset_index(inplace=True)
        self.__df.set_index("Date", inplace=True)
        return

    def get_moving_average(self, num_of_days=100):
        self.__df['100ma'] = self.__df['Adj Close'].rolling(window=num_of_days).mean()
        return self.__df['100ma']

    def get_closing_price(self):
        return self.__df["Adj Close"]

    def get_volume(self):
        return self.__df["Volume"]


class StockView:
    def __init__(self, stockinfo=None):
        self.__stockinfo = stockinfo

    def show_stock_graph(self):
        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

        ax1.plot(self.__stockinfo.get_closing_price())
        ax1.plot(self.__stockinfo.get_moving_average())
        ax2.plot(self.__stockinfo.get_volume())

        plt.show()
        return


class StockList:
    def __init__(self, stock_type=0):
        self.__stock_type = int(stock_type)
        self.__stock_list_type = ['sp500', 'DowJones']
        self.__stock_list_link = ['http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                                  'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average']
        self.__stock_list_file = ['sp500_stocks.txt', 'dowjones_stocks.txt']
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
        txt_file = self.__stock_list_file[list_type]
        if os.path.isfile(txt_file):
            return True
        return False

    def __create_list_from_text_file(self):
        list_type = self.__stock_type
        txt_file = self.__stock_list_file[list_type]
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
        sp500_data_website = self.__stock_list_link[STOCK_TYPE_SP500]
        resp = requests.get(sp500_data_website)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})

        for row in table.findAll('tr')[1:]:
            stock = row.findAll('td')[0].text
            self.__stock_list.append(stock.strip())
        return

    def __create_dowjones_list_from_website(self):
        dowjones_data_website = self.__stock_list_link[STOCK_INDEX_DOWJONES]
        resp = requests.get(dowjones_data_website)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})

        for row in table.findAll('tr')[1:]:
            stock = row.findAll('td')[1].text
            self.__stock_list.append(stock.strip())
        return

    def __write_stock_list_to_file(self):
        list_type = self.__stock_type
        txt_file = self.__stock_list_file[list_type]
        file = open(txt_file, "w")
        for stock in self.__stock_list:
            file.write(stock + '\n')

def main():
    stock_filter = StockNasdaq.StockFilter()
    stock_filter.reset_filter()
    stock_filter.filter_by_country("United States")
    stock_filter.filter_by_sector("Technology")

    filtered_list = stock_filter.get_filtered_list()
    #for stock in filtered_list:
    #    print(stock.symbol, stock.name, stock.country, stock.sector, stock.industry)

    sp500_stock = StockList(stock_type=0)
    dowjones_stock = StockList(stock_type=1)
    sp500_stock_list = sp500_stock.get_stock_list()
    dowjones_stock_list = dowjones_stock.get_stock_list()

    print("*********** S&P 500 **************")
    print(sp500_stock_list)

    print("*********** DOW JONES **************")
    print(dowjones_stock_list)


    # stock = StockInfo(stocks[55])
    # view = StockView(stockinfo=stock)

    # view.show_stock_graph()


if __name__ == '__main__':
    main()
