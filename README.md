# Browse Dejadup
A dumb little program that lets me browse the output of `duplicity list-current-files` more easily.
Check TODO for future plans.


## Usage
First run `duplicity list-current-files ... > somelogfile` writing all the output to `somelogfile`.
Then load `somelogfile` in *Browse Dejadup* by running `python src/browse_dejadup somelogfile` to
start browsing. Or pip-install the program and run `python -m browse_dejadup somelogfile`.

### Commands

* **ls**: Simple list of all the files
* **cd dirname / ..**: Change directory either up or down to one of the directories/files
* **ll**: A list underneath each dir/file
* **name**: Name of the current file/dir
* **pwd**: The full "path" of the current location
* **q**: Quit

Note: These commands only implement the **most basic** parts of command and nothing more.