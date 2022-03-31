import pandas_datareader
import datetime
import matplotlib.pyplot as plt
import os

STOCK_DATA_DIRECTORY = "/stock_data"


class StockDataDescription:
    def __init__(self, date=None,
                 high=None,
                 low=None,
                 close=None,
                 volume=None):
        self.__date = date
        self.__high = high
        self.__low = low
        self.__close = close
        self.__volume = volume


class StockInfo:
    def __init__(self, ticker=None):
        self.__stock_dir_path = os.getcwd() + STOCK_DATA_DIRECTORY
        self.__stock_ticker = ticker
        self.__stock_closing_adj_price = []
        self.__stock_volume = []
        self.__stock_date = []
        self.__stock_data = []

        self.__get_stock_data()
        return

    def __get_stock_data(self):
        if self.__get_stock_data_from_text_file() is True:
            return

        self.__get_stock_data_from_web()

    def __get_stock_data_from_web(self):
        web = pandas_datareader.data
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=5 * 365)
        self.__df = web.DataReader(self.__stock_ticker, "yahoo", start, end)

        save_to_file = self.__stock_dir_path + \
                       "/" + \
                       self.__stock_ticker + \
                       datetime.datetime.today().strftime('-%Y-%m-%d') + \
                       ".csv"
        self.__df.to_csv(save_to_file)

        self.__stock_closing_adj_price = self.__df['Adj Close']
        self.__stock_volume = self.__df["Volume"]

        print(self.__df.columns.values)

    def __get_stock_data_from_text_file(self):
        if self.__does_stock_data_directory_exist() is False:
            self.__create_stock_data_directory()
            return False

        for file in os.listdir(self.__stock_dir_path):
            ticker_signature = self.__stock_ticker + "-"
            if file.startswith(self.__stock_ticker + "-"):
                date_string = file.replace(ticker_signature, '')
                date_string = date_string.replace(".csv", '')
                date_time_file = datetime.datetime.strptime(date_string, '%Y-%m-%d')
                date_time_now = datetime.datetime.now()
                if (date_time_now - date_time_file).days > 30:
                    os.remove(file)
                    return False
                else:
                    return True

        return False

    def get_moving_average(self, num_of_days=100):
        self.__df['100ma'] = self.__df['Adj Close'].rolling(window=num_of_days).mean()
        return self.__df['100ma']

    def get_closing_price(self):
        return self.__df["Adj Close"]

    def get_volume(self):
        return self.__df["Volume"]

    def __does_stock_data_directory_exist(self):
        isExist = os.path.exists(self.__stock_dir_path)
        if isExist is True:
            return True
        return False

    def __create_stock_data_directory(self):
        os.makedirs(self.__stock_dir_path)
        return


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
