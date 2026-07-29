import json
import os
import requests
from bs4 import BeautifulSoup

# Secure credentials loaded from GitHub Secrets
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# File to store previously seen movies
SEEN_FILE = 'seen_movies.json'


def load_seen_movies():
  if os.path.exists(SEEN_FILE):
    try:
      with open(SEEN_FILE, 'r') as f:
        return json.load(f)
    except Exception:
      return []
  return []


def save_seen_movies(movies_list):
  try:
    with open(SEEN_FILE, 'w') as f:
      json.dump(movies_list, f)
  except Exception as e:
    print(f'Failed to save seen movies: {e}')


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
      # (Replace these simulated lists with your actual BeautifulSoup selectors later)
      current_hd_movies = [
          'Supergirl (2026) HDRip Telugu Dubbed',
          'Jana Nayakudu (2026) HDRip Telugu',
          'Musafir Cafe Season 1 (2026) HDRip Telugu',
      ]
      current_dvd_movies = ['Oh Sukumari (2026) DVDScr Telugu']

      all_current_movies = current_hd_movies + current_dvd_movies

      # Load previously saved movies
      seen_movies = load_seen_movies()

      # Filter out only movies that are NOT in our history file
      new_hd_movies = [m for m in current_hd_movies if m not in seen_movies]
      new_dvd_movies = [m for m in current_dvd_movies if m not in seen_movies]

      # Check if any brand-new movies exist across either category
      if new_hd_movies or new_dvd_movies:
        print(
            'New movies detected! Preparing notification for only new entries...'
        )

        hd_text = '\n'.join([f'• [{m}]({url})' for m in new_hd_movies])
        dvd_text = '\n'.join([f'• [{m}]({url})' for m in new_dvd_movies])

        notification_text = '🎬 *Telugu Movie Tracker Update*\n\n'
        if hd_text:
          notification_text += f'🟢 *Latest HD Releases:*\n{hd_text}\n\n'
        if dvd_text:
          notification_text += f'🟡 *Latest DVD / CAM Prints:*\n{dvd_text}'

        # Send notification strictly for the new items
        send_telegram_message(notification_text)

        # Save all current movies to history so they are never flagged as new again
        save_seen_movies(all_current_movies)
      else:
        print(
            'No new movies added since the last check. No notification sent.'
        )

    else:
      print(f'Failed to reach Movierulz. Status code: {response.status_code}')
  except Exception as e:
    print(f'An error occurred: {e}')


if __name__ == '__main__':
  check_movies()
  
