# 小型图书馆管理系统-library management system

## Technology stack
1. python3
2. PyQt5
3. Sqlite3

> 实现以下功能:
- Store book information, purchase and elimination, and rental status
- Achieve book purchasing, elimination, and lending functions.
- Actualise book information, procurement and elimination, inventory, and rental inquiry
- Actualise the statistics of purchasing, inventory, elimination, and rental of books

- [ ] readers recommandation
- [ ] book I like
- [ ] book I collection

## General idea

As a management system, it is natural to implement both administrator and student content.

First need to log in and register the page
For the administrator, on the administrator's management page, the purchase, elimination, inventory, rental situation query and statistics of the book will be realized.
For students, it is necessary to realize the borrowing, returning, and renting of books.

## Usage

Install all the require packages
```python3
pip3 install -r requirement.txt
```
run the admin GUI:
```python3
python3 AdminHome.py
```
