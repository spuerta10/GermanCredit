from typing import ClassVar

from streamlit import columns, number_input, selectbox

from src.view.form.base_form_view import BaseFormView


class CreditRequestView(BaseFormView):
    CREDIT_AMOUNT_MIN: ClassVar[float] = 250.0
    CREDIT_AMOUNT_MAX: ClassVar[float] = 987657.0

    PURPOSE_OPTIONS: ClassVar[list[str]] = [
        "Car",
        "Education",
        "Radio/TV",
        "Furniture/equipment",
        "Repairs",
        "Business",
        "Domestic appliances",
        "Vacation/others",
    ]

    DURATION_MIN: ClassVar[int] = 4  # in months
    DURATION_MAX: ClassVar[int] = 72

    def render(self) -> dict[str, str | int | float]:
        col1, col2 = columns(2)

        credit_amount: float = number_input(
            label="Credit amount",
            min_value=self.CREDIT_AMOUNT_MIN,
            max_value=self.CREDIT_AMOUNT_MAX,
        )

        with col1:
            purpose: str = selectbox(label="Purpose", options=self.PURPOSE_OPTIONS)

        with col2:
            duration: int = number_input(
                label="Duration",
                min_value=self.DURATION_MIN,
                max_value=self.DURATION_MAX,
                help="Loan duration in months",
            )

        return {
            "Credit amount": credit_amount,
            "Purpose": purpose.lower(),
            "Duration": duration,
        }
