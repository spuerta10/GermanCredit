from abc import ABC, abstractmethod
from typing import Any

from src.service.base_service import BaseService


class BaseController(ABC):
    """Abstract base class for controllers.

    This class defines the contract for controllers that handle predictions.
    """

    def __init__(self, service: BaseService):
        """Initializes the controller with a service.

        Args:
            service (BaseService): The service responsible for processing data.
        """
        self.service: BaseService = service

    @abstractmethod
    def handle_prediction(self, data: Any) -> Any:
        """Processes a prediction request.

        This method must be implemented by subclasses to handle prediction logic.

        Args:
            data (Any): Input data required for prediction.

        Returns:
            Any: The prediction result.
        """
        ...
