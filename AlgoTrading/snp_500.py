###########################################################################################################################
## This program sends GET requests to the iexcloud.io Sandbox API and obtains data on stock prices.
## Using the protfolio value obtained from the user, it then calculates the best number of shares to buy 
## based on the data collected.
## Finally, this progrm returns the best number of shares to buy on the S & P 500 index as an Excel file.
###########################################################################################################################

import numpy as np
import pandas as pd
import requests
from secrets import IEX_CLOUD_API_TOKEN
import math
import xlsxwriter


class stocksToBuy:

    def __init__(self):
        self.stocks = pd.read_csv('sp_500_stocks.csv')
        self.stock_columns = ['Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Buy']


    def get_stocks_df_single(self):
        """
            This function returns tha data obtained from the API for each of the 
            stock market 'Tickers'.
        """

        stocks_df = pd.DataFrame(columns=self.stock_columns)

        for symbol in stocks['Ticker'][:10]:
            api_url = f"https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}"
            request_dictionary = requests.get(api_url).json()

            
            stocks_df = stocks_df.append(
                pd.Series(
                    [
                        symbol,
                        request_dictionary['latestPrice'],
                        request_dictionary['marketCap'],
                        'N/A'
                    ],
                    index=self.stock_columns
                ),
                ignore_index=True
            )

        return stocks_df


    def chunks(self, input_list, chunk_size):
        """
            This function takes in a list and returns a list of lists
        """
        for i in range(0, len(input_list), chunk_size):
            yield input_list[i : i+chunk_size]


    def get_stocks_df_batch(self):
        """
            This function takes a batch of stock market 'Tickers'
            and returns the data from the URL in batches.
            
            This is fatset than individually sending GET requests 
            to the API for all 500+ stocks.
        """

        symbol_groups = list(self.chunks(self.stocks['Ticker'], 100))
        symbol_strings = []
        for symbol in range(0, len(symbol_groups)):
            symbol_strings.append(','.join(symbol_groups[symbol]))

        stocks_batch_df = pd.DataFrame(columns=self.stock_columns)

        for symbol_string in symbol_strings:
            batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
            data = requests.get(batch_api_url).json()

            for symbol in symbol_string.split(','):
                stocks_batch_df = stocks_batch_df.append(
                    pd.Series(
                        [
                            symbol,
                            data[symbol]['quote']['latestPrice'],
                            data[symbol]['quote']['marketCap'],
                            'N/A'
                        ],
                        index=self.stock_columns
                    ),
                    ignore_index=True
                )

        return stocks_batch_df


    def calculate_no_shares_to_buy(self, stocks_df):
        """
            This function takes in the generated stocks dataframe,
            then calculates the number of stocks to buy for each company.

            This is done by getting the user input of the portfolio value 
            as a float ot int value.
            
            It then stores these numbers in the "Number of Shares to Buy" column
            in the dataframe
        """

        portfolio_size = input("Enter Portfolio Size (float/int): \n")
        try:
            val = float(portfolio_size)
        except ValueError:
            print("Please enter a valid portfolio size! (float/int)")
        
        position_size = float(portfolio_size) / len(stocks_df.index)

        for i in range(0, len(stocks_df['Ticker'])-1):
            stocks_df.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / stocks_df['Stock Price'][i])
        
        print(stocks_df)
        return stocks_df



    def generate_xlsx_file(self, stocks_df):
        """
            This function takes in the generated stocks dataframe with the number of shares to buy.
            It then generates an xlsx file as output and saves it to the directory.
        """

        writer = pd.ExcelWriter('recommended_trades.xlsx', engine='xlsxwriter')
        stocks_df.to_excel(writer, sheet_name='Recommended Trades', index = False)
        
        background_color = '#0a0a23'
        font_color = '#ffffff'

        string_format = writer.book.add_format(
                {
                    'font_color': font_color,
                    'bg_color': background_color,
                    'border': 1
                }
            )

        dollar_format = writer.book.add_format(
                {
                    'num_format':'$0.00',
                    'font_color': font_color,
                    'bg_color': background_color,
                    'border': 1
                }
            )

        integer_format = writer.book.add_format(
                {
                    'num_format':'0',
                    'font_color': font_color,
                    'bg_color': background_color,
                    'border': 1
                }
            )

        column_formats = { 
                            'A': ['Ticker', string_format],
                            'B': ['Price', dollar_format],
                            'C': ['Market Capitalization', dollar_format],
                            'D': ['Number of Shares to Buy', integer_format]
                            }

        for column in column_formats.keys():
            writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 20, column_formats[column][1])
            writer.sheets['Recommended Trades'].write(f'{column}1', column_formats[column][0], string_format)

        writer.save()


def main():
    """
        This is the main functino of the program.
        This function instantiates the "stocksToBuy" class.

        It then uses this class to calculate the number of shares to buy 
        for each company of the S & P 500 index using the portfolio value
        obtained via user input.
    """
    
    getStocksToBuy = stocksToBuy()
    stocks_df = getStocksToBuy.get_stocks_df_batch()
    stocks_to_buy_df = getStocksToBuy.calculate_no_shares_to_buy(stocks_df)
    getStocksToBuy.generate_xlsx_file(stocks_to_buy_df)


if __name__ == "__main__":
    main()