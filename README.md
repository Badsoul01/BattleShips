#  ⚓ Terminálové Lodě v Pythonu

Strategická hra Lodě přivedená k životu přímo v příkazové řádce. Obsahuje boj proti chytré AI na dynamicky generovaném bojišti 20x20. Kód je plně objektově orientovaný a využívá ANSI escape sekvence pro přehlednost.

##  ✨ Hlavní funkce

* **Chytrá umělá inteligence:** Jakmile AI zasáhne cíl, aktivuje vyhledávací algoritmus, určí orientaci lodi a systematicky ji potopí. 
* **Dynamická flotila:** Každá hra generuje unikátní flotilu 10 lodí s náhodnou délkou (2 až 7 polí) pro oba hráče.
* **Plynulé terminálové rozhraní:** Hra automaticky promazává obrazovku a využívá barevné kódování pro maximální přehlednost.
* **Pravidlo zásahu:** Pokud hráč nebo AI zasáhne nepřátelskou loď, získává tah navíc.

## 🗂️ Struktura logiky

* `Board` - Třída spravující herní plán 20x20, ověřování souřadnic, umisťování lodí a záznamy o střelbě.
* `Ship` - Reprezentace jednotlivých lodí, udržuje si přehled o vlastních souřadnicích a obdržených zásazích.
* `Player / HumanPlayer / AIPlayer` - Třídy rozdělující chování hráčů. AI obsahuje logiku pro trackování "načatých" lodí a výpočet osy útoku.
* `BattleShipGame` - Hlavní herní smyčka, která řídí střídání tahů a vyhodnocuje konec hry.

## 🎮 Ovládání

Hra se ovládá psaním souřadnic ve formátu **PísmenoČíslo** (např. `A2`, `C15`, `H8`)   
Písmenka reprezentují řádky (A-T) a čísla sloupce (1-20). Systém je odolný vůči překlepům a malým/velkým písmenům.

## 🚀 Instalace a spuštění

Projekt nevyžaduje instalaci žádných externích knihoven přes `pip`.

1. Naklonuj repozitář [BattleShips](https://github.com/Badsoul01/BattleShips):
    ```bash
    git clone https://github.com/Badsoul01/BattleShips.git
    ```
2. Přejdi do složky s projektem:
    ```bash
    cd BattleShips
    ```
3. Spusť hru přes hlavní soubor:
    ```bash
    python3 BattleShips.py
    ```

## 🛠️ Použité technologie

* **Python 3**
* **Objektově orientované programování (OOP)**
* **ANSI Escape Codes (Barevné formátování textu v terminálu)**