import requests
from bs4 import BeautifulSoup

URL = "https://www.5movierulz.vote/"
TELEGRAM_BOT_TOKEN = "8804491708:AAGc68AYGPx4ezPBbbCMB5V-BjErVE8PW8E"
CHAT_ID = "7228745110"

def get_categorized_movies():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        movies = []
        for a in soup.find_all('a'):
            text = a.text.strip()
            if text and ("[Telugu]" in text or "[Telugu Dubbed]" in text):
                if text not in movies:
                    movies.append(text)
        return movies
    except Exception as e:
        print(f"Error: {e}")
        return []

def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    current_movies = get_categorized_movies()
    if current_movies:
        # Sends the top latest movie found on the site during this check
        latest_movie = current_movies[0]
        send_telegram_notification(f"🎬 Latest Telugu Check: {latest_movie}")
      
