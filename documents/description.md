# Fuzzer

Celem projektu jest stworzenie fuzzer'a, który łączy najbardziej istotne cechy już istniejących narzędzi – skuteczność, elastyczność oraz prostotę obsługi. Rozwiązanie zostało zaprojektowane z myślą o użytkownikach, którzy potrzebują narzędzia łatwego w użyciu, a jednocześnie zdolnego do efektywnego wykrywania błędów w testowanym oprogramowaniu. W ramach pracy przedstawione zostają założenia projektowe, zastosowane rozwiązania techniczne oraz wyniki testów potwierdzających skuteczność działania fuzzer'a.

### Istniejące fuzzer'y

##### 1) Frelatage

Fuzzer bazujący na genetycznym generowaniu danych wejsciowych. Stara się zebrać najlepsze właściwości innych fuzzer'ów i stworzyć jeden spełniający większość funkcji pomagających w znalezieniu błędów i/lub wejść psujących program w trakcie pracy aplikacji. Frelatage ogranicza sie jedynie do podstawowych typów zmiennych w pythonie (String, Int, Float, List, Tuple, Dictionary) oraz pliku wejściowego.

##### 2) PyDySoFu

Pozwala na dynamiczne fuzzowanie w trakcie wykonywania kodu co zwiększa jego elastyczność i skuteczność. Został zaprojektowany konkretnie z myślą o pythonie, dzięki czemu jest łatwy w użyciu za pomocą dekoratorów. Niestety dokumentacja projektu nie jest już dostępna oraz brakuje dobrych przykładów w jaki sposób z niego korzystać. 

##### 3) Atheris

Fuzzing jest oparty na pokryciu kodu, skutecznie eksplorując różne ścieżki wykonania. Umożliwia wykonywanie testów z wykorzystaniem OSS-Fuzz. Wspiera pythona 3.8+ oraz C-extensions modules. Dobra dokumentacja oraz dalsze prace nad Atheris sprawiają, że jest to narzędzie nie tylko łatwiejsze do wdrożenia w profesjonalnych projektach, ale również bardziej przyszłościowe pod kątem integracji z nowoczesnymi platformami testowania bezpieczeństwa i jakości kodu. Aby móc korzystać z Atheris wymagana jest re-kompilacja Pythona z obsługą debugowania, co może być największą, a dla niektórych przeszkodą nie do przeskoczenia. Wymaga również zdecydowanie więcej wiedzy z zakresu fuzzowania od pozostałych popularnych bibliotek lub narzędzi.

##### 4) HypoFuzz

Rozszerzenie popularnej biblioteki Hypothesis, umożliwiające łatwe i szybkie wdrożenie fuzzowania w ramach testów jednostkowych. HypoFuzz bazuje na generowaniu danych testowych zgodnych z określonymi właściwościami funkcji, dzięki czemu bardzo dobrze sprawdza się w testowaniu logiki biznesowej, API oraz funkcji o zdefiniowanych typach wejściowych. Wyróżnia się prostotą integracji z istniejącym kodem oraz przyjaznym progiem wejścia.

### Założenia

Projekt tworzony z myślą o dalszym rozwoju także po realizacji pierwotnych założeń. Połączone zostaną genetyczne generowanie argumentów, rozszerzone wsparcie dla typów przekazywanych w funkcjach oraz zapewnione przyjazne środowisko dla osób bez doświadczenia w cyber-bezpieczeństwie.

Zakładane cele:
- Wsparcie dla wszystkich wbudowanych typów (int, str, tuple, list,...)
- Wsparcie dla niestandardowych typów - obiekty, klasy, Callable, Unions
- Wykorzystanie genetycznie generowanych wejść dla zwiększonej precyzji
- Proste w użyciu za pomocą dekoratorów

### Implementacja

Proces rozpoczęty zostanie od stworzenia szkieletu projektu – diagramów, krótkich opisów, identyfikacji prawdopodobnych problemów oraz szkicu interfejsu.

<!-- Diagram -->

