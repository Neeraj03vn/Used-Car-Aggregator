import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry


class Cars24Scraper:
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
        min_price = filters.get("budget_min", 100000)
        max_price = filters.get("budget_max", 5000000)
        
        if brand and "maruti" in brand:
            brand="maruti"

        url = f"https://www.cars24.com/buy-used-{brand}-{model}-{transmission}-cars-{city}/?f=year%3Abw%3A{min_year}%2C{max_year}&f=fuelType%3Ain%3A{fuel}&f=listingPrice%3Abw%3A{min_price}%2C{max_price}"
        print(url)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = self.session.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: Status {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        Filtered_cars = soup.find('div', class_='styles_wrapper__b4UUV')
        if Filtered_cars:
            cars = Filtered_cars.find_all("div", class_="styles_normalCardWrapper__qDZjq")
            data = []

            for car in cars:
                try:
                    name_parts = car.find("span", class_="kjFjan").text.split()
                    year = name_parts[0]
                    brand_name = name_parts[1]
                    model_name = " ".join(name_parts[2:])
                except:
                    year, brand_name, model_name = "N/A", "N/A", "N/A"

                try:
                    features = car.find_all("p", class_="kvfdZL")
                    mileage = features[0].text.strip() if len(features) > 0 else "N/A"
                    fuel_type = features[1].text.strip() if len(features) > 1 else "N/A"
                    transmission_type = features[2].text.strip() if len(features) > 2 else "N/A"
                except:
                    mileage, fuel_type, transmission_type = "N/A", "N/A", "N/A"

                try:
                    price = car.find("p", class_="cyPhJl").text.strip()
                except:
                    price = "0"

                data.append({
                    "brand": brand_name,
                    "model": model_name,
                    "price": price,
                    "year": year,
                    "mileage": mileage,
                    "transmission": transmission_type,
                    "fuel": fuel_type,
                    "url": url,
                    "source": "Cars24"
                })

            return data
