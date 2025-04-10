from os.path import abspath, exists
from typing import Any, ClassVar

from imblearn.pipeline import Pipeline as ImbPipeline
from joblib import load
from pandas import DataFrame

from src.service.base_service import BaseService


class PredictionService(BaseService):
    """Service for loading a machine learning model and making predictions.

    This service handles loading a pre-trained model stored on disk and
    executing predictions based on input data.
    """

    MODEL_NOT_FOUND: ClassVar[str] = "Model not found at {}"
    MODEL_NOT_LOADED: ClassVar[str] = "Model has not been loaded"
    EXPECTED_COLUMNS: ClassVar[list[str]] = [
        "Credit amount",
        "Purpose",
        "Job",
        "Sex",
        "Saving accounts",
        "Housing",
        "Age",
        "Duration",
    ]

    def __init__(self, model_path: str):
        """Initializes the PredictionService by loading a model from disk.

        Args:
            model_path (str): The file path to the trained model.

        Raises:
            AssertionError: If the model file does not exist.
        """
        assert exists(abspath(model_path)), self.MODEL_NOT_FOUND.format(model_path)

        self.__model_path: str = abspath(model_path)
        self.__model: ImbPipeline | None = None
        self.__load_model()

    def __load_model(self) -> "PredictionService":
        """Load the model from disk.

        Returns:
            Self for method chaining

        Raises:
            RuntimeError: If model loading fails
        """
        self.__model = load(self.__model_path)
        return self

    # @override
    def execute(self, data: dict[str, Any]) -> int | Any:
        """Execute prediction on input data.

        Args:
            data: Dictionary containing features

        Returns:
            int: Prediction result
        """
        assert self.__model, self.MODEL_NOT_LOADED

        df: DataFrame = DataFrame.from_dict(data, orient="index").T
        df = df[self.EXPECTED_COLUMNS]
        return self.__model.predict(df)
