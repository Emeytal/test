import yfinance as yf

def get_aapl_ticker():
    """
    Returns the yfinance.Ticker object for Apple Inc. (AAPL).
    """
    try:
        return yf.Ticker("AAPL")
    except Exception as e:
        print(f"Error creating Ticker object: {e}")
        return None

def get_option_expiration_dates(ticker):
    """
    Fetches and returns the list of option expiration dates for the given ticker.
    Args:
        ticker: yfinance.Ticker object.
    Returns:
        A list of option expiration dates, or None if an error occurs.
    """
    if ticker is None:
        return None
    try:
        return ticker.options
    except Exception as e:
        print(f"Error fetching option expiration dates: {e}")
        return None

def get_option_chain_for_date(ticker, date):
    """
    Fetches the option chain (calls and puts) for a given ticker and expiration date.
    Args:
        ticker: yfinance.Ticker object.
        date: String representing the expiration date (e.g., 'YYYY-MM-DD').
    Returns:
        A tuple containing two pandas DataFrames: (calls, puts).
        Returns (None, None) if an error occurs or data is not found.
    """
    if ticker is None:
        return None, None
    try:
        option_chain = ticker.option_chain(date)
        return option_chain.calls, option_chain.puts
    except Exception as e:
        print(f"Error fetching option chain for date {date}: {e}")
        return None, None

if __name__ == "__main__":
    print("Fetching AAPL option expiration dates...")
    aapl_ticker = get_aapl_ticker()
    if aapl_ticker:
        expiration_dates = get_option_expiration_dates(aapl_ticker)
        if expiration_dates:
            print("Available option expiration dates for AAPL will be processed below.\n")

            columns_to_display = ['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest']

            if not expiration_dates:
                print("No expiration dates found to fetch option chain.")
            else:
                for date in expiration_dates:
                    print(f"\n--- Options for Expiration Date: {date} ---")
                    calls_df, puts_df = get_option_chain_for_date(aapl_ticker, date)

                    if calls_df is not None and not calls_df.empty:
                        print("\nCALL OPTIONS:")
                        # Ensure only existing columns are selected to avoid KeyErrors
                        present_columns_calls = [col for col in columns_to_display if col in calls_df.columns]
                        if present_columns_calls:
                            print(calls_df[present_columns_calls].to_string())
                        else:
                            print("Selected columns not found in Calls DataFrame.")
                    else:
                        print("\nNo CALL OPTIONS data or an error occurred for this date.")

                    if puts_df is not None and not puts_df.empty:
                        print("\nPUT OPTIONS:")
                        # Ensure only existing columns are selected to avoid KeyErrors
                        present_columns_puts = [col for col in columns_to_display if col in puts_df.columns]
                        if present_columns_puts:
                            print(puts_df[present_columns_puts].to_string())
                        else:
                            print("Selected columns not found in Puts DataFrame.")
                    else:
                        print("\nNo PUT OPTIONS data or an error occurred for this date.")
                    
                    print("\n" + "-"*50 + "\n") # Separator
        else:
            print("Could not retrieve option expiration dates.")
    else:
        print("Could not retrieve AAPL ticker object.")

    # Attempt to install yfinance if it's not found and then retry.
    # This is a simple check; a more robust solution might involve checking specific import errors.
    # Note: This block might be redundant if yfinance is installed via requirements.txt beforehand.
    try:
        import yfinance
    except ImportError:
        print("\nyfinance not found. Attempting to install...")
        try:
            import subprocess
            subprocess.check_call(["python", "-m", "pip", "install", "yfinance"])
            print("yfinance installed successfully. Please re-run the script.")
        except Exception as e:
            print(f"Failed to install yfinance: {e}")
            print("Please install it manually by running: pip install yfinance")
