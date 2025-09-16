import requests
from bs4 import BeautifulSoup
import logging
from requests.adapters import HTTPAdapter, Retry

class CardekhoScraper:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)

    def fetch_listings(self, filters):
        brand = (filters.get("brand") or "").lower()
        model = (filters.get("model") or "").lower()
        transmission = (filters.get("transmission") or "").lower()
        city = (filters.get("city") or "bangalore").lower()
        min_year = filters.get("year_min", 2000)
        max_year = filters.get("year_max", 2025)
        fuel = (filters.get("fuel") or "").lower()
        
        if brand and "maruti" in brand:
            brand="maruti"

        url = f"https://www.cardekho.com/used-spinny+{brand}-{model}+{min_year}-{max_year}-year+{fuel}+{transmission}+cars+in+{city}"
        print(url)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: Status {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        cars = soup.find_all("div", class_="NewUcExCard posR")

        data = []

        for car in cars:
            try:
                ModelBrandyear = car.find("h3", class_="title").text
                parts = ModelBrandyear.split(" ")
                year = parts[0]
                brand_name = parts[1]
                model_name = " ".join(parts[2:])
            except:
                year, brand_name, model_name = 0, "N/A", "N/A"


            try:
                other_features = car.find("div", class_="dotsDetails")
                if other_features:
                    raw_features = other_features.get_text(" ", strip=True)
                    parts = [p.strip() for p in raw_features.split("•")]
                    mileage = parts[0] if len(parts) > 0 else "N/A"
                    fuel_type = parts[1] if len(parts) > 1 else "N/A"
                    transmission_type = parts[2] if len(parts) > 2 else "N/A"
                else:
                    mileage, fuel_type, transmission_type = "N/A", "N/A", "N/A"
            except Exception as e:
                mileage, fuel_type, transmission_type = "N/A", "N/A", "N/A"
            try:
                price_tag = car.find("div", "Price")
                price = price_tag.find("p").get_text(strip=True) if price_tag else "N/A"
            except:
                price = 0

            data.append({
                "brand": brand_name,
                "model": model_name,
                "price": price,
                "year": year,
                "mileage": mileage,
                "transmission": transmission_type,
                "fuel": fuel_type,
                "url": url,
                "source": "Cardekho"
            })

        return data
