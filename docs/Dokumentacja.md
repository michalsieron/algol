# Algol

**Michał Sieroń** 256 259

## 1. Opis zakresu projektu

Program **Algol** jest symulacją gwiazd zmiennych zaćmieniowych i nie tylko. Pozwala na zdefiniowanie w presetach stanu systemu gwiazd i planet oraz ich właściwości. Użytkownik ma możliwość zmiany perspektywy, czy też poziomu przybliżenia. Presety mogą być zmieniane podczas pracy programu. Po zakończeniu pracy programu użytkownik może wygenerować wykres przedstawiający średnią jasność układu. Fragmenty wykresu mają przypisane kolory w zależności od presetu jaki był w tym czasie używany.

## 2. Analiza czasownikowo - rzeczownikowa

Symulacja przedstawiająca *ruch* **gwiazd** i **planet**. Każde z nich jest przedstawione w postaci kuli w **oknie symulacji**. W trakcie trwania symulacji **gwiazdy** świecą i *zmieniają położenie* w zależności od czasu. Po zakończeniu symulacji możliwe jest *wygenerowanie* **wykresu**.
Parametry symulacji:

- ilość obiektów
- typy obiektów
- parametry obiektów

## 3. Karty CRC

| `App`                                                          | Klasa rodzic: `moderngl_window.WindowConfig`     |
| ------------------------------------------------------------ | ------------------------------------------------ |
| zarządza symulacją<br />przetrzymuje aktualne ustawienia<br />wczytuje presety<br />zapisuje zmierzoną jasność systemu | `Star`<br />`Planet`<br />`World`<br />`Logger`<br /> |

| `World`                                                      |                      |
| ------------------------------------------------------------ | -------------------- |
| przechowuje stan świata<br />odpowiada za zaktualizowanie wszystkich obiektów w świecie | `Star`<br />`Planet` |

| `Star`                                                       | Klasa rodzic: `WorldObject` |
| ------------------------------------------------------------ | -------------------------- |
| przetrzymuje dane opisujące stan gwiazdy<br />aktualizuje stan gwiazdy<br />przedstawia gwiazdę w postaci krotki<br />zwraca kolor gwiazdy |                            |

| `Planet`                                                     | Klasa rodzic: `WorldObject` |
| ------------------------------------------------------------ | -------------------------- |
| przetrzymuje dane opisujące stan planety<br />aktualizuje stan planety<br />przedstawia planetę w postaci krotki<br />zwraca kolor planety |                            |

| `Logger`                                                     |      |
| ------------------------------------------------------------ | ---- |
| otwiera plik w trybie dopisywania<br />dopisuje podane ciągi znaków do pliku tekstowego |      |



## 4. Diagram przypadków użycia

<img src=".\diagram_przypadkow_uzycia.png" alt="Diagram przypadków użycia" style="zoom:50%;" />

## 5. Diagram klas

<img src=".\diagram_klas.png" alt="Diagram klas" style="zoom:50%;" />

## 6. Diagram aktywności

![Diagram aktywności](D:\Desktop\projects\algol\docs\diagram_aktywnosci.png)