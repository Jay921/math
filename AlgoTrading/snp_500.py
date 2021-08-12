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

stocks = pd.read_csv('sp_500_stocks.csv')
stock_columns = ['Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Buy']


def get_stocks_df_single(stock_columns):
    """
        This function returns tha data obtained from the API for each of the 
        stock market 'Tickers'.
    """

    stocks_df = pd.DataFrame(columns=stock_columns)

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
                index=stock_columns
            ),
            ignore_index=True
        )

    return stocks_df


def chunks(input_list, chunk_size):
    """
        This function takes in a list and returns a list of lists
    """
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i : i+chunk_size]


def get_stocks_df_batch(stock_columns):
    """
        This function takes a batch of stock market 'Tickers'
        and returns the data from the URL in batches.
        
        This is fatset than individually sending GET requests 
        to the API for all 500+ stocks.
    """

    symbol_groups = list(chunks(stocks['Ticker'], 100))
    symbol_strings = []
    for symbol in range(0, len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[symbol]))

    stocks_batch_df = pd.DataFrame(columns=stock_columns)

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
                    index=stock_columns
                ),
                ignore_index=True
            )

    return stocks_batch_df


def calculate_no_shares_to_buy(stocks_df):
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



def generate_xlsx_file(stocks_df):
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


stocks_df = get_stocks_df_batch(stock_columns)
stocks_to_buy_df = calculate_no_shares_to_buy(stocks_df)
generate_xlsx_file(stocks_to_buy_df)