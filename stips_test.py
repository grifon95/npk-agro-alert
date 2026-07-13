import requests
import re
from bs4 import BeautifulSoup


url = "https://stips.minpolj.gov.rs/srl/vest/promet-na-produktnot-berzi"

r = requests.get(url)

print("Status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

tekst = soup.get_text(" ", strip=True)


# pšenica
psenica = re.search(
    r"Ponder cena iznosi ([0-9]+,[0-9]+) din/kg",
    tekst
)

if psenica:
    print("Pšenica:", psenica.group(1))
else:
    print("Pšenica nije pronađena")


# kukuruz
kukuruz = re.search(
    r"Ponder cena ove žitarice iznosi ([0-9]+,[0-9]+) din/kg",
    tekst
)

if kukuruz:
    print("Kukuruz:", kukuruz.group(1))
else:
    print("Kukuruz nije pronađen")


# soja
soja = re.search(
    r"Soja.*?([0-9]+,[0-9]+) din/kg",
    tekst
)

if soja:
    print("Soja:", soja.group(1))
else:
    print("Soja nije pronađena")
