import os
import requests
from bs4 import BeautifulSoup
import tweepy
import time
from keep_alive import keep_alive

# Ativa o servidor Flask para o Render
keep_alive()

# Carrega as variáveis de ambiente (API do Twitter)
CONSUMER_KEY = os.getenv("TWITTER_API_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Autenticação no Twitter
auth = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
)
api = tweepy.API(auth)

# URL da página de cupons da Shopee
URL = "https://shopee.com.br/m/cupom-de-desconto"

# Guarda o último cupom postado
LAST_COUPON_FILE = "last_coupon.txt"


def get_last_coupon():
    if os.path.exists(LAST_COUPON_FILE):
        with open(LAST_COUPON_FILE, "r") as f:
            return f.read().strip()
    return ""


def save_last_coupon(coupon):
    with open(LAST_COUPON_FILE, "w") as f:
        f.write(coupon)


def fetch_latest_coupon():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Pega o primeiro cupom visível na página
        coupon_element = soup.find("div", {"class": "section-content"})
        if not coupon_element:
            return None

        coupon_text = coupon_element.get_text(strip=True)
        return coupon_text[:100]  # limita pra evitar tweets muito longos

    except Exception as e:
        print("Erro ao buscar cupom:", e)
        return None


def post_coupon():
    latest = fetch_latest_coupon()
    if not latest:
        print("Nenhum cupom encontrado.")
        return

    last = get_last_coupon()

    if latest != last:
        tweet = f"🎟️ Novo cupom Shopee disponível!\n{latest}\n👉 https://s.shopee.com.br/1qTERPoef6"
        try:
            api.update_status(tweet)
            print("✅ Cupom postado no Twitter!")
            save_last_coupon(latest)
        except Exception as e:
            print("Erro ao postar:", e)
    else:
        print("Nenhum novo cupom.")


if __name__ == "__main__":
    while True:
        post_coupon()
        time.sleep(120)  # verifica a cada 2 minutos
