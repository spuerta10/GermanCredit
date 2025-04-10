from streamlit import download_button

from src.view.base_view import BaseView


class DonwloadPredictionsView(BaseView):
    def render(self, file: str) -> None:
        download_button(
            label="Download results as CSV",
            data=file,
            file_name="credit_requests_predictions.csv",
            mime="text/csv",
        )
