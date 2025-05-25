# AAPL Options Web Viewer

This project is a simple web application that displays Apple (AAPL) stock options fetched from Yahoo Finance. It presents the option chains (calls and puts) in a tabbed interface, where each tab represents a different expiration date.

## Prerequisites

*   Python 3 (3.7 or newer recommended)
*   pip (Python package installer, usually comes with Python)

## Setup & Running

1.  **Clone the Repository (if applicable):**
    If you've downloaded this as a ZIP, extract it. If it's a Git repository, clone it.
    ```bash
    # git clone <repository_url> # If applicable
    cd <project_directory>
    ```

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    # For Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .
env\Scriptsctivate
    ```

3.  **Install Dependencies:**
    Install the required Python libraries using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Web Application:**
    Start the Flask development server.
    ```bash
    python app.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/` in your web browser. The console output will confirm the address.

## Features

*   Fetches all available option expiration dates for AAPL from Yahoo Finance.
*   Displays call and put options for each expiration date in separate tables.
*   Tabbed interface for easy navigation between different expiration dates.
*   Shows Strike, Last Price, Bid, Ask, Volume, and Open Interest for each option.

## Known Limitations

*   **Option Greeks (Delta, Gamma, etc.):** This application does not display option Greeks like Delta or Gamma. The `yfinance` library, in its standard option chain fetching, does not provide this data directly.
