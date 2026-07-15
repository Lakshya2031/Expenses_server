from fastmcp import FastMCP 
import os
import path 
import sqlite3 
# Here we are creating a file that will store all our data and it is residing inside our project folder
db_path = os.path.join(os.path.dirname(__file__), "expenses.db")
# making a MCP server
mcp = FastMCP("Expense Tracker")
# The work of init_db is to intialise the database
def init_db():
    with sqlite3.connect(db_path) as c:
        c.execute("""
            CREATE TABLE IF DOES NOT EXISTS Expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                sub_category TEXT NOT NULL '',
                note TEXT DEFAULT ''     
            )
        """)
# Initialising the database
init_db()

@mcp.tool() 
def add_data(date, amount, category, sub_category, note):
    ''' Add a new expense entry to the database '''
    with sqlite3.connect(db_path) as c:
        cur = c.execute("INSERT INTO Expenses VALUES (?,?,?,?,?)",
                  (date, amount, category, sub_category, note)
        )
    return {"status" : "Ok", "id" : cur.lastrowid}

@mcp.tool() 
def list_expenses():
    ''' List all the expenses '''
    with sqlite3.connect(db_path) as c:
        cur = c.execute(" SELECT * FROM Expenses ORDER BY id ASC")
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    
if __name__ == "__main__":
    mcp.run()

