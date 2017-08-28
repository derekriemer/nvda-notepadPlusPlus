# Notepad++ Erweiterung für  NVDA #

Diese Erweiterung  verbessert die barrierefreie Bedienung  von Notepad++. Notepad++ ist ein Text Editor für Windows und verfügt über viele Funktionen. Sie können mehr erfahren bei  <https://notepad-plus-plus.org/>

## Besonderheiten:

### Unterstützung für Lesezeichen

Notepad++ erlaubt es Ihnen im Text Lesezeichen zu setzen.
Ein Lesezeichen gestattet  es Ihnen jederzeit  rasch an eine gespeicherte  Position im Editor   zurückzukehren.
Um ein Lesezeichen zu setzen, drücken Sie Steuerung+F2 in der Zeile wo es  erstellt werden soll.
Sie können nun F2 drücken um zum nächsten oder auch Umschalt+F2 um zum vorherigen Lesezeichen zu gelangen.  
Sie können so viele Lesezeichen setzen wie Sie möchten.

### Signalisierung bei Erreichen der maximalen Zeilenlänge

Notepad++ verfügt über ein Lineal das zum Überprüfen  der Zeilenlänge genutzt werden kann.
Jedoch ist diese Funktion weder  zugänglich noch aussagekräftig für blinde Benutzer.
Daher signalisiert diese Erweiterung durch einen Piepton   wann immer  die Zeile länger als die vorgegebene Anzahl von Zeichen ist.
Um diese Funktion einzuschalten aktivieren  Sie zunächst Notepad++, öffnen dann das NVDA Menü und wählen  unter Einstellungen "Notepad++".
Aktivieren Sie daraufhin das Kontrollkästchen "Aktiviere Anzeige von überlangen Zeilen" und geben Sie unter "Maximal erlaubte Zeilenlänge:" die gewünschte Zahl ein.
 Wenn die Funktion eingeschaltet ist hören Sie einen Piepton wann immer  Sie zu einer überlangen Zeile navigieren oder wenn sich das Zeichen an der Einfügemarke  ausserhalb der  erlaubten Zeilenlänge befindet.
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

Eine der interessantesten funktionen  von Notepad++ ist die
Fähigkeit eine inkrementelle Suche durchführen zu können.
Das ist ein Suchmodus  bei welchem Sie nach einer Phrase suchen indem Sie  Text im Eingabefeld eintippen und das Programm in Realzeit zu der entsprechenden Stelle voranrückt.
Während Sie tippen, wird das Dokument so verschoben das die Zeile mit der wahrscheinlichsten Übereinstimmung im Fokus ist
und weitere Übereinstimmungen werden grafisch hervorgehoben und die Gesamtanzahl angezeigt.
Es gibt Schalter um zur vorherigen oder nächsten Übereinstimmung zu wechseln.

As you type, NVDA will announce the line of text that notepad++ detected a search result in. NVDA also announces how many matches there are, but only if the number of matches has changed. 
When you found the line of text you want, simply press escape, and that line of text will be at your cursor.
To launch this dialog, select incremental search from the search menu, or press alt+control+i.

### Reporting information about the  current line

Pressing nvda+shift+\ (back slash) at any time will report the following:

* the line number
* the column number I.E. how far into the line you are.
* the selection size, (number of characters horizontally selected, followed by  the number of characters vertically selected, which would make a rectangle. This info is only reported if relevant.

### Support for the previous/next find feature.

By Default, if you press control+f you bring up the find dialog. 
If you type text here and press enter, the text in the window is selected and the document is moved to the next search result. 
In Notepad++ you can press f3 or shift+f3 to repeat the search in the forward or backward direction respectively. 
NVDA will read both the current line, and the selection within the line which represents the found text.

### Preview of MarkDown or Hypertext as Web page 

Notepad++ does natively not support MarkDown (*.md) with e.g. language highlighting.   
However, you can preview such content as browsable message if you press NVDA+h (Escape to close the message). 
Pressing this combination twice will open it in your standard browser.  
Some popular Markdown extensions such as PHP Extra or TOC are supported.  
It works also with (single-paged) Html. 

To try it out, Copy the following block, paste it into a new Notepad++ document and press NVDA+h:

<br>

    ---
    ## Where it began...  
    > A long time ago,  
    > in a foreign country.  
    ## And where it went next  
    1. First stage  
    2. Second stage  
    ## Eventually it became  
    * unordered  
    * but still  
    * a list  

<br>

# Non-default Notepad++ keyboard shortcuts

This add-on expects that Notepad++ is being used with the default shortcut keys. 
If this is not the case, please change this app module's key commands to reflect your Notepad++ commands as necessary in NVDA's input gestures dialog.
All of the add-ons commands are under the notepad++ section.
