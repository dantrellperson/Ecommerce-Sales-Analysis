# Import dependencies
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

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