# Notepad++-lisäosa NVDA:lle #

Tämä lisäosa parantaa Notepad++:n saavutettavuutta. Notepad++ on tekstieditori Windowsille, ja siinä on monia ominaisuuksia. Voit lukea siitä lisää osoitteessa <https://notepad-plus-plus.org/>.
Tämän lisäosan alkuperäisen version kirjoittivat Derek Riemer ja Tuukka Ojala. Myöhemmin ominaisuuksia lisäsivät Robert Hänggi ja Andre9642.

## Ominaisuudet

### Tuki kirjanmerkeille

Notepad++ mahdollistaa kirjanmerkkien lisäämisen tekstiin.
Kirjanmerkkien avulla voidaan palata nopeasti tiettyyn tekstin kohtaan.
Lisää kirjanmerkki siirtymällä riville, johon haluat lisätä sen, ja paina Ctrl+F2.
Kun haluat palata kirjanmerkkiin, paina F2 siirtyäksesi seuraavaan tai Vaihto+F2 siirtyäksesi edelliseen.
Voit lisätä niin monta kirjanmerkkiä kuin haluat.

### Rivin enimmäispituuden ilmoitus

Notepad++:ssa on viivoitin, jota voi käyttää rivin pituuden tarkistamiseen. Tämä ominaisuus ei kuitenkaan ole saavutettava tai merkityksellinen näkövammaisille käyttäjille, joten tähän lisäosaan on lisätty rivipituuden ilmaisin, joka piippaa aina kun rivi on pidempi kuin määritelty merkkien määrä.

Ota tämä ominaisuus käyttöön käynnistämällä ensin Notepad++, menemällä NVDA-valikkoon ja valitsemalla sen jälkeen Notepad++-vaihtoehto Asetukset-valikosta. Ruksaa "Ota käyttöön rivipituuden ilmaisin" -valintaruutu ja muuta tarvittaessa merkkien enimmäismäärää. Kun ominaisuus on käytössä, kuulet piippauksen vierittäessäsi rivejä, jotka ovat liian pitkiä tai joiden merkkien määrä ylittää enimmäispituuden. Vaihtoehtoisesti voit painaa NVDA+G siirtyäksesi ensimmäiseen enimmäispituuden ylittävään merkkiin aktiivisella rivillä.

### Vastaavaan sulkeeseen siirtyminen

Notepad++:ssa voit siirtyä ohjelmakoodissa vastaavan sulkumerkin kohdalle painamalla Ctrl+B.
Siirtymistä varten sinun täytyy olla yhden merkin verran sulkeiden sisällä.
Kun painat tätä komentoa, NVDA lukee rivin, jolle siirryttiin, ja jos rivi koostuu vain sulkumerkistä, se lukee ylemmän ja alemman rivin sulkeen ylä- ja alapuolelta, jotta saat tuntuman asiayhteydestä.

### Automaattinen täydennys

Oletuksena Notepad++:n automaattinen täydennys ei ole saavutettava. Automaattisessa täydennyksessä on monia ongelmia, mukaan lukien se, että se tulee esiin kelluvana ikkunana. Tämän toiminnon saavutettavuuden parantamiseksi tehdään kolme asiaa:

1. Automaattisen täydennyksen ehdotuksen ilmestyessä kuuluu nouseva suhahdus. Ehdotuksen kadotessa kuuluu laskeva suhahdus.
2. Ala/ylänuolen painaminen lukee seuraavan/edellisen ehdotetun tekstin.
3. Suositeltu teksti puhutaan ehdotusten ilmestyessä.

Huom: Teksti näytetään myös pistekirjoituksena, mikäli pistenäyttö on käytössä. Tämä ominaisuus on tällä hetkellä kokeellinen, joten älä epäröi ilmoittaa mahdollisista virheistä.

### Lisäävä haku

Yksi mielenkiintoisimmista Notepad++:n ominaisuuksista on lisäävä haku.
Lisäävä haku on hakutila, jossa etsitään tekstiä kirjoittamalla se muokkauskenttään, ja asiakirjaa vieritetään reaaliajassa näyttämään etsitty teksti.
Asiakirjaa vieritetään kirjoittaessasi näyttämään rivi, jolla etsimäsi teksti todennäköisesti on. Lisäksi hakua vastaava teksti korostetaan.
Ohjelma näyttää myös löytyneiden vastineiden määrän. Valintaikkunassa on painikkeet seuraavaan ja edelliseen vastineeseen siirtymistä varten.
NVDA puhuu kirjoittaessasi rivin, jolta Notepad++ löysi hakemasi tekstin. Myös vastineiden määrä ilmoitetaan, mutta vain jos se on muuttunut.
Kun löydät haluamasi tekstin, paina Esc-näppäintä, jolloin kyseinen tekstirivi on kohdistimen alla.
Avaa tämä valintaikkuna valitsemalla Etsi-valikosta "Lisäävä haku" tai paina Alt+Ctrl+I.

### Nykyisen rivin tietojen puhuminen (ei toimi suomalaisissa näppäinasetteluissa)

Painamalla NVDA+Vaihto+\ (kenoviiva) puhutaan seuraavat tiedot:

* Rivinumero
* Sarakenumero (ts. missä rivin kohdassa olet)
* Valinnan koko, (vaakasuunnassa valittujen merkkien määrä, jota seuraa pystysuunnassa valittujen merkkien määrä, jotka muodostavat suorakulmion.) Tämä tieto puhutaan vain, jos se on relevanttia.

### Tuki Etsi edellinen/seuraava -ominaisuudelle

Kun painat Ctrl+F, oletuksena avautuu Etsi-valintaikkuna.
Jos kirjoitat siihen tekstiä ja painat Enteriä, ikkunassa oleva teksti valitaan ja asiakirjan kohdistus siirretään seuraavaan hakutulokseen.
Voit toistaa eteen- tai taaksepäin suuntautuvan haun Notepad++:ssa painamalla F3 tai Vaihto+F3.
NVDA lukee sekä nykyisen rivin että rivillä olevan valinnan, joka edustaa löydettyä tekstiä.

## Notepad++:n ei-oletusarvoiset näppäinkomennot

Tämä lisäosa olettaa, että Notepad++:aa käytetään oletuspikanäppäimillä.
Jos näin ei ole, muuta tämän sovellusmoduulin pikanäppäimet tarpeen mukaan vastaamaan käyttämiäsi Notepad++:n komentoja NVDA:n Näppäinkomennot-valintaikkunassa.
Kaikki lisäosan komennot ovat Notepad++-osiossa.