from typing import Union, List
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
        LOGGER.info(f"{delta_cols} created!")  # noqa: W1203
        return out_df

    @staticmethod
    def get_displacement(input_df: pd.DataFrame):
        out_df = input_df.copy()
        out_df[f"{input_df.name}_displacement"] = np.sqrt(
            np.square(out_df).sum(axis=1)
        )  # in mm
        return out_df

    @staticmethod
    def get_speed(
        input_df: pd.DataFrame,
        time_col_name: str,
        element_name: Union[str, List[str]],
        out_col_name: str = "speed",
    ) -> pd.DataFrame:
        element_name = [element_name] if isinstance(element_name, str) else element_name
        out_df = input_df.copy()

        if time_col_name not in input_df.columns:
            raise ValueError(f"{time_col_name} not in df's columns")

        delta_df = SpatioTemporalFeatures.get_delta_columns(out_df)
        speed_dfs = []
        for element in element_name:
            element_pat = (
                r"DARKO_Robot - (\d) "
                if element == "Darko_Robot" or element == "DARKO"
                else rf"{element} - (\d).*"
            )
            elements_disp = delta_df.groupby(
                delta_df.columns.str.extract(element_pat, expand=False),
                axis=1,
            ).apply(SpatioTemporalFeatures.get_displacement)
            elements_disp.columns = elements_disp.columns.droplevel(0)
            elements_disp = elements_disp.join(
                delta_df.loc[:, [f"{time_col_name}_delta"]]
            )

            elements_disp = elements_disp.rename_axis(None, axis=1)

            disp_cols = elements_disp.columns[
                elements_disp.columns.str.endswith("displacement")
            ]
            n_markers = len(disp_cols)
            speed_cols = [
                f"{element} - {i} {out_col_name} (m/s)" for i in range(1, n_markers + 1)
            ]
            elements_disp.loc[:, speed_cols] = (
                elements_disp[disp_cols]
                .div(elements_disp["Time_delta"].values, axis=0)
                .values
            )
            LOGGER.info(f"{speed_cols} created successfully!")  # noqa: W1203
            speed_dfs.append(elements_disp)
        speed_df = pd.concat(speed_dfs, axis=1, ignore_index=False)

        return speed_df
