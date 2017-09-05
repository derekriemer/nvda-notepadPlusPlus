# Notepad++ Erweiterung für NVDA #

Diese Erweiterung verbessert die barrierefreie Bedienung von Notepad++. Notepad++ ist ein Text Editor für Windows und verfügt über viele Funktionen. Sie können mehr erfahren bei <https://notepad-plus-plus.org/>

## Besonderheiten:

### Unterstützung für Lesezeichen

Notepad++ erlaubt es Ihnen im Text Lesezeichen zu setzen.
Ein Lesezeichen gestattet es Ihnen jederzeit rasch an eine gespeicherte Position im Editor zurückzukehren.
Um ein Lesezeichen zu setzen, drücken Sie Steuerung+F2 in der Zeile wo es erstellt werden soll.
Sie können nun F2 drücken um zum nächsten oder auch Umschalt+F2 um zum vorherigen Lesezeichen zu gelangen. 
Sie können so viele Lesezeichen setzen wie Sie möchten.

### Signalisierung bei Erreichen der maximalen Zeilenlänge

Notepad++ verfügt über ein Lineal das zum Überprüfen der Zeilenlänge genutzt werden kann.
Jedoch ist diese Funktion weder zugänglich noch aussagekräftig für blinde Benutzer.
Daher signalisiert diese Erweiterung durch einen Piepton wann immer die Zeile länger als die vorgegebene Anzahl von Zeichen ist.
Um diese Funktion einzuschalten aktivieren Sie zunächst Notepad++, öffnen dann das NVDA Menü und wählen unter Einstellungen "Notepad++".
Aktivieren Sie daraufhin das Kontrollkästchen "Aktiviere Anzeige von überlangen Zeilen" und geben Sie unter "Maximal erlaubte Zeilenlänge:" die gewünschte Zahl ein.
 Wenn die Funktion eingeschaltet ist hören Sie einen Piepton wann immer Sie zu einer überlangen Zeile navigieren oder wenn sich das Zeichen an der Einfügemarke ausserhalb der erlaubten Zeilenlänge befindet.
Sie können auch NVDA+G drücken um zum ersten Zeichen in der aktiven Zeile zu gelangen dessen Position grösser als die erlaubte Anzahl von Zeichen ist.

### Sprung zur zugehörigen Klammer

Durch Drücken von Steuerung+b können Sie in Notepad++ zu einer zugehörigen Klammer eines Programms springen.
Um springen zu können müssen Sie sich um eine Zeichenposition innerhalb der Klammer befinden zu der Sie das Gegenstück suchen.
Wenn Sie diesen Befehl ausführen wird Ihnen NVDA die Zeile vorlesen auf der Sie gelandet sind.
Falls die Klammer alleine steht, werden stattdessen die Zeilen ober- und unterhalb vorgelesen um Ihnen ein Gefühl des Kontextes zu vermitteln.

### Autovervollständigung

Die Autovervollständigungsfunktion von Notepad++ ist standardmässig nicht barrierefrei zugänglich.
Sie weist verschiedene Probleme auf, wie zum Beispiel die Tatsache dass sie sich in einem unverankerten Fenster befindet.
Um diese Funktionalität zu erschliessen werden drei Dinge getan:

1. Wenn ein Vorschlag für die Autovervollständigung erscheint wird ein Wisch-Geräusch abgespielt. Das Geräusch wird in gegenteiliger Richtung abgespielt wenn der Vorschlag verschwindet. 
2. Drücken der Pfeil nach unten/oben Taste verursacht ein Lesen des nächsten oder vorherigen Vorschlags. 
3. Der empfohlene Text wird gesprochen sobald ein Vorschlag erscheint.

### Tastatur

Zuweilen möchten Sie Tastenkombinationen in Notepad++ ändern oder hinzufügen.
Zum Beispiel könnten Sie ein Makro aufgezeichnet haben das das letzte Zeichen in jeder Zeile entfernt.
Wollen Sie nun eine Tastenkombination für dieses Makro definieren oder generell eine bestehende Tastenkombination ändern,
so gehen Sie gewöhnlich zu Optionen und dann auf Tastatur, woraufhin sich ein Dialog öffnet.
Bedauerlicherweise ist dieser Dialog standardmässig nicht sehr freundlich zu NVDA.
Diese Erweiterung macht ihn jedoch voll zugänglich.
Mittels Tabulator können Sie zwischen den verschiedenen Komponenten hin und her wechseln und durch Betätigen der Pfeiltasten die Werte ändern,
genau so wie Sie es von anderen Dialogen gewöhnt sind.

