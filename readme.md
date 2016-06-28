# Notepad++ Add-on for NVDA.

This add-on improves the accessibility of notepad++. Notepad++ is a text editor for windows, and has many features. You can learn more about  it at https://notepad-plus-plus.org/

## Features:

### Support for bookmarks.

Notepad++ allows you to set bookmarks in your text.
A bookmark allows you to quickly come back to a location in the editor at any point.
To set a bookmark, from the line you wish to bookmark, press control+f2.
Then,  when you want to come back to this bookmark, press f2 to jump to the next  bookmark, or shift+f2 to jump backwards to the previous one.
You can set as many bookmarks as you would like.

### Maximum line length announcement
`<write me please>`

### Move to matching brace.

In Notepad++ you can move to the matching brace of a program by pressing control+b. 
To move You must be one character inside the  brace that you wish to match.
When you press this command, nvda will read the line you landed on, and if the line consists of only a brace, it will read the line above and below the bace so you can get a feel for context.

### Keyboard shortcut mapper.

Sometimes you have to add or change the keyboard shortcuts in Notepad++. 
For example, you might record a macro to remove the last character of a line on every line.
If you set a keyboard shortcut for this macro, or wish to change a keyboard shortcut for another command in the editor, you will go to the preferences menu, and then go to the keyboard shortcuts dialog.
Unfortunately, the keyboard shortcuts dialog is not friendly to NVDA by default. This add-on makes this dialog accessible. You can tab between the components and press the arrow keys to manipulate the controls like you would for any other dialog.

### Incremental search

One of the most interesting features of notepad++ is the ability to use incremental search. 
Incremental search is a search mode in which you search for a phrase of test by typing in the edit field, and the document scrolls to show you the search in real time. 
As you type, the document scrolls to show the line of text with the most likely phrase you are looking for. It also highlights the text that matched.
The program also shows you how many matches have been detected. There are buttons to move to the next and previous match.
As you type, NVDA will announce the line of text that notepad++ detected a search result in. NVDA also announces how many matches there are, but only if the number of matches has changed. 
When you found the line of text you want, simply press escape, and that line of text will be at your cursor.
To launch this dialog, select incremental search from the search menu, or press alt+control+i.

### Reporting information about the  current line

Pressing nvda+shift+\ (back slash) at any time will report the following:

* the line number
* the column number I.E. how far into the line you are.
* the selection size, (number of characters horizontally selected, followed by a | symbol, followed by the number of characters vertically selected, which would make a rectangle.

