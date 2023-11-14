import pandas as pd
import requests
from log import log_process
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://web.archive.org/web/20230908091635%20/https://en.wikipedia.org/wiki/List_of_largest_banks"

data_path = "./data/"
log_name = "log.txt"
db_name = "Banks.db"

# Function to extract data under the heading "By market capitalization"
html = requests.get(url).text
data = BeautifulSoup(html, "html.parser")

tables_html = data.find_all("tbody")

n_tables = len(tables_html)

table = tables_html[0]
columns = [col.contents[0].strip() for col in table.find_all("th")]
extracted_data = pd.DataFrame(columns=columns)

rows = table.find_all("tr")

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

extracted_data
