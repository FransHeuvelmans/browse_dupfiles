# Browse Dupfiles
A dumb little program that lets me browse the output of `duplicity list-current-files` more easily.

This tool only helps me in browsing a backup. Making the stored files discoverable. Searching for particular
files can be done much faster using `grep` or one of its alternatives.
This program is not fast and not careful with memory use.

## Usage
First run `duplicity list-current-files ... > somelogfile` writing all the output to `somelogfile`.
Then load `somelogfile` in *Browse Dejadup* by running `python src/browse_dejadup somelogfile` to
start browsing. Or pip-install the program and run `python -m browse_dejadup somelogfile`.

## Modes
There are 2 modes. A more faux shell and a ncurses based browser. By default it starts the curses one.

Add `--prmpt`

* **ls**: Simple list of all the files
* **cd dirname / ..**: Change directory either up or down to one of the directories/files
* **ll**: A list underneath each dir/file
* **name**: Name of the current file/dir
* **pwd**: The full "path" of the current location
* **q**: Quit

Note: These commands only implement the **most basic** parts of command and nothing more.