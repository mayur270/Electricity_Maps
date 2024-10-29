"""API client for ElectricityMaps."""

from dataclasses import dataclass, field
from typing import Any

import requests
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    RequestException,
)

from config import config
from log import logger


@dataclass(kw_only=True)
class APIClient:
    """Class for HTTP Methods.

    :param default_headers: This is set in config file.
            Includes authorization, content-type and accept.
    """

    default_headers: dict = field(default_factory=lambda: config.API_HEADERS)

    def get(
            self,
            url: str,
            query_params: dict = None,
            additional_headers: dict = None,
    ) -> dict[str, Any]:
        """GET HTTP method.

        :param url: url to get data from.
        :param query_params: query parameters based on zone or coordinates.
        :param additional_headers: For any additional rules/ specificity.

        :returns: get api response.
        """
        query_parameters = {**(query_params or {})}
        get_headers = {**self.default_headers, **(additional_headers or {})}

        try:
            with requests.get(
                url=url,
                headers=get_headers,
                params=query_parameters,
            ) as response:
                return response.json()
        except HTTPError as http_error:
            msg = f'HTTP Error: {http_error}'
            logger.error(msg)
            raise HTTPError(msg)
        except ConnectionError as conn_timeout_err:
            msg = f'Connection Error: {conn_timeout_err}'
            logger.error(msg)
            raise ConnectionError(msg)
        except RequestException as request_exp:
            msg = f'Error caused due to: {request_exp}'
            logger.error(msg)
            raise RequestException(msg)


api_client = APIClient()
