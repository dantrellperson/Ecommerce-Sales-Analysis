import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# # The below function creates a total sales list by stock code from a provided sales_invoices csv 

def sales_by_stockCode():
    
    sales_csv = input(f"Please provide your sales csv path: ")

    # load in provided sales data csv
    provided_sales = pd.read_csv(sales_csv, encoding='unicode_escape')

    # filter out all the rows where the Quanty is 0
    sales_copy = provided_sales.loc[provided_sales['Quantity'] > 0]

    # drop description column
    sales_copy.drop(columns='Description', inplace=True)

    # remove the time from the invoice date column
    sales_copy['InvoiceDate'] = sales_copy['InvoiceDate'].str[:-5]

    # create a total sales column by summing all individual invoice sales for each stock code
    sales_copy['TotalSales'] = sales_copy.Quantity * sales_copy.UnitPrice

    # The average of the unit prices was used, as in the data there was no indication
    # as to why the same item have different prices, other than maybe season

    # Used sum of InvoiceTotal column to get the overall sales for each stockcode
    # Used sum of quantity to get an idea what total invntory might look like
    final = sales_copy.groupby(['StockCode']).agg({'TotalSales': 'sum', 'Quantity': 'sum',
                                                   'UnitPrice': 'mean'}).reset_index()
    # round the UnitPrice column to two decimal places
    final['UnitPrice'] = final['UnitPrice'].round(2)

    # --------------CSV export section--------------------------------------------

    final.to_csv('Output_Data/sales_by_stockCode.csv', index=False)

    # -------------- Return statement --------------------

    return final
