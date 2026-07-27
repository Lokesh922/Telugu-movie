import os
import requests
from bs4 import BeautifulSoup

# Secure credentials loaded from GitHub Secrets
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')


def send_telegram_message(message_body):
  if not BOT_TOKEN or not CHAT_ID:
    print('Telegram credentials missing!')
    return

  url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
  payload = {
      'chat_id': CHAT_ID,
      'text': message_body,
      'parse_mode': 'Markdown',
  }

  response = requests.post(url, json=payload)
  if response.status_code == 200:
    print('Notification sent successfully!')
  else:
    print('Failed to send notification:', response.text)


def check_movies():
  # Target Movierulz URL
  url = 'https://www.5movierulz.vote/'

  headers = {
      'User-Agent': (
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
          ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
      )
  }

  try:
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      # --- YOUR MOVIERULZ SCRAPING & PARSING LOGIC GOES HERE ---
      # Notification following your exact requested layout style linked to Movierulz:
      notification_text = (
          f'🎬 *Telugu Movie Tracker Update*\n\n'
          f'🟢 *Latest HD Releases:*\n'
          f'• [Supergirl (2026) HDRip Telugu Dubbed]({url})\n'
          f'• [Jana Nayakudu (2026) HDRip Telugu]({url})\n'
          f'• [Musafir Cafe Season 1 (2026) HDRip Telugu]({url})\n\n'
          f'🟡 *Latest DVD / CAM Prints:*\n'
          f'• [Oh Sukumari (2026) DVDScr Telugu]({url})'
      )

      # Trigger telegram alert
      send_telegram_message(notification_text)
    else:
      print(f'Failed to reach Movierulz. Status code: {response.status_code}')
  except Exception as e:
    print(f'An error occurred: {e}')


if __name__ == '__main__':
  check_movies()
      
