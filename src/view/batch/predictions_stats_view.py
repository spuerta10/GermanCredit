from matplotlib import pyplot as plt
from pandas import DataFrame
from seaborn import kdeplot
from streamlit import columns, metric, pyplot, subheader

from src.controller.streamlit_controller import StreamlitController
from src.view.base_view import BaseView


class PredictionsStatsView(BaseView):
    PLOT_COLUMNS: list[str] = StreamlitController.PLOT_COLUMNS

    def __plot_credit_distribution_by_prediction(self, plot_data: DataFrame) -> plt:
        """
        Creates a KDE plot showing the distribution of credit amounts
        segmented by prediction class (e.g., approved or denied).

        The Y-axis and left/top/right frame lines are removed for a cleaner appearance.

        Args:
            plot_data (DataFrame): DataFrame containing the prediction results with
                at least two columns:
                - One numeric column for the credit amount.
                - One categorical column for the prediction label.

        Returns:
            matplotlib.pyplot: The configured matplotlib plot object.
        """
        plt.figure(figsize=(10, 6))
        kdeplot(
            data=plot_data,
            x=self.PLOT_COLUMNS[0],
            hue=self.PLOT_COLUMNS[1],
            fill=True,
            common_norm=False,
            alpha=0.5,
            palette=["#EF553B", "#00CC96"],
        )
        plt.title("Distribution of Credit Amounts by Decision")
        plt.xlabel("Credit Amount (€)")
        plt.ylabel("Density")

        plt.gca().axes.get_yaxis().set_visible(False)  # remove Y axis

        for spine in ["top", "right", "left"]:
            plt.gca().spines[spine].set_visible(False)  # remove frame

        return plt

    def render(self, approval_rate: float, rejection_rate: float, plot_data: DataFrame) -> None:
        """
        Renders a credit application statistics summary in Streamlit, including
        approval and rejection rates and a KDE plot of credit amount distributions.

        Args:
            approval_rate (float): Percentage of credit requests that were approved.
            rejection_rate (float): Percentage of credit requests that were denied.
            plot_data (DataFrame): DataFrame containing the data to visualize,
                including columns for credit amount and prediction class.
        """
        subheader("Credit Application Statistics Overview")
        left, right = columns(2)

        with left:
            metric("✅ Approved Requests (%)", f"{approval_rate:.1f}%")

        with right:
            metric("❌ Denied Requests (%)", f"{rejection_rate:.1f}%")

        pyplot(self.__plot_credit_distribution_by_prediction(plot_data))
