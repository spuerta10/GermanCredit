from typing import ClassVar

from streamlit import columns, number_input, radio, selectbox

from src.view.form.base_form_view import BaseFormView


class PersonalInformationView(BaseFormView):
    MIN_APPLICANT_AGE: ClassVar[int] = 19
    MAX_APPLICANT_AGE: ClassVar[int] = 75

    JOBS: ClassVar[dict[str, int]] = {
        "Unskilled and non-resident": 0,
        "Unskilled and resident": 1,
        "Skilled": 2,
        "Highly skilled": 3,
    }

    # @override
    def render(self) -> dict[str, str | int]:
        col1, col2 = columns(2)
        with col1:
            age: int = number_input(
                "Age",
                min_value=self.MIN_APPLICANT_AGE,
                max_value=self.MAX_APPLICANT_AGE,
            )

        with col2:
            sex: str = radio(
                label="Sex",
                options=["male", "female"],
                horizontal=False,
            )

        job: str = selectbox(label="Job", options=self.JOBS)
        job_id: int = self.JOBS[job]

        return {"Age": age, "Sex": sex, "Job": job_id}
