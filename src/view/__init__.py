from src.view.base_view import BaseView
from src.view.batch.download_predictions_view import DonwloadPredictionsView
from src.view.batch.file_preview_view import FilePreviewView
from src.view.batch.predictions_preview_view import PredictionsPreviewView
from src.view.batch.predictions_stats_view import PredictionsStatsView
from src.view.batch.upload_file_view import UploadFileView
from src.view.form.credit_request_view import CreditRequestView
from src.view.form.financial_status_view import FinancialStatusView
from src.view.form.personal_information_view import PersonalInformationView

__all__ = [
    "BaseView",
    "CreditRequestView",
    "DonwloadPredictionsView",
    "FilePreviewView",
    "FinancialStatusView",
    "PersonalInformationView",
    "PredictionsPreviewView",
    "PredictionsStatsView",
    "UploadFileView",
]
