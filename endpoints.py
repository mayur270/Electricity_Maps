"""Electricity Maps API endpoints."""

from config import config


class APIEndpoints:
    """API endpoints in use."""

    CARBON_INTENSITY_API = f'{config.BASE_URL}/v3/carbon-intensity/history'
