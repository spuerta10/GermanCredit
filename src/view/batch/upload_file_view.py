from io import BytesIO

from streamlit import divider, file_uploader

from src.view.base_view import BaseView


class UploadFileView(BaseView):
    # @override
    def render(self) -> BytesIO:
        uploaded_file: BytesIO = file_uploader(label="Choose a CSV file", type="csv")
        divider()
        return uploaded_file
