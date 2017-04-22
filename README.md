# wypok
Alter ego popularnej strony [wykop.pl](http://www.wykop.pl).

Projekt realizowany jest w ramach konkursu [Daj Się Poznać 2017](http://dajsiepoznac.pl)

Postęp można śledzić na moim [blogu](https://arturtamborski.pl/) pod tagiem [#dajsiepoznac2017](https://arturtamborski.pl/tags/dajsiepoznac2017) ([feed](https://arturtamborski.pl/tags/dajsiepoznac2017/feed)).



# O projekcie

Aplikacja będzie podzielona na dwie części:
  - wykopywarka linków (strona główna wykopu / reddita),
  - wpisy użytkowników (mikroblog wykopu / imageboardy 4chana).

Obie części będą ściśle powiązane z systemem komentowania, głosowania i kategoryzowania najpopularniejszych wpisów.

Użytkownicy będą mogli produkować treści udostępniając je z własnych kont jak i również pisząc z publicznego anonimowego konta.

Komentarze będą formatowane w markdown'ie co umożliwi zmienianie właściwości tekstu (pogrubienie, pochylenie, itd). Użytkownicy będą również mogli skorzystać ze specjalnych znaków nadających nowe znaczenie:
  - `@konto`    nawiązanie do użytkownika (twitter)
  - `#kotki` hashtag (twitter)
  - `/gif/` sekcja (reddit)
  - `:lenny:` emoji (gg)
  - `!general` chat (irc)
  - `>text` greentext (4chan)
  - `>>12341` link do innego postu (4chan)
  - `/thread` zamknij wątek (tylko dla OPa)
  - `feelsgoodman.png` wstaw obrazek o podanym tytule z publicznej galerii memów (to samo dla .jpg, .png, .bmp)
  - `feelsgoodman.mp4` wstaw filmik o podanym tytule z publicznej galerii memów (to samo dla .gif, .webm)

Dodatkowo wokół avataru będzie pasek oznaczający płeć
  - różowy (kobieta)
  - niebieski (mężczyzna).

Kolor nazwy użytkownika to
  - szary (konto zostało zbanowane)
  - biały (konto zostało usunięte przez użytkownika)
  - zielony (konto ma mniej niż 30 dni)
  - pomarańczowy (konto ma więcej niż 30 dni)
  - czerwony (administrator)

Strona jest podzielona na kilka aplikacji:
  - accounts - Konta użytkowników, profile, opisy ustawienia itd.
  - excavation - Wykopalisko - strona domowa.
  - mirkochan - Mirkoczan - luźne miejsce dla twórczości użytkowników.
  - chatroom - Pokoje rozmów - użytkownicy mogą dołączyć do czatów live typu omegele czy obcy

![logo konkursu](https://github.com/arturtamborski/wypok/raw/master/logo.png)
