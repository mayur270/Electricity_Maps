"""Util unit tests."""

from unittest.mock import patch

import pandas as pd
import pytest
from pydantic import BaseModel, ValidationError

from exceptions import CsvFileError, DataValidationError
from utils.util import data_validation, output_filepath, write_to_csv


class MockSchemaModel(BaseModel):
    key: str


def test_data_validation_success():
    api_data = {"key": "value"}
    validated_data = data_validation(MockSchemaModel, api_data)
    assert validated_data == api_data


def test_data_validation_error():
    api_data = {"wrong_key": "value"}
    with pytest.raises(DataValidationError):
        data_validation(MockSchemaModel, api_data)


def test_output_filepath_default_directory():
    filename = "testfile"
    with patch("os.makedirs") as mock_makedirs, patch(
        "os.getcwd", return_value="/current/dir"
    ):
        filepath = output_filepath(filename)
        assert filepath.startswith("/current/dir/results/testfile_")
        assert filepath.endswith(".csv")
        mock_makedirs.assert_called_once_with(
            "/current/dir/results/", exist_ok=True
        )


def test_output_filepath_custom_directory():
    filename = "testfile"
    directory = "/custom/dir"
    with patch("os.makedirs") as mock_makedirs:
        filepath = output_filepath(filename, directory)
        assert filepath.startswith("/custom/dir/testfile_")
        assert filepath.endswith(".csv")
        mock_makedirs.assert_called_once_with("/custom/dir", exist_ok=True)


def test_output_filepath_os_error():
    filename = "testfile"
    with patch("os.makedirs", side_effect=OSError("OS error")):
        with pytest.raises(OSError):
            output_filepath(filename)


def test_write_to_csv_csv_file_error():
    df = pd.DataFrame()
    filepath = "/path/to/file.csv"
    with patch(
        "pandas.DataFrame.to_csv", side_effect=CsvFileError("CSV file error")
    ):
        with pytest.raises(CsvFileError):
            write_to_csv(df, filepath)
