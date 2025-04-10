from abc import ABC, abstractmethod
from typing import Any

from pandas import DataFrame


class BaseService(ABC):
    """Abstract base class for services that process data.

    This class defines a standard interface for executing services
    with a given input data dictionary.
    """

    @abstractmethod
    def execute(self, data: dict[Any, Any] | DataFrame) -> Any:
        """Executes the service with the provided data.

        Args:
            data (Dict[Any, Any], DataFrame): A dictionary or DataFrame containing the input data
                required for execution.

        Returns:
            Any: The result of the service execution.
        """
        ...
