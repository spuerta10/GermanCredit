from src.app.streamlit_app import StreamlitApp
from src.controller.streamlit_controller import StreamlitController
from src.service.prediction_service import PredictionService
from src.service.transformations import (
    clean_features,  # noqa
    get_features_names,  # noqa
    remove_outliers,  # noqa
)

if __name__ == "__main__":
    prediction_service: PredictionService = PredictionService(
        r"models/credit_classification-logistic_regression-v2.joblib"
    )
    streamlit_controller: StreamlitController = StreamlitController(service=prediction_service)
    app: StreamlitApp = StreamlitApp(controller=streamlit_controller)
    app.run()
