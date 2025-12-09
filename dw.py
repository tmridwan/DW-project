from selenium import webdriver
from selenium.webdriver.common.by import By
import time 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

columns = ["Date", "Time", "Latitude", "Longitude", "Depth", "Region", "Type", "Automatic/Manual", "Magnitude", "Network"]
def details(row):
    cells = row.find_elements(By.TAG_NAME, 'td')
    details = [cell.text.strip() for cell in cells if cell.text.strip()]
    contents = {}
    if len(cells) < 10:
        print(f"Skipping row due to insufficient data (length {len(details)}): {details}")
        return contents
    try:
        contents["Date"] = details[1].split('\n')[0]
        contents["Time"] = details[1].split('\n')[1]
        contents["Latitude"] = details[2]
        contents["Longitude"] = details[3] 
        contents["Depth"] = details[4]
        contents["Region"] = details[6]
        contents["Type"] = details[7]
        contents["Automatic/Manual"] = details[8]
        contents["Magnitude"] = details[9] + details[10]
        contents["Network"] = details[11]

    except IndexError as e:
        print(f"Skipping row due to index error: {details} (Error: {e})")
        return contents
    return contents
def main():
    webdriver_path = "venv/Scripts/chromedriver.exe"
    row_contents = []
    for i in range(1, 150):
        service = Service(webdriver_path)
        driver = webdriver.Chrome(service=service)
        url = f"https://www.emsc.eu/Earthquake_data/?view={i}"
        driver.get(url)
        table = driver.find_element(By.CLASS_NAME, 'table')
        tbody = table.find_elements(By.TAG_NAME, 'tbody')
        for idx, row in enumerate(tbody):
            data = details(row)
            if data:
                row_contents.append(data)
        driver.close()

    df = pd.DataFrame(data = row_contents, columns= columns)
    df.to_csv("eq_record.csv", index = False)
    print(len(row_contents))
    return
if __name__ == "__main__":
    main()