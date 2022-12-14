![Credit Card Stock Image](Assets/images/Banner-for-readme.png)

# E-commerce sales data (from an actual UK retailer) Analysis.
---

I have created a process to reduce 1 weeks worth of data cleaning down to minutes

*Data Description:*
---

Company that mainly sells unique all-occasion gifts. Many customers of the company are wholesalers. All the transactions occurring between 01/12/2010 and 09/12/2011

#### Source: <!--'E-Commerce Transactions from actual UK Retailer --> https://www.kaggle.com/datasets/carrie1/ecommerce-data

*Problem Statement:*
---

**The overall goal was to create categories for stock codes to fall into based on their description, price range, and sales frequency. Then find trends for created categories based on sales.**

*What Business Impact does this have?/ What is the Business Value?*
---

- This analysis will help Sales team make data backed decisions like: "Based on previous sales, Which item categories should be pitched as our best sellers to wholesales partners to encourage them bulk order?", Can provide Sales team with an overview of how similarly categorized and priced items in inventory performed by organizing stock codes into category buckets.
- Based on sales performance shown by analysis, Supply Chain/Operations department can more easily forecast which quantities of items should be ordered from factory partner.

*Scope (system's used):*
---

Python/Jupyter, HTML/CSS, Excel

## Metrics:
---

*Overall UnitPrice Analysis*
---

- cheap = Less than \\$5.00
- medium = More than \\$5.00, but less than \\$20.00
- high = More than \\$20.00

![Unit Price](Output_Data/Images/UnitPrice_Sales.png)

![Unit QTY](Output_Data/Images/qtyDistributionPerUnitPice_Sales.png)

This Gift Shop's money maker was overwhelmingly cheap items, with 92.3% of all items sold costing less than \\$5.00, accounting for 71.4\% of total sales.

Medium priced items accounted for 7.7\% of all items sold, and 27\% of total sales.

High priced items accounted for less than 0.1\% of all items sold, and 0.7\% of total saless.

*Category compared to TotalSales Analysis*
---

The below percentage shows each category compared to the rest of sales, multiple items meet more than one category so the % are not meant to add up to 100. The percentages are to show specific category type vs rest of inventory.

For example, "SET OF 5 RED PLATES" would fall into the sets category and the colors category.

- SETS = 18.6% of total sales

---

![SETS](Output_Data/Images/SETS_Sales.png)

- Colors = 23.6% of total sales

---

![Colors](Output_Data/Images/Colors_Sales.png)

- Material = 16.6% of total sales

---

![Material](Output_Data/Images/Material_Sales.png)

- Design = 46% of total sales

---

![Design](Output_Data/Images/Design_Sales.png)

- Jewelry = 1.2% of total sales

---

![Jewelry](Output_Data/Images/Jewelry_Sales.png)

- Household = 32 % of total sales

---

![Household](Output_Data/Images/Household_Sales.png)

- MISC = 18% of total sales

---

![MISC](Output_Data/Images/Misc_Sales.png)

### Sales Frequency Analysis

---

Legend:

- best_seller: items that sold more than 10,000 pieces
- cold: items that sold less than 100 pieces
- hot: items that sold between 5,000 and 10,1000 pieces
- reg_seller: items that sold between 1,000 and 5,000 pieces
- warm: items that sold between 100 and 1,000 pieces

**Regular selling** items made 39.4% of total sales for this wholeseller. Items that include a design in the description are far and away the best selling created category

- best_seller: 24.8%
- cold: 1.5%
- hot: 17.3%
- reg_seller: 39.4%
- warm: 17%
- 
![Sales Frequency](Output_Data/Images/Sales-by-Sales_Frequency.png)

# Main Takeaways

---

1. "Regular" selling items made 39.4% of total sales for this wholeseller.

1. Items that include a design in the description are far and away the best selling created category. Second are items that include some indication of being for household(for person not business) in the description, and Third items that include color in description.

1. This Gift Shop's money maker by Unit Price was overwhelmingly cheap items, with 92.3% of all items sold costing less than \\$5.00, accounting for 71.4\% of total sales.

1. Reduced the redunancy of stock code from x number to x number

# How the code works:

---

_The jupyter notebook titled "Ecommerce Sales Analysis is the fine tuned version of my process:_

I created a python package: inventory, the functions in this package carry out of the cleaning process listed further down in this readme.

The main created function is clean_sales_inventory

clean_sales_inventory then contains three functions:

inventory_list(), sales_by_stockCode(), actual_sales_inventory()

*inventory_list():*
---

will ask you for csv file path, mine for this project exists in "Resources/data.csv", **csv must contain a StockCode and Description column to work**. Creats category columns(SETS, Colors, Material, Design, Jewelry, Household, MISC). Function then goes through each description, and places a (1) in the cateory column(s) for each unique stock code if the stock code's description meets the requirements for that column. inventory_list()

*sales_by_stockCode():* 
---

will ask you for csv file path, mine for this project exists in "Resources/data.csv", **csv must contain a StockCode and Description column to work**. Function then cleans inputed csv file, transforms data into unique list of stockcodes and creates, total sales, total quantity based on totalings the amounts shipped on each invoice, and keeps unit price column. Then exports a csv "Output_Data/sales_by_stockCode.csv"

*actual_sales_inventory():* 
---

will ask you to supply csv file paths. Supplied paths must be set to your clean sales by stock code csv path and your clean inventory list csv path. This function then creates and returns your overall sales inventory dataframe. Which will have sales by stock code and category columns. This dataframe will also include Description, Price_Category, & Sales_Frequency columns. 

## Cleaning Process:

---

1. There were different price for some stock codes, however the data did not show any indications as to why. As a result, for the final clean inventory list the unit price was adjusted to be a mean of prices for these products

1. There were several miscellaneous stock codes included for things such as "broken packages", "missed", "return". The good descriptions, thankfully, for actual sales items had a trend of being in all caps, but there were some miscellaneous descriptions in all caps as well. To help with cleaning, an all lower case column was created so these unwanted descriptions were less likely to be missed. A handful of bad descriptions remain in data post cleaning as there was a wide variety of miscellaneous desctitions.

### **Stock Code Cleaning Process to return only sales items:**

1. Create an all lower case column so unwanted descriptions are less likely to be mised
1. Create a list of found miscellaneous words and characters to filter out of data.

### **Category Creation Process:**

1. The first step was to break every description down to just individual words, and then count the occurences of each unique word in this list.
1. Then a common word list was created from the words with more than 49 occurences.
1. These common words were used to base the categories off.
1. The categories are: SETS, Colors, Holidays, Material, Design, Jewelry, Vintage, Household
1. Lists were then created containing the words that inspired the categories. These lists were used to display True if a description contained a word in the list for the matching category.
1. Then more words were pulled from the less frequent words for the lists if they fit in the broader category.
1. After that, there was a column created to display True or False if the description contained a common word(words with more than 49 occurences).
1. Finally all True and False occurences were converted to (1) and (0) respectively to total for a sum. Sum is used to create MISC categroy for descriptions not falling into any category.

# Recommendations and Next steps

---

1. Conduct a survey with Sales team to determine product categories to improve product recommendations to wholesale customer.
1. Implement code into current softwares to automate graphs for results for sales team (e.g. tableau dashboard)
