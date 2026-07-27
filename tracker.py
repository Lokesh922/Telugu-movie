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
        
        hd_list = []
        dvd_cam_list = []
        
        for a in soup.find_all('a'):
            text = a.text.strip()
            if text and ("[Telugu]" in text or "[Telugu Dubbed]" in text):
                if "HDRip" in text or "BRRip" in text or "BluRay" in text:
                    if text not in hd_list:
                        hd_list.append(text)
                else:
                    if text not in dvd_cam_list:
                        dvd_cam_list.append(text)
                        
        return hd_list, dvd_cam_list
    except Exception as e:
        print(f"Error fetching page: {e}")
        return [], []

def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    hd_movies, other_movies = get_categorized_movies()
    
    if hd_movies or other_movies:
        message = "🎬 *Telugu Movie Tracker Update*\n\n"
        
        message += "🟢 *Latest HD Releases:*\n"
        if hd_movies:
            message += "\n".join([f"• {m}" for m in hd_movies[:3]]) + "\n\n"
        else:
            message += "None found\n\n"
            
        message += "🟡 *Latest DVD / CAM Prints:*\n"
        if other_movies:
            message += "\n".join([f"• {m}" for m in other_movies[:3]])
        else:
            message += "None found"
            
        send_telegram_notification(message)
    else:
        print("No movies found or site blocked.")
            
