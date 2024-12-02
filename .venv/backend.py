import sqlite3
from tkinter import messagebox
import csv

def connect():
    """Connect to the SQLite database and create the book table if it doesn't exist."""
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER, total INTEGER DEFAULT 1)")
    conn.commit()
    conn.close()

def insert(title, author, year, isbn, total):
    """Insert a new book record into the database."""
    try:
        if not title or not isbn:
            messagebox.showwarning("Warning", "Please fill in the title and ISBN.")
            return

        if not year or not str(year).isdigit() or len(str(year)) != 4:
            messagebox.showwarning("Warning", "Please enter a valid year (4 digits).")
            return

        if not isinstance(total, int) or total < 1:
            messagebox.showwarning("Warning", "Total must be a positive integer.")
            return

        conn = sqlite3.connect("books.db")
        cur = conn.cursor()

        cur.execute("SELECT id, total FROM book WHERE title=? AND author=? AND year=? AND isbn=?", (title, author, year, isbn))
        result = cur.fetchone()

        cur.execute("SELECT * FROM book WHERE isbn=? AND (title!=? OR author!=? OR year!=?)", (isbn, title, author, year))
        isbn_check = cur.fetchone()

        if result:
            cur.execute("UPDATE book SET total = total + ? WHERE id=?", (total, result[0]))
            messagebox.showinfo("Success", f"The number of books was updated by {total}.")
        elif isbn_check:
            messagebox.showerror("Error", "A different book with this ISBN already exists.")
        else:
            cur.execute("INSERT INTO book (title, author, year, isbn, total) VALUES (?, ?, ?, ?, ?)", (title, author, year, isbn, total))
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")

        conn.commit()
        conn.close()

    except Exception as e:
        handle_error(e)

def view():
    """Return all book records from the database."""
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(title="", author="", year="", isbn=""):
    """Search for book records that match the given criteria."""
    try:
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()

        query = "SELECT * FROM book WHERE 1=1"
        params = []

        if title:
            query += " AND title=?"
            params.append(title)

        if author:
            query += " AND author=?"
            params.append(author)

        if year:
            if not str(year).isdigit() or len(str(year)) != 4:
                messagebox.showwarning("Warning", "Please enter a valid year (4 digits) for search.")
                return []
            query += " AND year=?"
            params.append(year)

        if isbn:
            query += " AND isbn=?"
            params.append(isbn)

        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return rows

    except Exception as e:
        handle_error(e)

def delete(id , total=1):
    """Delete the book record or decrease its total from the database."""
    try:
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()

        cur.execute("SELECT total FROM book WHERE id=?", (id,))
        result = cur.fetchone()

        if result is None:
            raise ValueError("The selected book does not exist in the database.")

        if result[0] > total:
            new_total = result[0] - total
            cur.execute("UPDATE book SET total = ? WHERE id=?", (new_total, id))
            messagebox.showinfo("Success", f"The number of books was updated by {total}.")

        elif result[0] == total:
            cur.execute("DELETE FROM book WHERE id=?", (id,))
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete all of this book?")

            if not confirm:
                return

        else:
            messagebox.showinfo("Success", "The entered total is less than the quantity. Please check the entered value and try again..")


        conn.commit()
        conn.close()

    except Exception as e:
        handle_error(e)

def delete_all(id):
    """Delete all copies of the book record with the given ID from the database."""
    try:
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete all of this book?")

        if not confirm:
            return

        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM book WHERE id=?", (id,))
        messagebox.showinfo("Success", "All of the books were deleted.")
        conn.commit()
        conn.close()

    except Exception as e:
        handle_error(e)

def update(id, title, author, year, isbn, total):
    """Update the book record with the given ID in the database."""
    try:
        if not id:
            messagebox.showwarning("Warning", "Please select a book to update.")
            return

        if not title or not author or not year or not isbn or total is None:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        if not str(year).isdigit() or len(str(year)) != 4:
            messagebox.showwarning("Warning", "Please enter a valid year (4 digits).")
            return

        if not str(total).isdigit() or int(total) < 1:
            messagebox.showwarning("Warning", "Total must be a positive integer.")
            return

        conn = sqlite3.connect("books.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM book WHERE isbn=? AND id!=?", (isbn, id))
        isbn_check = cur.fetchone()

        if isbn_check:
            messagebox.showerror("Error", "A different book with this ISBN already exists.")
            conn.close()
            return

        cur.execute("SELECT * FROM book WHERE isbn=? AND id!=?", (isbn, id))
        isbn_check = cur.fetchone()

        if isbn_check:
            messagebox.showerror ("Error", "A different book with this ISBN already exists.")
            conn.close()
            return

        cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=?, total=? WHERE id=?",
                    (title, author, year, isbn, total, id))
        messagebox.showinfo("Success", "Book was updated successfully.")

        conn.commit()
        conn.close()

    except Exception as e:
        handle_error(e)

def backup_to_csv(filename="books_backup.csv"):
    """Backup the database to a CSV file."""
    try:
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM book")
        rows = cur.fetchall()
        conn.close()

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Title", "Author", "Year", "ISBN", "Total"])
            writer.writerows(rows)

        return filename
    except Exception as e:
        handle_error(e)

def advanced_search(title="", author="", start_year="", end_year="", isbn=""):
    """Perform an advanced search for book records based on the given criteria."""
    try:
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()

        query = "SELECT * FROM book WHERE 1=1"
        params = []

        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")

        if author:
            query += " AND author LIKE ?"
            params.append(f"%{author}%")

        if start_year and start_year.isdigit():
            query += " AND year >= ?"
            params.append(start_year)

        if end_year and end_year.isdigit():
            query += " AND year <= ?"
            params.append(end_year)

        if isbn:
            query += " AND isbn LIKE ?"
            params.append(f"%{isbn}%")

        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return rows

    except Exception as e:
        handle_error(e)

def check_low_stock(threshold=5):
    """Check for books with stock lower than the specified threshold."""
    try:
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM book WHERE total < ?", (threshold,))
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        handle_error(e)
        return []

def handle_error(e):
    messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Connect to the database (create if it doesn't exist)
connect()
