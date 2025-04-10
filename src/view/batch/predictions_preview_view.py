from pandas import DataFrame
from streamlit import dataframe, divider, subheader, success

from src.view.base_view import BaseView


class PredictionsPreviewView(BaseView):
    def render(self, predictions: DataFrame) -> None:
        success("✅ Credit requests processed!")
        subheader("Here's a quick look at some predicted credit requests")
        dataframe(predictions)
        divider()
