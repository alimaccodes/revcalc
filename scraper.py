from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

def run_scraper():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.booking.com/searchresults.html?ss=Glasgow&checkin_year=2025&checkin_month=6&checkin_monthday=18&checkout_year=2025&checkout_month=6&checkout_monthday=19&group_adults=1&no_rooms=1")
    time.sleep(5)

    hotels = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")
    results = []
    for hotel in hotels[:15]:
        try:
            name = hotel.find_element(By.CSS_SELECTOR, "div[data-testid='title']").text
            price = hotel.find_element(By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price']").text
            price = int(''.join(filter(str.isdigit, price)))
            results.append({"Hotel": name, "Room Category": "Unknown", "Price": price})
        except:
            continue

    driver.quit()
    return pd.DataFrame(results)

def get_suggestions(df):
    categories = {
        "Large shared dorm": [],
        "Medium shared dorm": [],
        "Small shared dorm": [],
        "Female-only dorm": [],
        "Premium dorm": [],
        "Premium dorm w/ ensuite": [],
        "Private double w/ ensuite": [],
        "Private double (shared bathroom)": [],
        "Family room / triple room": []
    }

    for _, row in df.iterrows():
        name = row["Hotel"].lower()
        price = row["Price"]

        if "female" in name:
            categories["Female-only dorm"].append(price)
        elif "private" in name and "ensuite" in name:
            categories["Private double w/ ensuite"].append(price)
        elif "private" in name:
            categories["Private double (shared bathroom)"].append(price)
        elif "family" in name or "triple" in name:
            categories["Family room / triple room"].append(price)
        elif "premium" in name:
            categories["Premium dorm"].append(price)
        elif "dorm" in name and "6" in name:
            categories["Small shared dorm"].append(price)
        elif "dorm" in name and "9" in name:
            categories["Medium shared dorm"].append(price)
        elif "dorm" in name:
            categories["Large shared dorm"].append(price)

    suggestion_data = []
    for cat, prices in categories.items():
        if prices:
            avg = round(sum(prices) / len(prices))
            suggestion_data.append({
                "Room Category": cat,
                "Competitor Avg Price": avg,
                "Suggested Price (-5%)": round(avg * 0.95)
            })

    return pd.DataFrame(suggestion_data)
