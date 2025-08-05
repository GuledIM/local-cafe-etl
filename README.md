### GitHub Repo Description (short)

Café Order ETL Pipeline | Python, Docker & MySQL CLI & GUI Proof of Concept for local data management and PII-safe record storage.

### README.md

````markdown
# Café Order ETL Pipeline

This project is a Proof of Concept (PoC) for a local data management system designed to replace a paper-based order record system for a local café chain. The application extracts, transforms, and loads (ETL) order data from CSV files into a local MySQL database while ensuring data quality and removing Personally Identifiable Information (PII).

---

## Project Overview

The café required a simple yet effective solution to digitize their order records on a Microsoft Windows or macOS infrastructure. This ETL pipeline extracts raw order data, cleans and validates the data by removing incorrect or badly formed records, and scrubs sensitive PII such as card numbers and customer names before loading the sanitized data into a MySQL database.

Two user interfaces are included:
- **Command-Line Interface (CLI):** A menu-driven interface to manually trigger ETL pipeline functions and interact with the data.
- **Windows Graphical User Interface (GUI):** A simple GUI menu for non-technical users to perform the same ETL tasks more intuitively.

---

## Features

- [] Extract order data from CSV files
- [] Transform data by cleaning, validating, and removing PII
- [] Load sanitized data into a local MySQL database
- [] CLI and GUI menus to manually control the ETL process
- [] Display and clear screen functionality in the CLI
- [] Designed with Docker for easy deployment

---

## Technologies Used

- Python  
- MySQL  
- Docker  
- Flask or Tkinter (for Windows GUI) - Yet to decide
- pandas (for data transformation)  

---

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/cafe-order-etl.git
   cd cafe-order-etl
````

2. **Set up Docker and MySQL:**

   Ensure Docker is installed on your machine. The project includes a `docker-compose.yml` file to set up a local MySQL database container.

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database credentials:**

   Update the `config.py` or environment variables with your local MySQL credentials.

---

## Usage

* **CLI:** Run `python cli_menu.py` to launch the command-line interface.
* **GUI:** Run `python gui_menu.py` to open the graphical user interface.

Within both interfaces, users can:

* Trigger Extract, Transform, and Load functions individually
* View sanitized data summaries
* Clear the console screen (CLI only)

---

## Project Deliverables

* **Product Demo:** Showcase of all application functions (approx. 5 mins)
* **Client Presentation:** Highlighting benefits such as improved data accuracy, PII compliance, and easier record-keeping (approx. 5 mins)
* **Whiteboard Session:** Explanation of design choices, architecture, and alternatives considered (approx. 5 mins)

---

## Reflections & Progress

This project provided valuable experience in:

* Building ETL pipelines using Python and MySQL
* Designing dual interfaces (CLI and GUI) for different user types
* Data cleaning and PII removal techniques
* Using Docker to containerize and simplify deployment

---

## Future Improvements

* Add automated scheduling for ETL runs
* Implement role-based access control in GUI
* Extend database schema for expanded order analytics
* Enhance GUI with better UX design and error handling

---

## License

This project is licensed under the MIT License.

