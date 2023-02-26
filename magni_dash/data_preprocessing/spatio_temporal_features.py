from typing import Optional
import logging
import pandas as pd
import numpy as np


LOGGER = logging.getLogger(__name__)


class SpatioTemporalFeatures:
    @staticmethod
    def get_delta_columns(input_df: pd.DataFrame):
        initial_columns = set(input_df.columns)
        out_df = input_df.diff().add_suffix("_delta").fillna(0).sort_index(axis=1)

        delta_cols = set(out_df.columns) - initial_columns
        print(f"{delta_cols} created!")
        return out_df

    @staticmethod
    def get_displacement(input_df: pd.DataFrame, element_name: str):
        out_df = input_df.copy()
        out_df[f"{element_name}_{input_df.name}_displacement"] = (
            np.sqrt(np.square(out_df).sum(axis=1)) / 1000
        )  # in mm
        return out_df

    @staticmethod
    def get_speed(
        input_df: pd.DataFrame,
        time_col_name: str,
        out_col_name: Optional[str] = "speed",
    ):
        out_df = input_df.copy()

        if time_col_name not in input_df.columns:
            raise ValueError(f"{time_col_name} not in df's columns")

        delta_df = SpatioTemporalFeatures.get_delta_columns(out_df)
        helmet_pat, darko_pat = r"Helmet_(\d+ - \d).*", r"DARKO_Robot.*"
        helmets_disp = delta_df.groupby(
            delta_df.columns.str.extract(helmet_pat, expand=False),
            axis=1,
        ).apply(SpatioTemporalFeatures.get_displacement, "Helmet")
        helmets_disp.columns = helmets_disp.columns.droplevel(0)
        helmets_disp = helmets_disp.rename_axis(None, axis=1)
        return helmets_disp
