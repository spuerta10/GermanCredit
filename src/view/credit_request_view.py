from typing import ClassVar

from streamlit import columns, number_input, selectbox

from src.view.base_view import BaseView


class CreditRequestView(BaseView):
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
    DURATION_MAX: ClassVar[int] = 12

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
            duration: int = number_input(label="Duration", min_value=4, max_value=72)

        return {
            "Credit amount": credit_amount,
            "Purpose": purpose.lower(),
            "Duration": duration,
        }
