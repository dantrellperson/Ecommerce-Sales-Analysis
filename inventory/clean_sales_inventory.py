# Import dependencies
import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')


# ----------- Creating inventory section--------------------------------
# # The below function creates an inventory list from a provided sales_invoices csv 
# # (dropping returns, damaged, misc entries)

def inventory_list():
    
    # --------Cleaning Section--------------------

    sales_csv = input(f"Please provide your sales csv path: ")
    
    # --------Cleaning Section--------------------

    # Load in provided sales data csv
    provided_sales = pd.read_csv(sales_csv, encoding='unicode_escape')

    # grab all stock code and description columns
    all_stock_codes = provided_sales[['StockCode', 'Description']]

    # # drop duplicates and missing values
    all_stock_codes.dropna(inplace=True)
    all_stock_codes.drop_duplicates(
        subset=["Description"], keep='first', inplace=True)

    # # Some stock codes are place holders for various reasons, the below gets rid of those

    # create a column where all descriptions are lower case 
    all_stock_codes['Lower_Case_Description'] = all_stock_codes['Description'].str.lower()

    #list of found descriptions to remove
    remove_list = ["?","??","???","adjust","adjustment","broken",
                  "can't find","came as", "crushed","damaged", "damages", "damage", "discount",
                  "display", "dotcom", "ebay", "amazon", "faulty", "fba", "found","check","cracked",
                  "counted","found", "given away", "had been put aside","incorrect", "incorrectly",
                  "label mix up","lost", "mailout","manual","missing", "smashed","mixed up", "amazon fee",
                  "manual","bank charges", "cruk", "discount","samples", "postage","voucher","$","£","dotcom postage",
                  "wet?", "lost","lost??", "lost in space","wet", "wet boxes","????damages????", "sold as 1",
                  "?display?", "code mix up?", "?missing", "crushed","wrongly","test", "mix up", "temp adjustment",
                  "for online retail orders","taig adjust", "allocate", "stock", "for online", "OOPS", "found", "fixed",
                  "historic computer difference?....se","incorrect",'wet/mouldy', 
                   'carriage', 'mia', 'possible damages or lost']


    # # create df without descriptions in removeList 
    df = all_stock_codes[~all_stock_codes['Lower_Case_Description'].isin(remove_list)]

    # create lists from df['StockCode'] & df['Description'] to zip into tuple
    stock_code = df['StockCode']
    desc = df['Description']

    # # set empty list to place (StockCode & descriptions in all caps) in
    inven_clean = []

    # # turn stock code and description into Tuple
    inven_tuple = list(zip(stock_code,desc))

    # # loop through and check if description is in all caps, if true add it to the clean tuple
    for item in inven_tuple:
        if (item[1].isupper()) == True:
            inven_clean.append(item)

    # turn clean tuple into dataframe
    clean_df = pd.DataFrame(inven_clean, columns = ['StockCode', 'Description'])
    
    # --------Creating Common Words list------------------------------------------
    
    # create a list of all the words in each description to search for which appear the most often
    # combine exact orders that appear than once into a list
    descriptions = clean_df['Description']
    all_word_list = []

    # create a list of all the words from all the orders
    for desc in descriptions:
        split_it = desc.split()
        all_word_list.extend(split_it)
        
    # create unique word list 
    unique = Counter(all_word_list).most_common()
    
    # Split the count of words tuple into two separate lists to turn into dataframe

    a,b = map(list,zip(*unique))
    words_merged = pd.DataFrame({
        'Words': a,
        'Count': b
    })

    # all rows with a count of 50 or more to base columns off of
    common_words = words_merged.loc[words_merged['Count'] >= 50]
    
    # --------Creating categories + comparison columns Section--------------------
    
    # Create category columns

    # The words in the lists come from the (commonWords.csv) where the word count is greater than 50 lists and words I noticed from reviewing data
    sets = ['SET', 'BOX', 'PACK','ASSORTED']
    colors = ['PINK','BLUE','RED','WHITE','GREEN','BLACK', 'YELLOW', 'ORANGE', 'PURPLE', 'GREY']
    material = ['METAL', 'WOOD', 'GLASS','CRYSTAL', 'ALUMINUM', 'WOOL', 'VINYL', 'PAPER', 'WOOD', 'FELTCRAFT']
    design = ['DESIGN','HEART', 'STAR','FLAG','TREE', 'FLOWER', 
              'BIRD', 'DOG', 'CAT', 'SKULL', 'SKULLS', 'FAIRY', 'BEADED', 'PANDA', 'BUNNIES','POLKADOT',
              'STRAWBERRY','RETROSPOT','DAISY','KITTY','ANIMAL', 'BIRTHDAY','CHERRY', 'BLOSSOM','TROPICAL',
              'APPLE','FRENCH', 'TRADITIONAL', 'BUTTERFLIES', 'BUTTERFLY', 'GIRLS', 'BOYS', 'CHRISTMAS',
              'XMAS', 'VALENTINE', 'HALLOWEEN', 'HOLIDAY', 'VINTAGE','ANTIQUE']
    jewelry = ['NECKLACE','EARRING', 'BRACELET', 'RING']
    household = ['POT', 'CUP', 'MUG', 'QUILT', 'PLATE', 'CANDLE','LUNCHBOX', 
                 'HOME', 'DOORMAT', 'CLOCK', 'SPOON', 'FORK', 'JAR'
                 ,'CUTLERY', 'CABINET', 'ALARM', 'BATHROOM',
                 'TABLE', 'BATH', 'BOTTLE', 'JUG','BED','GARDEN',
                 'CUSHION', 'LUGGAGE', 'UMBRELLA', 'HANGER', 'GARAGE', 'KITCHEN', 'HERB', 'PANTRY','GIFT']
    
    # create a list of common words from the common_words_csv that have a count greater than 49
