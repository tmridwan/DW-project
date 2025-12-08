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
    row_contents = []

    # Create driver ONCE outside loop (VERY IMPORTANT!)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    for i in range(1, 21):
        url = "https://www.carwow.co.uk/used-cars"
        driver.get(url)
        time.sleep(3)

        # Fetch all cards
        cards = driver.find_elements(By.CLASS_NAME, 'deal-card')

        for card in cards:
            try:
                price = card.find_element(By.CLASS_NAME, 'deal-card__price').text
                row_contents.append(price)
            except:
                continue

    driver.quit()

    df = pd.DataFrame(row_contents, columns=columns)
    df.to_csv("gari.csv", index=False)
    print("Saved", len(row_contents), "rows.")

if __name__ == "__main__":
    main()
