import StockInfo
import StockMarketIndex
import StockNasdaq

def main():
    # stock_filter = StockNasdaq.StockFilter()
    # stock_filter.reset_filter()
    # stock_filter.filter_by_country("United States")
    # stock_filter.filter_by_sector("Technology")

    # filtered_list = stock_filter.get_filtered_list()
    # for stock in filtered_list:
    #    print(stock.symbol, stock.name, stock.country, stock.sector, stock.industry)

    sp500_stock = StockMarketIndex.StockMarketIndex(stock_type=0)
    dowjones_stock = StockMarketIndex.StockMarketIndex(stock_type=1)
    sp500_stock_list = sp500_stock.get_stock_list()
    dowjones_stock_list = dowjones_stock.get_stock_list()

    print("*********** S&P 500 **************")
    print(sp500_stock_list)

    print("*********** DOW JONES **************")
    print(dowjones_stock_list)

    stock = StockInfo.StockInfo(ticker="MSFT")
    view = StockInfo.StockView(stockinfo=stock)

    view.show_stock_graph()


if __name__ == '__main__':
    main()
