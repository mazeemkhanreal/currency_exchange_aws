import requests
import pandas as pd
import sys


def fetch_exchange_rates(api_url: str, access_key: str):
    """
    Fetch exchange rates with a fallback to the default base currency (EUR).
    """
    try:
        params = {"access_key": access_key}
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        print("Connected to Exchange Rates API with fallback base (EUR).")
        return response.json()
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        sys.exit(1)


def extract_exchange_rates(data: dict):
    """
    Extract exchange rates from the JSON response into a structured DataFrame.
    """
    date = data.get("date", None)
    base = data.get("base", None)
    rates = data.get("rates", {})

    # Flatten the data into a list of records
    records = [{"date": date, "base_currency": base, "currency": currency, "rate": rate}
               for currency, rate in rates.items()]

    return pd.DataFrame(records)


def transform_exchange_data(data: pd.DataFrame, target_base: str = "PKR") -> pd.DataFrame:
    """
    Transform exchange rates DataFrame to use a specific base currency (e.g., PKR).
    """
    # Check if the target base currency exists in the 'currency' column
    if target_base not in data['currency'].values:
        raise ValueError(f"{target_base} is not available in the exchange rates data.")

    # Get the rate of the target base currency (e.g., PKR)
    target_base_rate = data.loc[data['currency'] == target_base, 'rate'].iloc[0]

    # Recalculate the rates relative to the target base currency
    data['converted_rate'] = target_base_rate / data['rate']

    # Add a column for the base currency
    data['base_currency'] = target_base

    # Return the transformed DataFrame with relevant columns
    return data[['base_currency', 'currency', 'converted_rate', 'date']]


def save_data_to_csv(df: pd.DataFrame, path: str):
    """
    Save the DataFrame to a CSV file.
    """
    df.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")

