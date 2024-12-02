from tkinter import *
from tkinter import ttk
import backend
from tkinter import messagebox, END
from tkinter import Toplevel

selected_tuple = None
sort_reverse = False

def sort_column(tree, col):
    """Sort the specified column in the treeview."""
    global sort_reverse
    data = [(tree.item(child)["values"], child) for child in tree.get_children()]
    try:
        data.sort(
            key=lambda x: (
                float(x[0][col]) if is_number(x[0][col]) else str(x[0][col]).lower()
            ),
            reverse=sort_reverse
        )

    except Exception as e:
        data.sort(key=lambda x: str(x[0][col]).lower(), reverse=sort_reverse)

    for child in tree.get_children():
        tree.delete(child)

    for values, _ in data:
        tree.insert("", "end", values=values)

    sort_reverse = not sort_reverse

def get_selected_row(event):
    """Retrieve the selected row data and display it in the input fields."""
    global selected_tuple
    selected = tree.focus()
    if not selected:
        return
    selected_tuple = tree.item(selected, 'values')
    entries = [e1, e2, e3, e4, e5]
    for i, entry in enumerate(entries, start=1):
        entry.delete(0, END)
        entry.insert(END, selected_tuple[i])

def add_command():
    """Add a new book record to the database."""
    try:
        title = title_text.get()
        author = author_text.get()
        year = year_text.get()
        isbn = isbn_text.get()
        total = total_text.get()

        if not title or not author or not year or not isbn or not total:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        if total == "" or total <= 0:
            messagebox.showwarning("Warning", "Total must be a positive number.")
            return

        total = int(total)
        backend.insert(title, author, year, isbn, total)
        view_command()

    except Exception as e:
        handle_error(e)

def view_command():
    """View all records in the database."""
    new_command()
    try:
        tree.delete(*tree.get_children())

        for row in backend.view():
            tag = "low_stock" if int(row[5]) < 5 else ""
            tree.insert("", END, values=row, tags=(tag,))

        tree.tag_configure("low_stock", background="yellow")

    except Exception as e:
        handle_error(e)

def search_command():
    """Search for records that match the input criteria."""
    try:
            tree.delete(*tree.get_children())
            title = title_text.get().strip()
            author = author_text.get().strip()
            year = year_text.get().strip()
            isbn = isbn_text.get().strip()
            rows = backend.search(title, author, year, isbn)

            if not title and not author and not year and not isbn:
                messagebox.showwarning("Warning", "Please fill in at least one field to search.")
                view_command()
                return
            if not rows:
                messagebox.showinfo("Info", "No results found.")
                view_command()
            else:
                for row in rows:
                    row = [str(value) for value in row]
                    tree.insert("", END, values=row)
    except Exception as e:
        handle_error(e)

def delete_command():
    """Delete the selected book record from the database."""
    try:
        if not selected_tuple:
            messagebox.showwarning("Warning", "Please select a book to delete.")
            return

        total_to_delete = int(total_text.get())

        if total_to_delete <= 0:
            messagebox.showwarning("Warning", "Please enter a valid number greater than 0.")
            return

        backend.delete(selected_tuple[0], total_to_delete)

        view_command()

    except Exception as e:
        handle_error(e)
        view_command()

def delete_all_command():
    """Delete all book records from the database."""
    try:
        if not selected_tuple:
            messagebox.showwarning("Warning", "Please select a book to delete.")
            return

        backend.delete_all(selected_tuple[0])
        view_command()

    except Exception as e:
        handle_error(e)

def update_command():
    """Update the selected book record in the database."""
    try:
        if not selected_tuple:
            messagebox.showwarning("Warning", "Please select a book to update.")
            return

        title = title_text.get()
        author = author_text.get()
        year = year_text.get()
        isbn = isbn_text.get()
        total = total_text.get()

        if not title or not author or not year or not isbn:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        backend.update(selected_tuple[0], title, author, year, isbn, total)
        view_command()

    except Exception as e:
        handle_error(e)

def new_command():
    """Clear the input fields for a new entry."""
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    global selected_tuple
    selected_tuple = None

def backup_command():
    """Create a backup of the database and save it to a CSV file."""
    try:
        filename = backend.backup_to_csv()
        messagebox.showinfo("Success", f"Backup completed successfully!\nFile saved as: {filename}")
    except Exception as e:
        handle_error(e)

def open_advanced_search():
    """Open the advanced search window."""
    top = Toplevel(window)
    top.title("Advanced Search")

    top.geometry("350x200")
    top.resizable(False, False)

    l1 = Label(top, text="Title (Contains)")
    l1.grid(row=0, column=0)
    title_filter_text = StringVar()
    e1 = Entry(top, textvariable=title_filter_text)
    e1.grid(row=0, column=1)

    l6 = Label(top, text="Start Date (Year)")
    l6.grid(row=1, column=0)
    start_year_text = StringVar()
    validate_year_cmd = top.register(validate_year)
    e6 = Entry(top, textvariable=start_year_text, validate="key", validatecommand=(validate_year_cmd, "%P"))
    e6.grid(row=1, column=1)

    l7 = Label(top, text="End Date (Year)")
    l7.grid(row=2, column=0)
    end_year_text = StringVar()
    e7 = Entry(top, textvariable=end_year_text, validate="key", validatecommand=(validate_year_cmd, "%P"))
    e7.grid(row=2, column=1)

    l8 = Label(top, text="Author (Contains)")
    l8.grid(row=3, column=0)
    author_filter_text = StringVar()
    e8 = Entry(top, textvariable=author_filter_text)
    e8.grid(row=3, column=1)

    l9 = Label(top, text="ISBN (Contains)")
    l9.grid(row=4, column=0)

    isbn_filter_text = StringVar()
    e9 = Entry(top, textvariable=isbn_filter_text)
    e9.grid(row=4, column=1)

    b10 = Button(top, text="Search",command=lambda: advanced_search_command(title_filter_text.get(), author_filter_text.get(),
                                                             start_year_text.get(), end_year_text.get(),
                                                             isbn_filter_text.get(), top))
    b10.grid(row=5, columnspan=2)

