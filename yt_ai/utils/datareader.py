import pandas as pd
from yt_ai.utils.logger import logger


def read_data_csv(input_file):
    logger.info(f"Reading data file from {input_file}")    
    csv_data = pd.read_csv(input_file)
    return csv_data.set_index(["Id", "Prompts"])

    