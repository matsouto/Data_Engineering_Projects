import pandas as pd
import requests
import numpy as np
import sqlite3
from log import log_process
from bs4 import BeautifulSoup
from datetime import datetime

# --------------EXTRACT---------------
url = "https://web.archive.org/web/20230908091635%20/https://en.wikipedia.org/wiki/List_of_largest_banks"

data_path = "./data/"
log_name = "log.txt"
db_name = "Banks.db"

# Function to extract data under the heading "By market capitalization"
html = requests.get(url).text
data = BeautifulSoup(html, "html.parser")

tables_html = data.find_all("tbody")
n_tables = len(tables_html)

# Get only the intended table
table = tables_html[0]
columns = [col.contents[0].strip() for col in table.find_all("th")]
rows = table.find_all("tr")

extracted_data = pd.DataFrame(columns=columns)

# Creates a dataframe for each row in the html table
for row in rows[1 : len(rows)]:
    cols = row.find_all("td")
    _values = []
    for value in cols:
        # Some rows have a different structure
        try:
            _values.append(value.contents[0].strip())
        except:
            _values.append(value.find_all("a")[1].contents[0].strip())
    _dict = {columns[i]: value for i, value in enumerate(_values)}
    _df = pd.DataFrame(_dict, index=[0])
    extracted_data = pd.concat([extracted_data, _df], ignore_index=True)

print(extracted_data)

log_process("data extracted")

# --------------TRANSFORM---------------

exchange_rate = pd.read_csv("./WorldBanks/data/exchange_rate.csv")

transformed_data = extracted_data.copy()
# Converts prices to float values
transformed_data["Market cap"] = transformed_data["Market cap"].values.astype("float")

# Adds GBP price
transformed_data["Market_cap_GBP"] = np.round(
    transformed_data["Market cap"].values
    * exchange_rate.query("Currency == 'GBP'")["Rate"].values[0],
    2,
)


# Adds EUR price
transformed_data["Market_cap_EUR"] = np.round(
    transformed_data["Market cap"].values
    * exchange_rate.query("Currency == 'EUR'")["Rate"].values[0],
    2,
)


# Adds INR price
transformed_data["Market_cap_INR"] = np.round(
    transformed_data["Market cap"].values
    * exchange_rate.query("Currency == 'INR'")["Rate"].values[0],
    2,
)

print(transformed_data)
log_process("data transformed")

# --------------LOAD---------------

# Save transformed data to a .csv file
output_csv = "./WorldBanks/data/transformed_data.csv"
transformed_data.to_csv(output_csv, index=False)

# Creating a SQLite3 database
conn = sqlite3.connect("./WorldBanks/data/" + db_name)
transformed_data.to_sql("WorldBanks", conn, if_exists="replace", index=False)
conn.close()

log_process("data loaded")

# --------------QUERY---------------

# Getting average from a selected column
conn = sqlite3.connect("./WorldBanks/data/" + db_name)
query_statement = f"SELECT AVG(MARKET_cap_GBP) FROM WorldBanks"
query_output = pd.read_sql(query_statement, conn)
log_process(f"query : {query_statement}")
print(query_output)
conn.close()
