# normalize.py

import re

def normalize_price(price_text):
    
    if not price_text or price_text == "N/A":
        return None
    price_text = price_text.replace("₹", "").replace(",", "").lower()
    if "lakh" in price_text:
        try:
            val = float(price_text.split()[0])
            return int(val * 100000)
        except:
            return None
    if "crore" in price_text:
        try:
            val = float(price_text.split()[0])
            return int(val * 10000000)
        except:
            return None
    try:
        return int(re.sub(r"[^0-9]", "", price_text))
    except:
        return None

def normalize_mileage(mileage_text):
    if not mileage_text or mileage_text == "N/A":
        return None
    mileage_text = mileage_text.lower().replace("km", "").strip().replace(",", "")
    if "k" in mileage_text:
        try:
            val = float(mileage_text.replace("k", ""))
            return int(val * 1000)
        except:
            return None
    try:
        return int(re.sub(r"[^0-9]", "", mileage_text))
    except:
        return None

def normalize_listing(listing):
    return {
        "year": int(listing.get("year") or 0),
        "brand": listing.get("brand", ""),
        "model": listing.get("model", ""),
        "price": listing.get("price", ""),
        "price_inr": normalize_price(listing.get("price")),
        "mileage": normalize_mileage(listing.get("mileage")),
        "transmission": listing.get("transmission", ""),
        "fuel": listing.get("fuel", ""),
        "url": listing.get("url", ""),
        "source": listing.get("source", "")
    }
