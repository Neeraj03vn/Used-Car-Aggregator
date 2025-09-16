# Used Car Price Aggregator

The Used Car Price Aggregator is a real-time platform that fetches and displays used car listings from multiple platforms (Cars24, OLX, CarDekho).

It features a Streamlit dashboard for searching cars by filters like brand, model, budget, year, fuel type, city, and transmission.
Results are normalized (price, mileage, etc.) and exported automatically to Google Sheets.

The project is deployed on AWS EC2 and uses Crontab for automated background scraping.

# Features
1. Multi-platform scraping: Cars24, OLX, CarDekho
2. Streamlit Dashboard with admin login and search filters
3. Data normalization for price (₹, lakh, crore), mileage, and year
4. Google Sheets API export for real-time data sharing
5. Crontab automation for scheduled scraping
6. Logging and error handling for reliability

# System Architecture


# Tech Stack
1. Python: Streamlit, Pandas, Requests, BeautifulSoup
2. Google Sheets API: gspread, oauth2client
3. Deployment: AWS EC2
4. Automation: Crontab scheduling
5. Logging: scraper.log

# Setup Instructions

1. Clone Repository
  -> git clone https://github.com/<your-username>/used-car-aggregator.git
  -> cd used-car-aggregator

2. Create Virtual Environment
  -> python3 -m venv venv
  -> source venv/bin/activate   # Linux/Mac
  -> venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Google Sheets API
  -> Enable Google Sheets API in Google Cloud Console
  -> Download your credentials JSON → save as service_account.json
  -> Share your Google Sheet with the service account email

5. Run Streamlit App Locally
  -> streamlit run app.py --server.port 8501
  -> Access at: http://localhost:8501

6. Deploy on AWS EC2
  -> Launch an Ubuntu EC2 instance

7. SSH into the instance:
   -> ssh -i your-key.pem ubuntu@your-ec2-ip
  Install Python, pip, git, and virtualenv:
   -> sudo apt update && sudo apt install -y python3-pip python3-venv git
8. Clone repo, set up venv, install dependencies (steps 1–3 above).
  Run the app:
    -> nohup streamlit run app.py --server.port 8501 --server.address 127.0.0.1 &

9. Automate with Crontab
  Edit crontab:
    -> crontab -e
  Add job to run every minute:
    -> * * * * * /home/ubuntu/Task_1/venv/bin/python /home/ubuntu/Task_1/Scraping_runner.py >> /home/ubuntu/Task_1/scraper.log 2>&1

# Project Structure

Project Files
├── app.py                # Streamlit dashboard
├── connectors/           # Scrapers
│   ├── cars24.py
│   ├── olx.py
│   ├── cardekho.py
├── normalize.py          # Normalization utils
├── sheets.py             # Google Sheets connector
├── Scraping_runner.py    # Background scraper
├── requirements.txt      # Dependencies
├── scraper.log           # Log file
├── service_account.json  # Google Sheets credentials (ignored in .gitignore)
├── diagram.png           # Architecture diagram
└── README.md

# Future Enhancements
1. Add support for more platforms (Spinny, Droom, etc.)
2. Add HTTPS using Let’s Encrypt (Certbot)
3. Build a web dashboard (React/Django + API)
4. Add ML-based car price prediction
