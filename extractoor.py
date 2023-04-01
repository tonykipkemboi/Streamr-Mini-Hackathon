import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import logging
from logging_config import configure_logging


def get_magnitude_scale_description(magnitude):
    """
    Get the description of the earthquake magnitude scale.

    Args:
        magnitude (float): Earthquake magnitude value.

    Returns:
        str: Description of the earthquake magnitude scale.
    """

    magnitude_scale = {
        (0, 1.9): 'Micro',
        (2, 2.9): 'Minor',
        (3, 3.9): 'Light',
        (4, 4.9): 'Moderate',
        (5, 5.9): 'Strong',
        (6, 6.9): 'Major',
        (7, 7.9): 'Great',
        (8, 10): 'Exceptional'
    }
    for magnitude_range, description in magnitude_scale.items():
        if magnitude_range[0] <= magnitude <= magnitude_range[1]:
            return description
    return 'Unknown'


def get_earthquake_data():
    """
    Retrieve and process earthquake data from the EMSC RSS feed.

    Returns:
        pd.DataFrame: DataFrame containing earthquake data.
    """
    url = "https://www.emsc-csem.org/service/rss/rss.php?typ=emsc"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to retrieve data, status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')

    magnitudes = []
    magnitude_descriptions = []
    regions = []
    date_times = []
    locations = []
    depths = []

    utc = pytz.timezone('UTC')
    est = pytz.timezone('US/Eastern')

    for item in items:
        description = item.find('description').text

        desc_soup = BeautifulSoup(description, 'html.parser')
        details = desc_soup.find_all('td', class_='point2')

        magnitude = float(details[0].text.strip().split()[1])
        magnitudes.append(magnitude)
        magnitude_descriptions.append(
            get_magnitude_scale_description(magnitude))

        regions.append(details[1].text.strip())

        # Convert date time to EST
        date_time_utc = datetime.strptime(
            details[2].text.strip(), '%Y-%m-%d %H:%M:%S.%f UTC')
        date_time_utc = utc.localize(date_time_utc)
        date_time_est = date_time_utc.astimezone(est)
        date_times.append(date_time_est.strftime('%Y-%m-%d %H:%M:%S %Z'))

        locations.append(details[3].text.strip())
        depths.append(details[4].text.strip())

    df = pd.DataFrame({
        'Magnitude': magnitudes,
        'Magnitude Scale': magnitude_descriptions,
        'Region': regions,
        'Date time': date_times,
        'Location': locations,
        'Depth': depths
    })

    # Convert the DataFrame to a list of dictionaries
    earthquake_data = df.to_dict(orient='records')

    return earthquake_data


if __name__ == "__main__":
    configure_logging()
    logging.info('Starting the extractor...')
    earthquake_data = get_earthquake_data()
    logging.info('Retrieved earthquake data:')
    logging.info(earthquake_data)