### Inkrementelle Suche

Eine der interessantesten funktionen von Notepad++ ist die
Fähigkeit eine inkrementelle Suche durchführen zu können.
Das ist ein Suchmodus bei welchem Sie nach einer Phrase suchen indem Sie Text im Eingabefeld eintippen und das Programm in Realzeit zu der entsprechenden Stelle voranrückt.
Während Sie tippen, wird die Zeile mit der wahrscheinlichsten Übereinstimmung fokusiert und weitere Übereinstimmungen farblich hervorgehoben und die Gesamtanzahl angezeigt.
Es gibt Schalter um zur vorherigen oder nächsten Übereinstimmung zu wechseln. 
Während Sie tippen , spricht NVDA die Zeile in der ein Suchergebnis gefunden worden ist. NVDA gibt zudem an wieviele Übereinstimmungen es gibt, jedoch nur wenn sich deren Zahl gerade geändert hat.
Sobald Sie die gewünschte Zeile im Text gefunden haben, drücken Sie einfach Escape, und die Einfügemarke wird in diese Zeile gesetzt werden. 
Um diesen Dialog zu öffnen, wählen Sie inkrementelle Suche im Menü Suchen oder drücken Sie Steuerung+Alt+E.

### Information zur aktuellen Zeile erhalten

Drücken von Umschalttaste+NVDA+\ (Backslash), zu irgendeinem Zeitpunkt, lässt NVDA das Folgende sprechen:

* die Zeilennummer
* die Spaltennummer, das heisst, wie weit innerhalb der Zeile Sie sich befinden
* die Auswahlgrösse (Anzahl der Zeichen die in horizontaler Richtung ausgewählt sind, gefolgt bei der Anzahl der Zeichen in vertikaler Richtung, also ein Rechteck., Diese Information wird nur angesagt wenn sie relevant ist.)

### Unterstützung für die Funktionen "Weitersuchen" und "Rückwärts suchen"

Steuerung+F öffnet standardmässig den Suchen Dialog. 
Wenn Sie hier Text eingeben und die Eingabetaste betätigen wird im Fenster der entsprechende Text ausgewählt und das Dokument zum nächsten Suchresultat verschoben. 
In Notepad++ können Sie F3 oder Umschalt+F3 betätigen um die Suche in Vorwärts- oder Rückwärtsrichtung zu wiederholen.
NVDA wird sowohl die aktuelle Zeile als auch den ausgewälten Text darin, der dem Suchergebnis entspricht, vorlesen.

### Vorschau von "MarkDown" oder Hypertext als Webseite

Notepad++ unterstützt normalerweise MarkDown (*.md) nicht durch beispielsweise Syntax-Hervorhebung.
Nun können Sie sich solchen Inhalt in einem Browser-ähnlichen Fenster anzeigen lassen indem Sie NVDA+H betätigen (Escape zum Schliessen des Fensters). 
Drücken von NVDA+Umschalt+H  öffnet jenen dagegen in Ihrem Standardbrowser.
Einige populäre MarkDown-Erweiterungen wie beispielsweise PHP Extra oder TOC (Inhaltsverzeichnis) werden ebenfalls unterstützt.
Zudem funktioniert es auch mit (ein-seitigem) Html.

Um es auszuprobieren, kopieren Sie bitte folgenden Block, fügen Sie ihn in ein leeres Notepad++ Dokument ein und betätigen Sie NVDA+H.

<br>

    ---
    ## Wo alles begann...  
    > vor langer Zeit,  
    > in einem fernen Land.  
    ## Und wohin  es sich dann begab  
    1. Erste Station  
    2. Zweite Station  
    ## Schlussendlich wurde es zu einer  
    * zwar ungeordneten,  
    * jedoch immer noch  
    * verbleibenden Liste.  

<br>

# Nicht standardmässige Notepad++ Tastatur Kombinationen

Diese Erweiterung erwartet das Notepad++ mit den Standard Tastaturkürzeln genutzt wird. 
Falls dies nicht der Fall sein sollte, ändern Sie bitte die Befehle dieses Anwendungsmoduls im "Eingabe" Dialog von NVDA so dass sie der reelen Belegung entsprechen.
Alle Befehle dieser Erweiterung sind unter dem Abschnitt "Notepad++" aufgelistet.