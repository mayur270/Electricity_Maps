from abc import ABC, abstractmethod
from typing import Any, Dict


class APIData(ABC):
    """
    Abstract base class for data requesting and validation data.
    """

    @abstractmethod
    def request_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Requesting data.

        Args:
            data: A dictionary containing the data to process.

        Returns:
            Dict[str, Any]: The processed data.
        """
        pass

    @abstractmethod
    def validate_data(self) -> Dict[str, Any]:
        """
        Validate data.

        Returns:
            Dict[str, Any]: return validated data.
        """
        pass
