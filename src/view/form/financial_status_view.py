from typing import ClassVar

from streamlit import columns, selectbox

from src.view.form.base_form_view import BaseFormView


class FinancialStatusView(BaseFormView):
    SAVING_ACCOUNTS: ClassVar[list[str]] = ["Little", "Moderate", "Quite rich", "Rich"]
    HOUSING: ClassVar[list[str]] = ["Own", "Rent", "Free"]

    # @override
    def render(self) -> dict[str, str]:
        col1, col2 = columns(2)
        with col1:
            saving_accounts: str = selectbox(label="Saving accounts", options=self.SAVING_ACCOUNTS)

        with col2:
            housing: str = selectbox(label="Housing", options=self.HOUSING)

        return {"Saving accounts": saving_accounts.lower(), "Housing": housing.lower()}
