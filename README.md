
# Book Store Management System

This is a Book Store Management System built using Python and Tkinter for the frontend, and SQLite for the backend. 
The system allows users to manage a book store database, including adding, updating, searching, and deleting book records.

## Features

- **Add a Book**: Add a new book to the database.
- **Update a Book**: Update the details of an existing book.
- **Delete a Book**: Delete a specific book from the database.
- **View All Books**: Display all books in the database.
- **Search Books**: Search for books by title, author, year, or ISBN.
- **Advanced Search**: Perform an advanced search with more specific criteria.
- **Low Stock**: View books with low stock (less than 5).
- **Backup**: Create a backup of the database to a CSV file.
- **Delete All Copies**: Delete all copies of a specific book.

## Installation

### Prerequisites
- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- SQLite3 (usually comes pre-installed with Python)

### Steps to Install and Run

1. **Download the Project:**  
   You can download the project by following these steps:  

   - Go to the project’s GitHub page.
   - Click on the **Code** button.
   - Choose **Download ZIP**.
   - Extract the ZIP file on your computer.

2. **Opening the Project in VS Code or PyCharm:**  
   Once you've downloaded and extracted the ZIP file, you can open the project in either VS Code or PyCharm:

   - **In VS Code:**  
     - Open VS Code.
     - Click on **Open Folder** and select the folder where you extracted the project.
     - The project files will now appear in the VS Code editor.

   - **In PyCharm:**  
     - Open PyCharm.
     - Click on **File > Open** and select the folder where you extracted the project.
     - PyCharm will load the project for you to view and work on.

3. **Running the Program:**  
   Once the project is open in your preferred IDE, follow these steps:  

   - Locate the `frontend.py` file in the project folder.
   - **To run the frontend:** Simply run the `frontend.py` file to start the Book Store Management System.
     - **In VS Code:** Right-click the `frontend.py` file and choose **Run Python File**.
     - **In PyCharm:** Click the green play button or right-click and select **Run**.

   Alternatively, if you have Git installed on your system, you can clone the repository using the following command in your terminal:

     - git clone https://github.com/177smohammadzadeh/Bookstore-Management-System.git
   
     - cd book-store-management


## How to Use
### Adding a Book
   - Fill in the details such as title, author, year, ISBN, and total quantity, then click Add Book. Make sure to enter the Total field.
### View All Books
   - To display all book records, simply click the View All button. This will fetch all the books currently stored in the Database.
### Searching for Books
  -  To search for a book, fill in any of the fields (Title, Author, Year, ISBN) and click Search Book Advanced Search.
### Advanced Search
   - Click Advanced Search to search using multiple criteria like title, author, year range, or ISBN.
### Updating a Book
   - To Select a book from the list, fill in the updated information, and click Update Book.
### Delete Selected (Single Copy)
   - If you want to delete a specific number of copies of a book, first select the book from the table by clicking on its row. Then, in the Total  input field, enter the number       of copies to be deleted. After entering the number, click the Delete Selected button.
### Delete All (All Copies)
   - If you want to completely remove a book from the database, select the desired book from the table by clicking on its row. Then click the Delete All button.
### Backup
   - Click Backup to create a backup of the database in CSV format. The file will be saved in the same directory where the application is running, and the file name is                Books_Backup.csv.
### Low Stock
   - Click Low Stock to view books with a quantity lower than 5.

## File Structure

   /book-store-management

   - frontend.py    # Frontend script with the Tkinter UI

   - backend.py     # Backend script for database operations

   - books.db       # SQLite database file

## Backend Functions

The backend file `backend.py` contains the functions for interacting with the SQLite database. The system supports basic operations like:

- Connecting to the database
- Inserting, updating, and deleting book records
- Searching for books
- Creating a backup of the database
- Advanced search based on specific fields
- Checking low stock

## Acknowledgements

- Python and Tkinter for the GUI
- SQLite for database management
- `messagebox` for displaying alerts and warnings
