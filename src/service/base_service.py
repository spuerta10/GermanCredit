from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """Abstract base class for services that process data.

    This class defines a standard interface for executing services
    with a given input data dictionary.
    """

    @abstractmethod
    def execute(self, data: dict[Any, Any]) -> Any:
        """Executes the service with the provided data.

        Args:
            data (Dict[Any, Any]): A dictionary containing the input data
                required for execution.

        Returns:
            Any: The result of the service execution.
        """
        ...
