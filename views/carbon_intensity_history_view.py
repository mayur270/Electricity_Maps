"""carbon intensity view."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict

import pandas as pd

from endpoints import APIEndpoints
from models import CarbonIntensityHistory, CoordinatesParam, ZoneParam
from utils import api_client, data_validation, output_filepath, write_to_csv
from views import APIData


@dataclass
class CarbonIntensityHistoryView(APIData):
    """Calculate total carbon intensity.

    :param directory: For changing directory location
    :param: filename: For changing filename
    :param: _api_client_data: internal use only; sharing of API data
    """

    directory: str = None
    filename: str = 'carbon_intensity'
    _cls_api_client_data: dict = field(default=None, init=False)

    def request_data(
        self,
        params: dict = CoordinatesParam | ZoneParam,
    ) -> Dict[str, Any]:
        """Get and validate carbon intensity history.

        :param params: Include Zone({'zone': 'GB'}) or
                       Coordinates ({'lon': '-0.1278', 'lat':'51.5074'}).
        """
        self._instance_api_client_data = api_client.get(
            url=APIEndpoints.CARBON_INTENSITY_API,
            query_params=params,
        )
        return self

    @property
    def validate_data(self) -> Dict[str, Any]:
        validated_data = data_validation(
            schema_model=CarbonIntensityHistory,
            api_data=self._instance_api_client_data,
        )
        self._instance_api_client_data = validated_data
        return self._instance_api_client_data

    @property
    def sum_carbon_intensity_data(self) -> float:
        """Calculate 24h carbon intensity."""
        return sum(
            data.get('carbonIntensity', 0)
            for data in self._instance_api_client_data['history']
        )

    @property
    def create_dataframe(self) -> pd.DataFrame:
        """Pandas DataFrame for carbon intensity"""
        return pd.DataFrame(
            {
                'Total_carbon_intensity': [
                    float(self.sum_carbon_intensity_data),
                ],
            },
        )

    @property
    def file_path(self) -> Callable:
        """Directory location and filename."""
        return output_filepath(
            filename=self.filename, directory=self.directory
        )

    @property
    def write_to_csv(self) -> Callable:
        """Write data to CSV File."""
        return write_to_csv(
            df=self.create_dataframe,
            filepath=self.file_path,
            index=False,
        )


def carbon_intensity_history_main(zone: str = 'GB') -> None:
    """Entrypoint to carbon intensity data."""
    carbon_intensity_history = CarbonIntensityHistoryView()
    get_carbon_intensity_data = carbon_intensity_history.request_data(
        params={'zone': zone},
    ).write_to_csv
    return get_carbon_intensity_data
