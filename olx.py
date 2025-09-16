import requests
from bs4 import BeautifulSoup
import logging
from requests.adapters import HTTPAdapter, Retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OlxScraper:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)

    def fetch_listings(self, filters, limit=20):
        brand = (filters.get("brand") or "").lower()
        model = (filters.get("model") or "").lower()
        transmission = (filters.get("transmission") or "").lower()
        city = (filters.get("city") or "bangalore").lower()
        min_year = filters.get("year_min", 2000)
        max_year = filters.get("year_max", 2025)
        fuel = (filters.get("fuel") or "").lower()
        min_price = filters.get("budget_min", 100000)
        max_price = filters.get("budget_max", 5000000)


        if brand=="honda":
            url = f"https://www.olx.in/{city}_g2001163/cars_c84?filter=model_eq_cars-{brand}-{model}%2Cpetrol_eq_{fuel}%2Cyear_between_{min_year}_to_{max_year}%2Cprice_between_{min_price}_to_{max_price}"
        else:
            url = f"https://www.olx.in/{city}_g2001163/cars_c84?filter=model_eq_{brand}-{model}%2Cpetrol_eq_{fuel}"
        if transmission and transmission == "manual":
            url+="%2Ctransmission_eq_2"
        else:
            url+="%2Ctransmission_eq_1"
        print(url)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: Status {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        data = []
        Cars = soup.find_all("li", class_="_3V_Ww")

        for car in Cars:
            a_tag = car.find("a", href=True)
            url_tag = 'https://www.olx.in' + a_tag["href"] if a_tag else "N/A"

            try:
                ModelBrand = car.find("div", class_="_2Gr10").text
                parts = ModelBrand.split(" ")
                brand_name = parts[0]
                model_name = parts[-1]
            except:
                brand_name, model_name = "N/A", "N/A"
                
            try:
                price = car.find("span", class_="_1zgtX").text
            except:
                price = 0
                
            try:
                other_features = car.find("div", class_="_21gnE").text
                parts = other_features.split(" - ")
                year = parts[0]
                mileage = parts[-1]
            except:
                year, mileage = 0, "N/A"
                


            data.append({
                "brand": brand_name,
                "model": model_name,
                "price": price,
                "year": year,
                "mileage": mileage,
                "transmission": transmission,
                "fuel": fuel,
                "url": url_tag,
                "source": "Olx"
            })
        logger.info(f"Fetched {len(data)} cars from Cars24")
        return data
