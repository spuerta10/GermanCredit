from collections.abc import Callable
from typing import Any

from numpy import nan, ndarray
from pandas import DataFrame


def get_features_names(_: Any, feature_names: ndarray) -> ndarray:
    """
    Returns the provided feature names.
    Args:
        _ (Any): Placeholder argument, not used.
        feature_names (ndarray): Array of feature names.
    Returns:
        ndarray: The input array of feature names.
    """
    return feature_names


def clean_features(
    input_data: DataFrame,
    values: dict[str, list],
    expected: bool = True,
) -> DataFrame:
    assert isinstance(input_data, DataFrame)
    assert isinstance(values, dict)

    temp_df: DataFrame = input_data.copy()
    categories_to_review: list[str] = list(set(temp_df.columns).intersection(set(values.keys())))
    if len(categories_to_review) == 0:
        return input_data

    temp_df[categories_to_review] = (
        temp_df[categories_to_review].apply(lambda x: x.where(x.isin(values[x.name])))
        if expected
        else temp_df[categories_to_review].apply(lambda x: x.where(~x.isin(values[x.name])))
    )
    return temp_df


def remove_outliers(input_data: DataFrame, threshold: float = 1.5) -> DataFrame:
    """
    Replace outliers from numeric columns given a certain treshold with NAN.
    Args:
        threshold (float, optional): Treshold for removing minor (1.5) or extreme outliers (3.0).
        Defaults to 1.5.
    """
    MIN_OUTLIER_THRESHOLD: float = 1.5
    MAX_OUTLIER_THRESHOLD: float = 3.0

    assert isinstance(input_data, DataFrame)
    assert isinstance(threshold, float | int)
    assert MIN_OUTLIER_THRESHOLD <= threshold <= MAX_OUTLIER_THRESHOLD

    temp_df: DataFrame = input_data.copy()

    Q1, Q3 = temp_df.quantile(0.25), temp_df.quantile(0.75)
    IQR: float = Q3 - Q1
    mask: Callable = ~(
        ((Q1 - threshold * IQR) <= temp_df) & ((Q3 + threshold * IQR) >= temp_df)
    ).all(axis=1)
    temp_df.loc[mask] = nan
    return temp_df
