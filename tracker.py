import json
import os
import requests
from bs4 import BeautifulSoup

# Secure credentials loaded from GitHub Secrets
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# File to store previously seen movies so we don't spam notifications
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
      # For demonstration, let's pretend these are the movies currently found on the site:
      current_hd_movies = [
          'Supergirl (2026) HDRip Telugu Dubbed',
          'Jana Nayakudu (2026) HDRip Telugu',
          'Musafir Cafe Season 1 (2026) HDRip Telugu',
      ]
      current_dvd_movies = ['Oh Sukumari (2026) DVDScr Telugu']

      all_current_movies = current_hd_movies + current_dvd_movies

      # Load previously seen movies from file
      seen_movies = load_seen_movies()

      # Find if there are any brand new movies that weren't in our saved list
      new_movies = [
          movie for movie in all_current_movies if movie not in seen_movies
      ]

      if new_movies:
        print(f'Found {len(new_movies)} new movie(s)! Sending notification...')

        # Format the notification layout for the new entries
        hd_text = '\n'.join(
            [f'• [{m}]({url})' for m in current_hd_movies if m in new_movies]
        )
        dvd_text = '\n'.join(
            [f'• [{m}]({url})' for m in current_dvd_movies if m in new_movies]
        )

        notification_text = '🎬 *Telugu Movie Tracker Update*\n\n'
        if hd_text:
          notification_text += f'🟢 *Latest HD Releases:*\n{hd_text}\n\n'
        if dvd_text:
          notification_text += f'🟡 *Latest DVD / CAM Prints:*\n{dvd_text}'

        # Send alert only because new items exist
        send_telegram_message(notification_text)

        # Update our saved list to current so we don't alert for them again next hour
        save_seen_movies(all_current_movies)
      else:
        print('No new movies found. No notification sent.')

    else:
      print(f'Failed to reach Movierulz. Status code: {response.status_code}')
  except Exception as e:
    print(f'An error occurred: {e}')


if __name__ == '__main__':
  check_movies()
  
