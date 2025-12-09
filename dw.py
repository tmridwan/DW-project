from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

columns = ["Date", "Magnitude", "Latitude", "Longitude", "Depth", "Location"]

def details(row):
    cells = row.find_elements(By.CLASS_NAME, "datatable-body-cell")
    contents = {}

    if len(cells) < 6:
        return contents
    
    try:
        contents["Date"] = cells[0].text.strip()
        contents["Magnitude"] = cells[1].text.strip()
        contents["Latitude"] = cells[2].text.strip()
        contents["Longitude"] = cells[3].text.strip()
        contents["Depth"] = cells[4].text.strip()
        contents["Location"] = cells[5].text.strip()
    except IndexError as e:
        print(f"Skipping row due to index error: {e}")
        return {}
    return contents

def main():
    options = Options()
    webdriver_path = "venv/Scripts/chromedriver.exe"
    row_contents = []


    service = Service(webdriver_path)
    driver = webdriver.Chrome(options=options)
    url = "https://www.iris.edu/app/seismic-monitor/table"
    driver.get(url)
    table = driver.find_element(By.CLASS_NAME, 'ngx-datatabledatatable-row-group')
    rows = driver.find_element(By.CLASS_NAME, "datatable-row-group")

    time.sleep(3)

    driver.quit()

    df = pd.DataFrame(row_contents, columns=columns)
    df.to_csv("eq1.csv", index=False)
    print("Saved", len(row_contents), "rows.")

if __name__ == "__main__":
    main()
