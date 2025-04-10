import streamlit as st
import json
import os

# Load library from file
def load_library():
    if os.path.exists("library.txt"):
        with open("library.txt", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Save library to file
def save_library(library):
    with open("library.txt", "w") as file:
        json.dump(library, file, indent=4)

# Initialize library in session
if 'library' not in st.session_state:
    st.session_state.library = load_library()

# Add Book
def add_book():
    st.subheader("➕ Add a Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.radio("Have you read this book?", ("Yes", "No"))

    if st.button("Add Book"):
        if title and author and genre:
            book = {
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read": True if read_status == "Yes" else False
            }
            st.session_state.library.append(book)
            save_library(st.session_state.library)
            st.success("Book added successfully!")
        else:
            st.warning("Please fill all fields.")

# Remove Book
def remove_book():
    st.subheader("❌ Remove a Book")
    titles = [book["title"] for book in st.session_state.library]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            st.session_state.library = [book for book in st.session_state.library if book["title"] != book_to_remove]
            save_library(st.session_state.library)
            st.success("Book removed successfully!")
    else:
        st.info("No books to remove.")

# Search Book
def search_book():
    st.subheader("🔍 Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author"])
    keyword = st.text_input(f"Enter {search_by.lower()}")

    if st.button("Search"):
        results = []
        for book in st.session_state.library:
            if keyword.lower() in book[search_by.lower()].lower():
                results.append(book)

        if results:
            for i, book in enumerate(results, 1):
                st.markdown(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No matching books found.")

# Display All Books
def display_books():
    st.subheader("📖 Display All Books")
    if st.session_state.library:
        for i, book in enumerate(st.session_state.library, 1):
            st.markdown(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        st.info("Library is empty.")

# Statistics
def display_statistics():
    st.subheader("📊 Library Statistics")
    total = len(st.session_state.library)
    read = sum(1 for book in st.session_state.library if book["read"])
    percent = (read / total * 100) if total else 0

    st.write(f"**Total Books:** {total}")
    st.write(f"**Books Read:** {read}")
    st.write(f"**Read Percentage:** {percent:.2f}%")

# Sidebar Menu
st.sidebar.title("📚 Personal Library Manager")
choice = st.sidebar.radio("Menu", [
    "Add a book",
    "Remove a book",
    "Search for a book",
    "Display all books",
    "Display statistics",
    "Exit"
])

# Main content handler
if choice == "Add a book":
    add_book()
elif choice == "Remove a book":
    remove_book()
elif choice == "Search for a book":
    search_book()
elif choice == "Display all books":
    display_books()
elif choice == "Display statistics":
    display_statistics()
elif choice == "Exit":
    st.balloons()
    st.success("Library saved. Goodbye!")
