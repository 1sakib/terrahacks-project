import pandas as pd
excel_file = 'TerraHacks appliance dataa.xlsx'
xls = pd.read_excel(excel_file)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
x = ['Dehumidifier', 'Residential cloths dryer', 'Rsidential cloths washer', 'refridgerator','oven/stove',
     'dishwasher', 'Air conditioner', 'Toaster', 'Coffee maker']
input = "refridgerator"
index = 0

for i in range(len(x)):
    if x[i] == input:
        index = i
        break


print(xls.loc[xls.index[index:index+1],['Estimated Annual Energy Use (kWh/yr)']])