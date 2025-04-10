from typing import Any

from src.controller.base_controller import BaseController
from src.service.base_service import BaseService


class StreamlitController(BaseController):
    """Controller for handling predictions in a Streamlit-based application."""

    def __init__(self, service: BaseService):
        """Initializes the Streamlit controller with a service.

        Args:
            service (BaseService): The service responsible for executing predictions.
        """
        super().__init__(service)

    # @override
    def handle_prediction(self, data: dict[str, Any]) -> int | Any:
        """Processes a prediction request and prints the input as a DataFrame.

        Args:
            data (dict[str, Any]): The input data for the prediction.

        Returns:
            int | Any: The prediction result from the service.
        """
        return self.service.execute(data)
