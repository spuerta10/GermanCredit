from typing import Any, ClassVar

from streamlit import divider, error, form, form_submit_button, success, title

from src.controller.base_controller import BaseController
from src.view import (
    BaseView,
    CreditRequestView,
    FinancialStatusView,
    PersonalInformationView,
)


class StreamlitApp:
    CREDIT_APPROVED_MESSAGE: ClassVar[str] = """
    ✅ Credit Approved
    Your credit application has been approved 🎉
    We're excited to support your goals. You'll receive the details shortly.
    """

    CREDIT_NOT_APPROVED_MESSAGE: ClassVar[str] = """
    ❌ Credit Not Approved
    Unfortunately, your credit application wasn't approved at this time 😔
    Don't worry — we're here to help you improve your chances in the future.
    Let's work on it together.
    """

    def __init__(self, controller: BaseController) -> None:
        self.__views: list[BaseView] = [
            CreditRequestView(),
            FinancialStatusView(),
            PersonalInformationView(),
        ]
        self.__controller: BaseController = controller

    def run(self) -> None:
        title("Your Credit Request")
        with form("prediction_form"):
            form_data: dict[str, Any] = {}
            for view in self.__views:
                form_data.update(view.render())
                divider()

            submitted: bool = form_submit_button("Predict")
            if submitted:
                prediction: int = self.__controller.handle_prediction(form_data)
                if prediction == 1:
                    success(self.CREDIT_APPROVED_MESSAGE)
                else:
                    error(self.CREDIT_NOT_APPROVED_MESSAGE)