#     common_df = common_words.loc[common_words['Count'] > 49]
#     common_words_gt50 = common_df['Words'].to_list()
#     list_to_remove = ['OF', 'AND', 'WITH', '3', '4', '6', '12', '10']
#     final_common_words = list(set(common_words_gt50) - set(list_to_remove))
    
    # If description contains any word in the list label True to create categories
    # last column is for if description contains the most common words
    for i in clean_df['Description']:

        clean_df['SETS'] = clean_df['Description'].str.contains('|'.join(sets))
        clean_df['Colors'] = clean_df['Description'].str.contains('|'.join(colors))
        clean_df['Material'] = clean_df['Description'].str.contains('|'.join(material))
        clean_df['Design'] = clean_df['Description'].str.contains('|'.join(design))
        clean_df['Jewelry'] = clean_df['Description'].str.contains('|'.join(jewelry))
        clean_df['Household'] = clean_df['Description'].str.contains('|'.join(household))
    
    # list of columns
    cols = clean_df.columns
    
    # convert True and False to 1 and 0, total sum, then use sum to create MISC column for descriptions that
    # don't fall into a category
    
    clean_df = clean_df.groupby(['StockCode','Description']).sum().reset_index()
    clean_df['Sum'] = clean_df[cols].sum(axis=1)
    clean_df['MISC'] = np.where(clean_df['Sum']==0,1,0)
    clean_df.drop(columns = 'Sum', inplace = True)
    # --------CSV export section--------------------
    
    common_words.to_csv('Output_Data/common_words.csv')
    
    clean_df.to_csv('Output_Data/actual_inventory.csv',index = False)
    
    return clean_df
# ----------- End of inventory section------------------------------------------


# ----------- Sales by stock code section---------------------------------------
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
# ----------- End of Sales by stock code section----------------------------------

# ----------- actual_sales_inventory section--------------------------------------

# # The below function creates a final inventory list with sales by stock code, and adds 'price category' 
# # and 'sales frequency' columns

def actual_sales_inventory():
    
    actual_sales_inventory_csv = input(f"Please provide your actual sales inventory csv path: ")
    sales_by_stockCode_csv = input(f"Please provide your sales by stockCode csv path: ")

    # load in provided csvs
    provided_inventory = pd.read_csv(actual_sales_inventory_csv, encoding='unicode_escape') # inventory df
    provided_sales = pd.read_csv(sales_by_stockCode_csv, encoding= 'unicode_escape') # sales df
      
    # created price categories labels below based on only 6 items having a UnitPrice higher than $100
    result = pd.merge(provided_inventory, provided_sales, on="StockCode")
    conditions = [
    result['UnitPrice'].lt(5), 
    result['UnitPrice'].ge(5) & result['UnitPrice'].le(20), 
    result['UnitPrice'].gt(20)]
    choices = ['cheap', 'medium', 'high']
    result['Price_Category'] = np.select(conditions, choices)
    
    # The highest selling item sold 80,995 , so sepaarted price frequency by 4 even categories because 80k is easily 
    # divisible by 4, over half of the items sold, sold less than 1000 units. However very few sold under 100
    conditions = [
    result['Quantity'].lt(100), 
    result['Quantity'].ge(100) & result['Quantity'].le(1000), 
    result['Quantity'].ge(1000) & result['Quantity'].le(5000), 
    result['Quantity'].ge(5000) & result['Quantity'].le(10000),
    result['Quantity'].gt(10000)]
    choices = ['cold', 'warm','reg_seller', 'hot', 'best_seller']
    result['Sales_Frequency'] = np.select(conditions, choices)

    # --------CSV export section--------------------
    
    result.to_csv('Output_Data/actual_sales_inventory.csv',index = False)
    return result

# ----------- End of actual_sales_inventory section--------------------------------
