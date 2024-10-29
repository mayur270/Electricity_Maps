"""Unit tests for carbon_intensity_history_view."""

from unittest.mock import patch

import pandas as pd
import pytest

from views.carbon_intensity_history_view import CarbonIntensityHistoryView

# Mock data
mock_data = {
    "zone": "GB",
    "history": [
        {
            "zone": "GB",
            "carbonIntensity": 211,
            "datetime": "2024-10-28T13:00:00.000Z",
            "updatedAt": "2024-10-29T10:46:52.406Z",
            "createdAt": "2024-10-25T13:48:33.600Z",
            "emissionFactorType": "lifecycle",
            "isEstimated": False,
            "estimationMethod": None,
        },
        {
            "zone": "GB",
            "carbonIntensity": 232,
            "datetime": "2024-10-28T14:00:00.000Z",
            "updatedAt": "2024-10-29T11:47:03.535Z",
            "createdAt": "2024-10-25T14:48:02.810Z",
            "emissionFactorType": "lifecycle",
            "isEstimated": False,
            "estimationMethod": None,
        },
    ],
}


@pytest.fixture
def carbon_intensity_view():
    return CarbonIntensityHistoryView()


@patch("views.carbon_intensity_history_view.api_client.get")
def test_request_data_zone(mock_get, carbon_intensity_view):
    """Test data request with zone parameter."""
    mock_get.return_value = mock_data
    result = carbon_intensity_view.request_data(params={"zone": "GB"})
    assert result.instance_api_client_data == mock_data


@patch("views.carbon_intensity_history_view.api_client.get")
def test_sum_carbon_intensity_data(mock_get, carbon_intensity_view):
    """Test summing of carbon intensity."""
    mock_get.return_value = mock_data
    carbon_intensity_view.request_data(params={"zone": "GB"})
    assert (
        carbon_intensity_view.sum_carbon_intensity_data == 443
    )  # Sum of 211 + 232


@patch("views.carbon_intensity_history_view.api_client.get")
def test_create_dataframe(mock_get, carbon_intensity_view):
    """Test creation of pandas DataFrame."""
    mock_get.return_value = mock_data
    carbon_intensity_view.request_data(params={"zone": "GB"})
    df = carbon_intensity_view.create_dataframe
    assert isinstance(df, pd.DataFrame)
    assert (
        df["Total_carbon_intensity"][0] == 443
    )  # Sum of the mock data values


@patch("views.carbon_intensity_history_view.api_client.get")
def test_estimated_data_flag(mock_get, carbon_intensity_view):
    """Test if estimated data is handled correctly."""
    mock_get.return_value = mock_data
    result = carbon_intensity_view.request_data(params={"zone": "GB"})
    assert all(
        item["isEstimated"] is False
        for item in result.instance_api_client_data["history"]
    )


@patch("views.carbon_intensity_history_view.api_client.get")
def test_datetime_format(mock_get, carbon_intensity_view):
    """Test datetime format correctness."""
    mock_get.return_value = mock_data
    result = carbon_intensity_view.request_data(params={"zone": "GB"})
    assert "T" in result.instance_api_client_data["history"][0]["datetime"]


@patch("views.carbon_intensity_history_view.api_client.get")
def test_emission_factor_type(mock_get, carbon_intensity_view):
    """Test if emission factor type is lifecycle for all entries."""
    mock_get.return_value = mock_data
    result = carbon_intensity_view.request_data(params={"zone": "GB"})
    assert all(
        item["emissionFactorType"] == "lifecycle"
        for item in result.instance_api_client_data["history"]
    )


@patch("views.carbon_intensity_history_view.api_client.get")
def test_instance_api_client_data(mock_get, carbon_intensity_view):
    """Test instance API client data assignment."""
    mock_get.return_value = mock_data
    result = carbon_intensity_view.request_data(params={"zone": "GB"})
    assert result.instance_api_client_data == mock_data


@patch("views.carbon_intensity_history_view.api_client.get")
def test_missing_carbon_intensity_key(mock_get, carbon_intensity_view):
    """Test handling missing carbon intensity key."""
    incomplete_data = {"history": [{}]}
    mock_get.return_value = incomplete_data
    carbon_intensity_view.request_data(params={"zone": "GB"})
    assert carbon_intensity_view.sum_carbon_intensity_data == 0


@patch("views.carbon_intensity_history_view.api_client.get")
def test_zero_carbon_intensity_data(mock_get, carbon_intensity_view):
    """Test zero values in carbon intensity data."""
    zero_data = {"history": [{"carbonIntensity": 0}]}
    mock_get.return_value = zero_data
    carbon_intensity_view.request_data(params={"zone": "GB"})
    assert carbon_intensity_view.sum_carbon_intensity_data == 0


@patch("views.carbon_intensity_history_view.api_client.get")
def test_large_dataset_sum_carbon_intensity(mock_get, carbon_intensity_view):
    """Test summing large dataset of carbon intensity values."""
    large_data = {"history": [{"carbonIntensity": 100} for _ in range(1000)]}
    mock_get.return_value = large_data
    carbon_intensity_view.request_data(params={"zone": "GB"})
    assert carbon_intensity_view.sum_carbon_intensity_data == 100000
