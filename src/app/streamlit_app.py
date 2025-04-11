from io import BytesIO
from time import sleep
from typing import Any, ClassVar

from pandas import DataFrame
from streamlit import (
    button,
    divider,
    error,
    form,
    form_submit_button,
    spinner,
    success,
    tabs,
    title,
)

from src.controller.base_batch_controller import BaseBatchController
from src.controller.base_controller import BaseController
from src.controller.streamlit_controller import StreamlitController
from src.view import (
    BaseView,
    CreditRequestView,
    DonwloadPredictionsView,
    FilePreviewView,
    FinancialStatusView,
    PersonalInformationView,
    PredictionsPreviewView,
    PredictionsStatsView,
    UploadFileView,
)


class StreamlitApp:
    CREDIT_APPROVED_MESSAGE: ClassVar[str] = """
    ✅ Credit Approved
    \nYour credit application has been approved 🎉
    \nWe're excited to support your goals. You'll receive the details shortly.
    """

    CREDIT_NOT_APPROVED_MESSAGE: ClassVar[str] = """
    ❌ Credit Not Approved
    \nUnfortunately, your credit application wasn't approved at this time 😔
    \nDon't worry — we're here to help you improve your chances in the future.
    \nLet's work on it together.
    """

    def __init__(self, controller: StreamlitController) -> None:
        assert isinstance(controller, BaseController) and isinstance(
            controller, BaseBatchController
        )  # controller must have batch and base (form) capabilities

        self.__views: dict[str, list[BaseView]] = {
            "form": [
                CreditRequestView(),
                FinancialStatusView(),
                PersonalInformationView(),
            ],
            "batch": [
                UploadFileView(),
                FilePreviewView(),
                PredictionsPreviewView(),
                PredictionsStatsView(),
                DonwloadPredictionsView(),
            ],
        }
        self.__controller: StreamlitController = controller

    def run(self) -> None:
        title("Your Credit Request")

        tab1, tab2 = tabs(["Credit Application", "Bulk Credit Applications"])

        with tab1, form("prediction_form"):
            form_data: dict[str, Any] = {}
            for view in self.__views["form"]:
                form_data.update(view.render())
                divider()

            submitted: bool = form_submit_button("Predict")
            if submitted:
                prediction: int = self.__controller.handle_prediction(form_data)
                if prediction == 1:
                    success(self.CREDIT_APPROVED_MESSAGE)
                else:
                    error(self.CREDIT_NOT_APPROVED_MESSAGE)

        with tab2:
            upload_view, preview_view, predictions_view, stats_view, download_view = self.__views[
                "batch"
            ]
            uploaded_file: BytesIO = upload_view.render()
            if uploaded_file:
                try:
                    preview_df: DataFrame = self.__controller.get_file_preview(uploaded_file)
                except Exception as e:
                    error(e)
                preview_view.render(preview_df)
                if button("Predict Credit Approval"):
                    with spinner("Processing data and making predictions..."):
                        try:
                            predictions: DataFrame = self.__controller.handle_batch_prediction(
                                uploaded_file
                            )
                        except Exception as e:
                            error(e)
                        else:
                            sleep(3)
                            predictions_view.render(predictions.sample(7, ignore_index=True))
                            approval_rate: float = self.__controller.get_approval_rate(predictions)
                            stats_view.render(
                                approval_rate,
                                100 - approval_rate,
                                self.__controller.get_plot_data(),
                            )
                            download_view.render(predictions.to_csv(index=False))
