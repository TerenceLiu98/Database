# library management system

*based on<a href = "https://github.com/ycdxsb/LibraryManageDesktopApp">Library ManageMent System</a>* 

## Technology stack

1. python3
2. PyQt5
3. Sqlite3

> Function:
- Store book information, purchase and elimination, and rental status
- Achieve book purchasing, elimination, and lending functions.
- Actualise book information, procurement and elimination, inventory, and rental inquiry
- Actualise the statistics of purchasing, inventory, elimination, and rental of books

> Need to do:
- [ ] readers recommandation
- [ ] book I like
- [ ] book I collection

## General idea

As a management system, it is natural to implement both administrator and student content.

First need to log in and register the page
For the administrator, on the administrator's management page, the purchase, elimination, inventory, rental situation query and statistics of the book will be realized.
For students, it is necessary to realize the borrowing, returning, and renting of books.

## Usage (virtualenv + pip3)

1. install virtualenv 
```shell
pip3 install virtualenv
```

2. install dependencies 
```shell
pip3 install -r requirements.txt
```
3. Install all the require packages

4. Run the Admin GUI
```python3
pip3 install -r requirement.txt
```
5. Run the admin GUI:
```python3
python3 AdminHome.py
```
Run the User GUI: 
```python3
python3 MainWindow.py
```

