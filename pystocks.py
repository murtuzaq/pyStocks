import pandas_datareader
import datetime
import matplotlib.pyplot as plt
import bs4 as bs
import requests
import os
import StockNasdaq
STOCK_TYPE_SP500 = 0
STOCK_TOTAL_TYPE = 1





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
    def __init__(self):
        self.__stock_list_type = ['sp500']
        self.__stock_list_link = ['http://en.wikipedia.org/wiki/List_of_S%26P_500_companies']
        self.__stock_list_file = ['sp500_stocks.txt']
        self.__stock_sp500 = []

        self.__get_sp500_list()

    def get_sp500_stocks(self):
        return self.__stock_sp500

    def __get_sp500_list(self):
        if self.__does_sp500_file_exist():
            self.__get_sp500_list_from_file()
            return

        self.__get_sp500_list_from_website()
        self.__write_sp500_list_to_file()
        return

    def __does_sp500_file_exist(self):
        sp500_txt_file = self.__stock_list_file[STOCK_TYPE_SP500]
        if os.path.isfile(sp500_txt_file):
            return True
        return False

    def __get_sp500_list_from_file(self):
        sp500_txt_file = self.__stock_list_file[STOCK_TYPE_SP500]
        with open(sp500_txt_file) as file:
            for line in file:
                self.__stock_sp500.append(line.strip())
        return

    def __get_sp500_list_from_website(self):
        sp500_data_website = self.__stock_list_link[STOCK_TYPE_SP500]
        resp = requests.get(sp500_data_website)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})

        for row in table.findAll('tr')[1:]:
            stock = row.findAll('td')[0].text
            self.__stock_sp500.append(stock.strip())
        return

    def __write_sp500_list_to_file(self):
        sp500_txt_file = self.__stock_list_file[STOCK_TYPE_SP500]
        file = open(sp500_txt_file, "w")
        for stock in self.__stock_sp500:
            file.write(stock + '\n')


def main():
    stock_filter = StockNasdaq.StockFilter()
    stock_filter.reset_filter()
    stock_filter.filter_by_country("United States")
    stock_filter.filter_by_sector("Technology")

    filtered_list = stock_filter.get_filtered_list()
    for stock in filtered_list:
        print(stock.symbol, stock.name, stock.country, stock.sector, stock.industry)

    #stock_list = StockList()
    #stocks = stock_list.get_sp500_stocks()

    #stock = StockInfo(stocks[55])
    #view = StockView(stockinfo=stock)

    #view.show_stock_graph()


if __name__ == '__main__':
    main()
