from pandas import DataFrame
from streamlit import dataframe, divider, subheader

from src.view.base_view import BaseView


class FilePreviewView(BaseView):
    def render(self, file: DataFrame) -> None:
        subheader("Here's a preview of your uploaded data")
        dataframe(file)
        divider()
