from io import BytesIO
from typing import Any, ClassVar

from numpy import ndarray
from pandas import DataFrame, read_csv

from src.controller.base_batch_controller import BaseBatchController
from src.controller.base_controller import BaseController
from src.service.base_service import BaseService


class StreamlitController(BaseController, BaseBatchController):
    """Controller for handling predictions in a Streamlit-based application."""

    FILE_INGESTION_ERROR: str = "Failed to ingest file: the file may be empty or malformed."

    CREDIT_REQUEST_COL: ClassVar[str] = "Credit Request"
    CREDIT_REQUEST_MAPPINGS: ClassVar[dict[int, str]] = {
        0: "Credit Not Approved",
        1: "Credit Approved",
    }

    def __init__(self, service: BaseService, preprocessing: BaseService):
        """Initializes the Streamlit controller with a service.

        Args:
            service (BaseService): The service responsible for executing predictions.
        """
        super().__init__(service)
        self.preprocessing = preprocessing

    def __ingest_file(self, file: BytesIO) -> DataFrame:
        try:
            data: DataFrame = read_csv(file)
        except Exception as err:
            raise ValueError(self.FILE_INGESTION_ERROR) from err
        else:
            return data

    # @override
    def get_file_preview(self, file: BytesIO) -> DataFrame:
        file.seek(0)  # reset file pointer
        data: DataFrame = self.__ingest_file(file)
        return data.head(7)

    # @override
    def handle_prediction(self, data: dict[str, Any]) -> int | Any:
        """Processes a prediction request and prints the input as a DataFrame.

        Args:
            data (dict[str, Any]): The input data for the prediction.

        Returns:
            int | Any: The prediction result from the service.
        """
        return self.service.execute(data)

    # @override
    def handle_batch_prediction(
        self,
        file: BytesIO,
    ) -> DataFrame:
        file.seek(0)  # reset file pointer
        data: DataFrame = self.__ingest_file(file)
        preprocessed: DataFrame = self.preprocessing.execute(data)
        predictions: ndarray = self.service.execute(preprocessed)
        data[self.CREDIT_REQUEST_COL] = predictions
        data[self.CREDIT_REQUEST_COL] = data[self.CREDIT_REQUEST_COL].map(
            self.CREDIT_REQUEST_MAPPINGS
        )
        return data

    def get_approval_rate(self, predictions: DataFrame) -> float:
        approval_rate: float = (
            len(
                predictions[
                    predictions[self.CREDIT_REQUEST_COL]
                    == self.CREDIT_REQUEST_MAPPINGS[1]  # mappings under approved
                ]
            )
            / len(predictions[self.CREDIT_REQUEST_COL])
        ) * 100
        return approval_rate
