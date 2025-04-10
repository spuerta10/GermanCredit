from streamlit import columns, divider, metric, subheader

from src.view.base_view import BaseView


class PredictionsStatsView(BaseView):
    def render(self, approval_rate: float, rejection_rate: float) -> None:
        subheader("Credit Application Statistics Overview")
        left, right = columns(2)

        with left:
            metric("✅ Approved Requests (%)", f"{approval_rate:.1f}%")

        with right:
            metric("❌ Denied Requests (%)", f"{rejection_rate:.1f}%")

        divider()
