from selenium import webdriver
from selenium.webdriver.common.by import By
import time 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd

columns = ["Date", "Time", "Latitude", "Longitude", "Depth", "Region", "Type", "Automatic/Manual", "Magnitude", "Network"]
def details(row):
    cells = row.find_elements(By.TAG_NAME, 'td')
    details = [cell.text.strip() for cell in cells if cell.text.strip()]
    result = {}
    try:
        result["Date"] = row.find_element(By.CLASS_NAME, "tbdate").text.split(" ")[0]
        result["Time"] = row.find_element(By.CLASS_NAME, "tbdate").text.split(" ")[1]
        result["Latitude"] = row.find_element(By.CLASS_NAME, "tblat").text
        result["Longitude"] = row.find_element(By.CLASS_NAME, "tblon").text
        result["Depth"] = row.find_element(By.CLASS_NAME, "tbdepth").text
        result["Region"] = row.find_element(By.CLASS_NAME, "tbreg").text
        result["Type"] = row.find_element(By.CLASS_NAME, "tbtyp").text
        result["Automatic/Manual"] = row.find_element(By.CLASS_NAME, "tbam").text
        result["Magnitude"] = row.find_element(By.CLASS_NAME, "tbmag2").text
        result["Network"] = row.find_element(By.CLASS_NAME, "tbnetw").text

    except IndexError as e:
        print(f"Skipping row due to index error: {details} (Error: {e})")
        return result
    return result
def main():
    webdriver_path = "venv/Scripts/chromedriver.exe"
    row_contents = []
    for i in range(1, 50):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        url = f"https://www.emsc.eu/Earthquake_data/?view={i}"
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Wait for the earthquake rows to appear
        rows = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[data-id]"))
        )
        print(f"Found {len(rows)} rows on page {i}")

            
        for row in rows:
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