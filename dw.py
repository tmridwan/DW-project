from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

columns = ["Price"]

def details(row):
    contents = {}
    try:
        contents["Price"] = row
    except IndexError as e:
        print(f"Skipping row due to index error: {row} (Error: {e})")
        return contents
    return contents

def main():
    webdriver_path = "venv/Scripts/chromedriver.exe"
    row_contents = []

    for i in range(1, 21):
        service = Service(webdriver_path)
        driver = webdriver.Chrome(service=service)
        url = "https://www.iris.edu/app/seismic-monitor/table"
        driver.get(url)
        table = driver.find_element(By.CLASS_NAME, 'datatable-row-group')

        time.sleep(3)

    driver.quit()

    df = pd.DataFrame(row_contents, columns=columns)
    df.to_csv("gari.csv", index=False)
    print("Saved", len(row_contents), "rows.")

if __name__ == "__main__":
    main()
