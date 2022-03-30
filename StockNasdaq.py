import csv


# https://www.nasdaq.com/market-activity/stocks/screener

class StockDescription:
    def __init__(self,
                 symbol=None,
                 name=None,
                 last_sale=None,
                 net_change=None,
                 percent_change=None,
                 market_cap=None,
                 country=None,
                 ipo_year=None,
                 volume=None,
                 sector=None,
                 industry=None):
        self.symbol = symbol
        self.name = name
        self.last_sale = last_sale
        self.net_change = net_change
        self.percent_change = percent_change
        self.market_cap = market_cap
        self.country = country
        self.ipo_year = ipo_year
        self.volume = volume
        self.sector = sector
        self.industry = industry


class StockNasdaq:
    def __init__(self):
        self.__nasdaq_header = []
        self.__nasdaq_list = []
        file = open('nasdaq_screener.csv')
        csvreader = csv.reader(file)
        self.__nasdaq_header = next(csvreader)
        for row in csvreader:
            if len(row) < 11:
                continue

            stock_desc = StockDescription(symbol=row[0],
                                          name=row[1],
                                          last_sale=row[2],
                                          net_change=row[3],
                                          percent_change=row[4],
                                          market_cap=row[5],
                                          country=row[6],
                                          ipo_year=row[7],
                                          volume=row[8],
                                          sector=row[9],
                                          industry=row[10])
            self.__nasdaq_list.append(stock_desc)
        return

    def get_nasdaq_list(self):
        return self.__nasdaq_list

    def lookup_symbol(self, symbol=None):
        if symbol is None:
            return None

        for nasdaq_stock in self.__nasdaq_list:
            if nasdaq_stock.symbol == symbol:
                return nasdaq_stock
        return None

    def lookup_company(self, name=None):
        if name is None:
            return None

        for nasdaq_stock in self.__nasdaq_list:
            if nasdaq_stock.name.find(name) != -1:
                return nasdaq_stock
        return None


class StockFilter:
    def __init__(self):
        stock_nasdaq = StockNasdaq()
        self.__full_list = stock_nasdaq.get_nasdaq_list()
        self.__filtered_list = self.__full_list

    def get_filtered_list(self):
        return self.__filtered_list

    def reset_filter(self):
        self.__filtered_list = self.__full_list

    def filter_by_country(self, country=None):
        if country is None:
            return

        index = 0
        for stock in self.__filtered_list:
            if stock.country.find(country) == -1:
                self.__filtered_list.pop(index)
            index = index + 1

        return

    def filter_by_industry(self, industry=None):
        if industry is None:
            return

        index = 0
        for stock in self.__filtered_list:
            if stock.industry.find(industry) == -1:
                self.__filtered_list.pop(index)
            index = index + 1

        return

    def filter_by_sector(self, sector=None):
        if sector is None:
            return

        index = 0
        for stock in self.__filtered_list:
            if stock.sector.find(sector) == -1:
                self.__filtered_list.pop(index)
            index = index + 1

        return
