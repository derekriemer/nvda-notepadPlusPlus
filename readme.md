# Notepad++ Add-on for NVDA #

This add-on improves the accessibility of notepad++. Notepad++ is a text editor for windows, and has many features. You can learn more about it at <https://notepad-plus-plus.org/>

## Features:

### Support for Bookmarks

Notepad++ allows you to set bookmarks in your text.
A bookmark allows you to quickly come back to a location in the editor at any point.
To set a bookmark, from the line you wish to bookmark, press control+f2.
Then, when you want to come back to this bookmark, press f2 to jump to the next bookmark, or shift+f2 to jump backwards to the previous one.
You can set as many bookmarks as you would like.

### Maximum Line Length Announcement

Notepad++ has a ruler that can be used for checking a line's length. However, this feature
is neither accessible or meaningful to blind users, so this add-on has an audible line length
indicator that beeps whenever a line is longer than the specified number of characters.

To enable this feature, first activate Notepad++, then go to the NVDA menu and activate Notepad++
under the settings menu. Tick the "enable line length indicator" checkbox and change the maximum
number of characters as necessary. When the feature is enabled you will hear a beep when scrolling
across lines that are too long or characters that are over the maximum length. Alternatively, you
can press NVDA+g to jump to the first overflowing character on the active line.

### Move to Matching Brace

In Notepad++ you can move to the matching brace of a program by pressing control+b. 
To move You must be one character inside the brace that you wish to match.
When you press this command, nvda will read the line you landed on, and if the line consists of only a brace, it will read the line above and below the brace so you can get a feel for context.

### Autocomplete

The Autocomplete functionality of Notepad++ is not accessible by default. The autocomplete has many problems, including that it shows up in a floating window. To make this functionality accessible, three things are done. 

1. When an autocomplete suggestion appears, a whoosh sound is played. The reverse sound is made when the suggestions disappear.
2. Pressing the down/up arrows read the next/previous suggested text. 
3. The recommended text is spoken when the suggestions appear.

### Keyboard Shortcut Mapper

Sometimes you have to add or change the keyboard shortcuts in Notepad++. 
For example, you might record a macro to remove the last character of a line on every line.
If you set a keyboard shortcut for this macro, or wish to change a keyboard shortcut for another command in the editor, you will go to the preferences menu, and then go to the keyboard shortcuts dialog.
Unfortunately, the keyboard shortcuts dialog is not friendly to NVDA by default. This add-on makes this dialog accessible. You can tab between the components and press the arrow keys to manipulate the controls like you would for any other dialog.

### Incremental Search

One of the most interesting features of Notepad++ is the ability to use incremental search. 
Incremental search is a search mode in which you search for a phrase of test by typing in the edit field, and the document scrolls to show you the search in real time. 
As you type, the document scrolls to show the line of text with the most likely phrase you are looking for. It also highlights the text that matched.
The program also shows you how many matches have been detected. There are buttons to move to the next and previous match.
As you type, NVDA will announce the line of text that Notepad++ detected a search result in. NVDA also announces how many matches there are, but only if the number of matches has changed. 
When you found the line of text you want, simply press escape, and that line of text will be at your cursor.
To launch this dialog, select incremental search from the search menu, or press alt+control+i.

### Reporting Information about the Current Line

Pressing nvda+shift+\ (back slash) at any time will report the following:

* the line number
* the column number I.E. how far into the line you are.
* the selection size, (number of characters horizontally selected, followed by the number of characters vertically selected, which would make a rectangle. This info is only reported if relevant.

### Support for the Previous/Next Find Feature

By Default, if you press control+f you bring up the find dialog. 
If you type text here and press enter, the text in the window is selected and the document is moved to the next search result. 
In Notepad++ you can press f3 or shift+f3 to repeat the search in the forward or backward direction respectively. 
NVDA will read both the current line, and the selection within the line which represents the found text.

### Preview of MarkDown or Hypertext as Webpage

Notepad++ does natively not support MarkDown (*.md) with e.g. language highlighting. 
However, you can preview such content as browsable message if you press NVDA+H (Escape to close the message). 
Pressing NVDA+Shift+H will open it in your standard browser. 
Some popular Markdown extensions such as PHP Extra or TOC are supported. 
It works also with (single-paged) Html. 

To try it out, Copy the following block, paste it into a new Notepad++ document and press NVDA+H:

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

# NonDdefault Notepad++ Keyboard Shortcuts

This add-on expects that Notepad++ is being used with the default shortcut keys. 
If this is not the case, please change this app module's key commands to reflect your Notepad++ commands as necessary in NVDA's input gestures dialog.
All of the add-ons commands are under the Notepad++ section.