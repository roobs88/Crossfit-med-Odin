# 🏋️ Friday WOD — Crossfit på jobben

En enkel og stilren Streamlit-app for å administrere ukentlige CrossFit-økter.

## Funksjoner

- 👤 **Brukerinnlogging** – skriv inn navn i sidepanelet
- 📅 **Påmelding** – meld deg på neste fredagsøkt med ett klikk
- 🔥 **WOD-visning** – admin legger inn dagens økt som alle kan se
- 🏆 **Leaderboard** – se hvem som har vært på flest treninger
- 📋 **Historikk** – oversikt over siste 5 økter
- 🔐 **Admin-panel** – legg inn WOD, administrer påmeldinger, eksporter data

## Kom i gang lokalt

```bash
git clone https://github.com/DITT-BRUKERNAVN/crossfit-jobb.git
cd crossfit-jobb
pip install -r requirements.txt
streamlit run app.py
```

## Deploy på Streamlit Cloud

1. Push koden til GitHub
2. Gå til [share.streamlit.io](https://share.streamlit.io)
3. Koble til GitHub og velg dette repoet
4. Klikk **Deploy** — ferdig! 🚀

## Admin-tilgang

Standard admin-passord er `crossfit2025`.  
**Husk å endre dette** i `app.py` (linje med `ADMIN_PASSWORD = ...`).

## Filstruktur

```
crossfit-jobb/
├── app.py              # Hele applikasjonen
├── requirements.txt    # Python-avhengigheter
├── README.md           # Denne filen
├── signups.csv         # Genereres automatisk (påmeldinger)
└── wods.json           # Genereres automatisk (WOD-tekster)
```

> **Tips:** Legg til `signups.csv` og `wods.json` i `.gitignore` hvis du ikke vil at data skal ligge på GitHub.
