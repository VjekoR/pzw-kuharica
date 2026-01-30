# Platforma za dijeljenje recepata i kulinarskih savjeta

Web aplikacija izrađena u Django frameworku koja omogućuje korisnicima pregled, dodavanje i komentiranje recepata.

## Funkcionalnosti
- Registracija i prijava korisnika
- CRUD operacije nad receptima
- Dodavanje sastojaka s količinama i jedinicama
- Komentiranje recepata
- Pretraga recepata
- Autorizacija (autor može uređivati/brisati svoje podatke)

## Modeli
- Recipe
- Category
- Ingredient
- Comment
- RecipeIngredient (through model)

## Ograničenja
1. Samo prijavljeni korisnici mogu dodavati recepte
2. Samo autor recepta može uređivati ili brisati recept
3. Samo autor recepta može dodavati ili mijenjati sastojke
4. Samo autor komentara može obrisati komentar

## Pokretanje projekta
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver
```

## Seed i demo login
```bash
python manage.py seed
```
Demo korisnik:
username: demo
password: demo12345