import os
import json
import requests
import re
import asyncio

from bs4 import BeautifulSoup
from telegram import Bot


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


url = "https://nscomex.com/podaci-iz-trgovanja/nedeljni-izvestaj/"


def broj(x):
    return float(x.replace(",", "."))


def uzmi_cene():

    response = requests.get(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    tekst = soup.get_text("\n", strip=True)


    psenica = re.search(
        r"Prosečna cena iznosila je ([0-9,]+) din/kg bez PDV-a",
        tekst
    )


    soja = re.search(
        r"Za sojino zrno zaključen je.*?po ceni od ([0-9,]+) din/kg bez PDV-a",
        tekst,
        re.S
    )


    jecam = re.search(
        r"Stočnim ječmom trgovalo se po ceni od ([0-9,]+) din/kg bez PDV-a",
        tekst
    )


    kukuruz = re.search(
        r"Kukuruz.*?(?:Ponder cena iznosila je|Prosečna cena iznosila\s+je).*?([0-9]+,[0-9]+) din/kg bez PDV-a",
        tekst,
        re.S
    )


    return {
        "psenica": broj(psenica.group(1)) if psenica else None,
        "soja": broj(soja.group(1)) if soja else None,
        "jecam": broj(jecam.group(1)) if jecam else None,
        "kukuruz": broj(kukuruz.group(1)) if kukuruz else None
    }
def promena(stara, nova):

    if stara is None or nova is None:
        return "Nema dovoljno podataka"

    razlika = nova - stara

    procenat = (razlika / stara) * 100

    znak = "📈" if razlika > 0 else "📉"

    return f"{znak} {razlika:+.2f} din ({procenat:+.2f}%)"



def main():

    nove_cene = uzmi_cene()

    print("Nove cene:")
    print(nove_cene)


    try:

        with open("poslednje_cene.json", "r") as f:
            stare_cene = json.load(f)

    except:

        stare_cene = nove_cene



    poruka = """
🌾 NPK AGRO DAILY ALERT

"""


    promena_postoji = False


    for proizvod, nova in nove_cene.items():

        stara = stare_cene.get(proizvod)


        if nova is None:
            continue


        poruka += f"""
➡️ {proizvod.upper()}

Stara: {stara:.2f} din/kg
Nova: {nova:.2f} din/kg
Promena: {promena(stara, nova)}

"""


        if stara != nova:
            promena_postoji = True



    if not promena_postoji:

        poruka += "\n➡️ Danas nema promena cena."





async def posalji_telegram():

    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=poruka
    )


asyncio.run(posalji_telegram())


with open("poslednje_cene.json", "w") as f:

    json.dump(
        nove_cene,
        f,
        indent=4
    )


print("✅ Telegram poruka poslata")


if __name__ == "__main__":

    main()
