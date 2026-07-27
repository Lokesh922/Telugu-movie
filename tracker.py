import os
import requests
from bs4 import BeautifulSoup

# Secure credentials loaded from GitHub Secrets
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')


def send_telegram_message(title, movie_url, watch_url, download_url):
  if not BOT_TOKEN or not CHAT_ID:
    print('Telegram credentials missing!')
    return

  # Styled message with bold text and emojis
  message = (
      f'🎬 *New Telugu Movie Available!*\n\n'
      f'📌 *Title:* {title}\n\n'
      f'🔗 *Source Page:* {movie_url}'
  )

  # Inline keyboard with colored/interactive buttons
  reply_markup = {
      'inline_keyboard': [
          [{'text': '▶️ Watch Online', 'url': watch_url}],
          [{'text': '📥 Download Movie', 'url': download_url}],
      ]
  }

  url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
  payload = {
      'chat_id': CHAT_ID,
      'text': message,
      'parse_mode': 'Markdown',
      'reply_markup': reply_markup,
  }

  response = requests.post(url, json=payload)
  if response.status_code == 200:
    print('Notification sent successfully with buttons!')
  else:
    print('Failed to send notification:', response.text)


def check_movies():
  # Replace with your target movie website URL and parsing declaration
  url = 'YOUR_TARGET_MOVIE_WEBSITE_URL'

  headers = {'User-Agent': 'Mozilla/5.0'}
  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # --- YOUR WEBSITE SCRAPING DECLARATION GOES HERE ---
    # Example placeholders (replace these with your actual parsed variables):
    movie_title = 'Sample Telugu Movie'
    movie_page_link = url
    watch_link = 'https://example.com/watch'
    download_link = 'https://example.com/download'

    # Trigger telegram alert with buttons
    send_telegram_message(movie_title, movie_page_link, watch_link, download_link)
  else:
    print('Failed to reach website.')


if __name__ == '__main__':
  check_movies()
    
