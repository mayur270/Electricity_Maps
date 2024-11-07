"""Reusable components"""

import os
import re
from datetime import datetime
from typing import Any, Dict

import pandas as pd
from pydantic import BaseModel, ValidationError

from exceptions import CsvFileError, DataValidationError
from log import logger


def data_validation(
    schema_model: BaseModel,
    api_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Schema validation for data type.

    :param schema_model: Pydantic model for data validation.
    :param api_data: Data from api request.

    :returns: Validated data for data type.
    """
    try:
        validated_data = schema_model.model_validate(api_data)
        return validated_data.model_dump()
    except ValidationError as val_error:
        msg = f'Incorrect input data: {val_error.json()}'
        logger.error(msg)
        raise DataValidationError(msg)
    except Exception as data_exp:
        msg = f'This error relates to: {data_exp}'
        logger.error(msg)
        raise DataValidationError(msg)


def output_filepath(filename: str, directory: str = None) -> str:
    """Filepath for saving.

    :param filename: Name of file.
    :param directory: Location of file.

    :returns: filepath in str format.
    """
    if re.search(r"[\\/ ]", filename):
        raise ValueError(
            f"Filename, {filename}, contains '\\', '/', or space."
        )

    if not directory:
        current_dir = os.getcwd()
        directory = f'{current_dir}/results/'

    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as os_error:
        msg = f'OS Error due to: {os_error}'
        logger.error(msg)
        raise OSError(msg)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{filename}_{timestamp}.csv'
    filepath = os.path.join(directory, filename)
    return filepath


def write_to_csv(
    df: pd.DataFrame = None,
    filepath: str = None,
    **kwargs: dict[str, Any],
) -> None:
    """Saving to CSV file.

    :param df: Pandas DataFrame with carbon intensity data.
    :param filepath: Filepath for saving.
            Retrieved from output_filepath function.
    :param kwargs: Keyword arguments related to saving file via dataframe.

    :returns: message acknowledgement when file created.
    """
    if not filepath:
        logger.error("File path does not exist")
        raise ValueError("File path does not exist.")

    try:
        df.to_csv(filepath, **kwargs)
        return logger.info(f'Successfully created {filepath}!')
    except Exception as csv_exp:
        msg = f'This error relates to: {csv_exp}'
        logger.error(msg)
        raise CsvFileError(msg)
