from io import BytesIO
from typing import Any, ClassVar

from numpy import ndarray
from pandas import DataFrame, read_csv

from src.controller.base_batch_controller import BaseBatchController
from src.controller.base_controller import BaseController
from src.service.base_service import BaseService
from src.service.transformations import remove_outliers


class StreamlitController(BaseController, BaseBatchController):
    """Controller for handling predictions in a Streamlit-based application."""

    FILE_INGESTION_ERROR: str = "Failed to ingest file: the file may be empty or malformed."

    CREDIT_REQUEST_COL: ClassVar[str] = "Credit Request"
    CREDIT_REQUEST_MAPPINGS: ClassVar[dict[int, str]] = {
        0: "Credit Not Approved",
        1: "Credit Approved",
    }
    PLOT_COLUMNS: ClassVar[list[str]] = ["Credit amount", CREDIT_REQUEST_COL]

    def __init__(self, service: BaseService, preprocessing: BaseService):
        """Initializes the Streamlit controller with a service.

        Args:
            service (BaseService): The service responsible for executing predictions.
        """
        super().__init__(service)
        self.preprocessing = preprocessing
        self.plot_data: None | DataFrame = None

    def __ingest_file(self, file: BytesIO) -> DataFrame:
        """Reads a CSV file into a pandas DataFrame.

        Args:
            file (BytesIO): A CSV file-like object containing input data.

        Raises:
            ValueError: If the file cannot be read properly.

        Returns:
            DataFrame: Parsed data from the input file.
        """
        try:
            data: DataFrame = read_csv(file)
        except Exception as err:
            raise ValueError(self.FILE_INGESTION_ERROR) from err
        else:
            return data

    def __get_mapped_predictions(self, data: DataFrame, predictions: ndarray) -> DataFrame:
        """Adds a prediction column to the input DataFrame with human-readable labels.

        Args:
            data (DataFrame): Original data without mapped predictions.
            predictions (ndarray): Raw prediction results.

        Returns:
            DataFrame: Updated DataFrame with mapped prediction labels.
        """
        temp_data: DataFrame = data.copy()
        temp_data[self.CREDIT_REQUEST_COL] = predictions
        temp_data[self.CREDIT_REQUEST_COL] = temp_data[self.CREDIT_REQUEST_COL].map(
            self.CREDIT_REQUEST_MAPPINGS
        )
        return temp_data

    def get_plot_data(self) -> DataFrame:
        """Prepares and filters the data for plotting, removing negative values and outliers.

        Returns:
            DataFrame: Cleaned DataFrame suitable for plotting.
        """
        assert isinstance(self.plot_data, DataFrame)
        plot_data: DataFrame = self.plot_data[self.PLOT_COLUMNS][
            self.plot_data[self.PLOT_COLUMNS[0]] > 0  # filter negative credit amounts
        ]
        plot_data[self.PLOT_COLUMNS[0]] = remove_outliers(plot_data[[self.PLOT_COLUMNS[0]]])
        return plot_data.dropna()  # remove outliers inplaced with NA

    # @override
    def get_file_preview(self, file: BytesIO) -> DataFrame:
        """Returns a preview of the uploaded file for display in the UI.

        Args:
            file (BytesIO): A CSV file-like object containing input data.

        Returns:
            DataFrame: First few rows of the uploaded data.
        """
        file.seek(0)  # reset file pointer
        data: DataFrame = self.__ingest_file(file)
        return data.head(7)

    # @override
    def handle_prediction(self, data: dict[str, Any]) -> int | Any:
        """Processes a single prediction request.

        Args:
            data (dict[str, Any]): The input data for prediction.

        Returns:
            int | Any: The prediction result.
        """
        return self.service.execute(data)

    # @override
    def handle_batch_prediction(
        self,
        file: BytesIO,
    ) -> DataFrame:
        """Processes batch predictions from a CSV file and prepares data for visualization.

        Args:
            file (BytesIO): A CSV file-like object containing multiple prediction inputs.

        Returns:
            DataFrame: DataFrame with predictions appended and formatted.
        """
        file.seek(0)  # reset file pointer
        data: DataFrame = self.__ingest_file(file)
        preprocessed: DataFrame = self.preprocessing.execute(data)
        predictions: ndarray = self.service.execute(preprocessed)

        self.plot_data = self.__get_mapped_predictions(preprocessed, predictions)
        return self.__get_mapped_predictions(data, predictions)

    def get_approval_rate(self, predictions: DataFrame) -> float:
        """Calculates the approval rate from the predictions.

        Args:
            predictions (DataFrame): DataFrame containing prediction results with mapped labels.

        Returns:
            float: Percentage of credit requests that were approved.
        """
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
