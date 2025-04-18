# Accident Database Analysis Tool

This project provides a graphical interface for analyzing accident data stored in a SQLite database.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Place your CSV data files in the `csv` directory:
   - `vehicules-2023.csv`
   - `usagers-2023.csv`
   - `lieux-2023.csv`
   - `caract-2023.csv`

3. Initialize the database:
   ```
   python "sql/base sql python.py"
   ```

## Usage

1. Launch the graphical interface:
   ```
   python "interface graphique/interface_graphique_ctk.py"
   ```

2. Select the database file (`accidents.db`) when prompted.

3. Enter SQL queries in the text area and click "Execute" to run them.

4. Use the light/dark mode toggle to switch between themes.

## Sample Queries

The `sql/requetes.sql` file contains sample queries that can be used to analyze the accident data.

## Troubleshooting

- If you encounter issues with the CSV files, ensure they are properly formatted with semicolon (;) as the delimiter.
- Make sure all required dependencies are installed.
- Check that the database file exists and is accessible.
