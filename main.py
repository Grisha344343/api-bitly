import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


def shorten_link(token, user_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "long_url": user_url
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def is_bitlink(token, link):
    parsed_url = urlparse(link)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{netloc}/{path}"
    url = url.format(netloc=parsed_url.netloc, path=parsed_url.path)
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.ok


def count_clicks(token, link):
    parsed_url = urlparse(link)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{netloc}/{path}/clicks/summary"
    url = url.format(netloc=parsed_url.netloc, path=parsed_url.path)
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(
        description='сокращает ссылку или считает клики по этой ссылке'
    )
    parser.add_argument('url', help='Ваша ссылка')
    args = parser.parse_args()

    user_url = args.url
    try:
        if is_bitlink(token, user_url):
            print('Колличество кликов', count_clicks(token, user_url))
        else:
            print('Битлинк', shorten_link(token, user_url))
    except requests.exceptions.HTTPError:
        print("Ошибка - неверная ссылка")
