from etls.currency_exchange_etl import fetch_exchange_rates, extract_exchange_rates, transform_exchange_data, save_data_to_csv
from utils.constants import ACCESS_KEY, API_URL, OUTPUT_PATH


def currency_exchange_pipeline(file_name: str, subreddit: str, time_filter='day', limit=None):
    # connecting to reddit instance
    raw_data = fetch_exchange_rates(API_URL, ACCESS_KEY)
    # extraction
    extracted_data = extract_exchange_rates(raw_data)
    # transformation
    transformed_data = transform_exchange_data(extracted_data,target_base="PKR")
    # loading to csv
    file_path = f'{OUTPUT_PATH}/{file_name}.csv'
    save_data_to_csv(transformed_data, path=file_path)
    return file_path