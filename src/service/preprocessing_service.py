from typing import ClassVar

from numpy import nan
from pandas import Categorical, DataFrame

from src.service.base_service import BaseService


class PreprocessingService(BaseService):
    REQUIRED_FIELDS_ERROR: ClassVar[str] = "Missing required fields: {}"

    EXPECTED_COLUMNS: ClassVar[list[str]] = [
        "Credit amount",
        "Purpose",
        "Job",
        "Sex",
        "Saving accounts",
        "Housing",
        "Age",
        "Duration",
    ]

    CATEGORICAL_MAPPINGS: ClassVar[dict[str, list | None]] = {
        "Purpose": None,
        "Job": [0, 1, 2, 3],
        "Sex": None,
        "Saving accounts": ["little", "quite rich", "rich"],
        "Housing": None,
    }

    NUMERICAL_MAPPINGS: ClassVar[dict[str, str]] = {
        "Duration": "Int64",  # has to be base 64 so it can be nullable
        "Credit amount": "Int64",
        "Age": "Int64",
    }

    @staticmethod
    def __convert_to_categorical(
        data: DataFrame, categorical_mappings: dict[str, None | list]
    ) -> DataFrame:
        temp_data: DataFrame = data.copy()
        temp_data[list(categorical_mappings.keys())] = temp_data[
            list(categorical_mappings.keys())
        ].astype("category")
        for col, categories in categorical_mappings.items():
            if categories:
                temp_data[col] = Categorical(temp_data[col], categories=categories, ordered=True)
        return temp_data

    @staticmethod
    def __convert_to_numerical(data: DataFrame, numerical_mappings: dict[str, str]) -> DataFrame:
        validation_df: DataFrame = data.copy()
        temp_data: DataFrame = data.copy()
        for col in numerical_mappings:
            validation_df[col] = validation_df[col].astype(
                str
            )  # convert to string temporarily for checking
            mask = ~validation_df[col].str.match(
                r"^-?\d+\.?\d*$", na=True
            )  # detecting weird values inside numerical columns
            temp_data.loc[mask, col] = nan

        temp_data = temp_data.astype(
            {col: num_type for col, num_type in numerical_mappings.items()}
        )
        return temp_data

    # @override
    def execute(self, data: DataFrame) -> DataFrame:
        try:
            data[self.EXPECTED_COLUMNS]
        except KeyError as err:
            missing_fields: list[str] = [
                field for field in self.EXPECTED_COLUMNS if field not in data
            ]
            raise ValueError(self.REQUIRED_FIELDS_ERROR.format(missing_fields)) from err
        else:
            data.drop_duplicates(
                subset=["Unnamed: 0"], inplace=True
            ) if "Unnamed: 0" in data.columns else data.drop_duplicates(inplace=True)
            data = data[self.EXPECTED_COLUMNS]
            data = self.__convert_to_categorical(data, self.CATEGORICAL_MAPPINGS)
            data = self.__convert_to_numerical(data, self.NUMERICAL_MAPPINGS)
            return data
