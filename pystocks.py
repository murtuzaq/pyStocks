import pandas_datareader
import datetime
import matplotlib.pyplot as plt
import StockMarketIndex
import StockNasdaq

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



def main():
    #stock_filter = StockNasdaq.StockFilter()
    #stock_filter.reset_filter()
    #stock_filter.filter_by_country("United States")
    #stock_filter.filter_by_sector("Technology")

    #filtered_list = stock_filter.get_filtered_list()
    #for stock in filtered_list:
    #    print(stock.symbol, stock.name, stock.country, stock.sector, stock.industry)

    sp500_stock = StockMarketIndex.StockMarketIndex(stock_type=0)
    dowjones_stock = StockMarketIndex.StockMarketIndex(stock_type=1)
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
