from abc import ABC, abstractmethod
from io import BytesIO

from pandas import DataFrame


class BaseBatchController(ABC):
    @abstractmethod
    def get_file_preview(self, file: BytesIO) -> DataFrame: ...

    @abstractmethod
    def handle_batch_prediction(self, file: BytesIO) -> DataFrame: ...