def advanced_search_command(title, author, start_year, end_year, isbn, top_window):
    """Perform an advanced search based on the input criteria."""
    try:
        tree.delete(*tree.get_children())

        if not title and not author and not start_year and not end_year and not isbn:
            messagebox.showwarning("Warning", "Please fill in at least one field to search.")
            return

        rows = backend.advanced_search(title, author, start_year, end_year, isbn)

        if not rows:
            messagebox.showinfo("Info", "No results found.")
        else:
            for row in rows:
                row = [str(value) for value in row]
                tree.insert("", END, values=row)

        top_window.destroy()

    except Exception as e:
        handle_error(e)

def low_stock_command():
    """Check and display books with low stock."""
    try:
        threshold = 5
        low_stock_books = backend.check_low_stock(threshold)

        if not low_stock_books:
            messagebox.showinfo("Info", f"No books with stock less than {threshold}.")
            return

        tree.delete(*tree.get_children())
        for row in low_stock_books:
            tree.insert("", END, values=row)

        messagebox.showwarning("Low Stock", f"Books with stock less than {threshold} are displayed.")
    except Exception as e:
        handle_error(e)

def is_number(value):
    """Check if the given value is a number."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def validate_year(new_value):
    """Validate that the year input is a four-digit number."""
    if new_value.isdigit() and len(new_value) <= 4:
        return True
    elif new_value == "":
        return True
    else:
        return False

def get_total_input(new_value):
    """Validate that the total input is a digit number."""
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False

def handle_error(e):
    messagebox.showerror("Error", f"An error occurred: {str(e)}")

window = Tk()
window.wm_title("Book Store")

window.geometry("1200x300")
window.resizable(False, False)

# inputs
l1 = Label(window, text="Title")
l1.grid(row=0, column=0)

l2 = Label(window, text="Author")
l2.grid(row=0, column=2)

l3 = Label(window, text="Year")
l3.grid(row=1, column=0)

l4 = Label(window, text="ISBN")
l4.grid(row=1, column=2)

l5 = Label(window, text="Total")
l5.grid(row=2, column=0)

title_text = StringVar()
e1 = Entry(window, textvariable=title_text)
e1.grid(row=0, column=1)

author_text = StringVar()
e2 = Entry(window, textvariable=author_text)
e2.grid(row=0, column=3)

vcmd = window.register(validate_year)
year_text = StringVar()
e3 = Entry(window, textvariable=year_text, validate="key", validatecommand=(vcmd, "%P"))
e3.grid(row=1, column=1)

isbn_text = StringVar()
e4 = Entry(window, textvariable=isbn_text)
e4.grid(row=1, column=3)

gti = window.register(get_total_input)
total_text = IntVar()
e5 = Entry(window, textvariable=total_text, validate="key", validatecommand=(gti, "%P"))
e5.grid(row=2, column=1)

# list
tree = ttk.Treeview(window, columns=("ID", "Title", "Author", "Year", "ISBN", "Total"), show="headings", height=8)
tree.grid(row=4, column=0, columnspan=6)

tree.heading("ID", text="ID", command=lambda: sort_column(tree, 0))
tree.heading("Title", text="Title", command=lambda: sort_column(tree, 1))
tree.heading("Author", text="Author", command=lambda: sort_column(tree, 2))
tree.heading("Year", text="Year", command=lambda: sort_column(tree, 3))
tree.heading("ISBN", text="ISBN", command=lambda: sort_column(tree, 4))
tree.heading("Total", text="Total", command=lambda: sort_column(tree, 5))

tree.bind('<ButtonRelease-1>', get_selected_row)

# buttons
b1 = Button(window, text="View all", width=12, command=view_command)
b1.grid(row=3, column=0)

b2 = Button(window, text="Search Book", width=12, command=search_command)
b2.grid(row=3, column=1)

b3 = Button(window, text="Add Book", width=12, command=add_command)
b3.grid(row=1, column=4)

b4 = Button(window, text="Update Book", width=12, command=update_command)
b4.grid(row=3, column=3)

b5 = Button(window, text="Delete selected", width=12, command=delete_command)
b5.grid(row=3, column=4)

b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=0, column=5)

b7 = Button(window, text="New", width=12, command=new_command)
b7.grid(row=0, column=4)

b8 = Button(window, text="Delete All", width=12, command=delete_all_command)
b8.grid(row=3, column=5)

b9 = Button(window, text="Backup", width=12, command=backup_command)
b9.grid(row=1, column=5)

b10_main = Button(window, text="Advanced Search", width=12, command=open_advanced_search)
b10_main.grid(row=3, column=2)

b11 = Button(window, text="Low Stock", width=12, command=low_stock_command)
b11.grid(row=2, column=5)

view_command()
window.mainloop()