Wszyscy członkowie zespołu zaangażowani zostaną kreatywnie. Wybrane zostaną najlepsze pomysły, które następnie zostaną zaimplementowane. Cały proces zostanie udokumentowany w artykule wydanym wraz z biblioteką.

Zadania zostaną rozdzielone pomiędzy 4 osoby:

- Część logiczna – 2 os.
- Interfejs – 1 os.
- Część redakcyjna – 1 os.

###### Część logiczna

Dwie osoby odpowiedzialne będą za przelanie pomysłu na kod. Stworzony zostanie modułowy i prosty w utrzymaniu framework, umożliwiający dalszy rozwój i modyfikację projektu.

Priorytetem będzie przejrzystość i dobra dokumentacja kodu. Kod pozostanie niezależny, bez bazowania na zewnętrznych bibliotekach, które mogą zostać porzucone.

###### Interfejs

Założeniem jest stworzenie biblioteki dostępnej dla użytkowników o różnym poziomie wiedzy w zakresie fuzzing'u. Opracowany zostanie przyjazny interfejs użytkownika oraz czytelny plik logu. Użytkownik będzie miał dostęp do informacji w czasie rzeczywistym o liczbie wykrytych nieprawidłowości oraz prędkości działania. Początkowo przygotowany zostanie TUI (terminal user interface) oraz zapis danych w formie tekstowej i surowej, możliwych do wizualizacji za pomocą np. biblioteki pyplot.

###### Część redakcyjna

Przygotowany zostanie artykuł naukowy zawierający szczegółowy opis procesu projektowego, uzasadnienie wybranych rozwiązań oraz analizę wyników testów. Dokumentacja zostanie opracowana zgodnie z formalnymi wymaganiami publikacji naukowych i będzie stanowić integralną część projektu.

###### Szczegóły implementacji

1) Genetycznie generowane wejścia
    Zastosowanie genetycznych algorytmów do generowania danych wejściowych pozwala w sposób inteligentny eksplorować przestrzeń możliwych wartości. W przeciwieństwie do losowego generowania, podejście genetyczne umożliwia ewolucję danych wejściowych, które z większym prawdopodobieństwem doprowadzą do wykrycia błędów.
    - Zaimplementujemy reprezentację chromosomu jako struktury zawierającej wartości wejściowe dla testowanej funkcji.
    - Zdefiniujemy funkcję oceny fitness
    - Zastosujemy klasyczne operatory genetyczne: mutację
    - Zaimplementujemy cykliczne ewolucje pokoleń
2) Elastyczność
    System zostanie zaprojektowany z myślą o rozszerzalności – zarówno pod kątem typów wejściowych, jak i dalszego rozwoju technik generowania danych.
    - Zaprojektujemy moduł generujący wartości dla każdego wspieranego typu
3) Proste API
    Dla użytkownika końcowego najważniejsza będzie łatwość użycia narzędzia. Nawet osoby nieznające pojęć związanych z fuzzing'iem powinny móc skorzystać z biblioteki bez konieczności dogłębnego poznawania wewnętrznych mechanizmów.
    - Głównym punktem wejścia będzie dekorator `@fuzz(*args, **kwargs)`, który będzie można zastosować bezpośrednio nad testowaną funkcją.
    - Umożliwimy przekazanie parametrów konfiguracyjnych jako argumentów dekoratora
4) Interfejs
    Interfejs użytkownika musi być zarówno funkcjonalny, jak i czytelny. Dostarczanie danych w czasie rzeczywistym, logowanie przypadków testowych oraz możliwość wizualizacji wyników stanowi integralny element skutecznego narzędzia.
    Dzięki Terminal UI (TUI) użytkownik otrzyma natychmiastowy feedback o działaniu fuzzer'a.
    - Logi pozwolą przeanalizować wykryte błędy, zapisać ścieżki do nich prowadzące i porównać skuteczność w różnych testach.
    - Wizualizacja umożliwi obserwację trendów np. w wykrywanych wyjątkach, czasie działania, czy „trudności” funkcji.

### Testy

<!-- Opis w jaki sposób będziemy testować -->

### Podsumowanie

<!-- Podsumowanie -->
