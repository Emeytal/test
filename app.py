import yfinance as yf
from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/')
def home():
    print("Fetching data for the home page...")
    aapl_ticker = get_aapl_ticker()
    options_data_all_dates = []
    columns_to_display = ['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest']

    if aapl_ticker:
        expiration_dates = get_option_expiration_dates(aapl_ticker)
        if expiration_dates:
            print(f"Found {len(expiration_dates)} option expiration dates.")
            for date in expiration_dates:
                print(f"Fetching option chain for date: {date}")
                calls_df, puts_df = get_option_chain_for_date(aapl_ticker, date)
                
                item = {'date': date}
                if calls_df is not None and not calls_df.empty:
                    # Ensure only existing columns are selected to avoid KeyErrors
                    present_columns_calls = [col for col in columns_to_display if col in calls_df.columns]
                    item['calls_html'] = calls_df[present_columns_calls].to_html(index=False, classes=['options-table'])
                else:
                    item['calls_html'] = "<p>No call options available for this date.</p>"

                if puts_df is not None and not puts_df.empty:
                    # Ensure only existing columns are selected to avoid KeyErrors
                    present_columns_puts = [col for col in columns_to_display if col in puts_df.columns]
                    item['puts_html'] = puts_df[present_columns_puts].to_html(index=False, classes=['options-table'])
                else:
                    item['puts_html'] = "<p>No put options available for this date.</p>"
                
                options_data_all_dates.append(item)
            
            # Verification print (simplified as DataFrames are now HTML)
            if options_data_all_dates:
                print(f"\nProcessed data for {len(options_data_all_dates)} expiration dates.")
                first_date_data = options_data_all_dates[0]
                print(f"Data for first date ({first_date_data['date']}) includes HTML for calls and puts.")
            else:
                print("\nNo option data processed.")
        else:
            print("Could not retrieve option expiration dates.")
    else:
        print("Could not retrieve AAPL ticker object.")
    
    return render_template('index.html', options_data=options_data_all_dates)

if __name__ == "__main__":
    # Note: Setting use_reloader=False for this specific environment
    # to avoid issues with yfinance fetching data twice on startup in debug mode.
    # For general development, use_reloader=True (default for debug=True) is common.
    app.run(debug=True, use_reloader=False)
