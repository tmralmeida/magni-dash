import streamlit as st
import pandas as pd
import logging
from typing import List, Union, Optional

from magni_dash.data_preprocessing.spatio_temporal_features import (
    SpatioTemporalFeatures,
)
from magni_dash.utils.common import get_mapping_cols
from magni_dash.config.constants import TRAJECTORY_DATA_TYPE

LOGGER = logging.getLogger(__name__)


@st.cache_data
def load_df(
    df_path: str, sep: str, header: int, index_col: str, height_suffix: str = "Z"
) -> pd.DataFrame:
    """Load a csv pandas dataframe.

    Parameters
    ----------
    df_path
        Absolute path to the file.
    sep
        Separation marker.
    header
        Header rows size.
    index_col
        Column name for the index.

    Returns
    -------
        Pandas DtaFrame object.
    """
    raw_df = pd.read_csv(
        df_path,
        sep=sep,
        header=header,
        index_col=index_col,
    )
    if TRAJECTORY_DATA_TYPE == "2D":
        raw_df = raw_df[raw_df.columns[~raw_df.columns.str.endswith(height_suffix)]]
    raw_df = raw_df.dropna(axis=1, how="all")
    raw_df = raw_df.interpolate()
    raw_df[
        raw_df.columns[
            (raw_df.columns.str.endswith("X"))
            | ((raw_df.columns.str.endswith("Y")))
            | ((raw_df.columns.str.endswith("Z")))
        ]
    ] /= 1000
    raw_df = raw_df.loc[
        :,
        (~raw_df.columns.str.contains("^Unnamed"))
        & (~raw_df.columns.str.contains("Type")),
    ]
    return raw_df


@st.cache_data
def extract_features(
    out_df: pd.DataFrame,
    helmets_labels: Union[str, List[str]],
    darko_label: Optional[str],
) -> pd.DataFrame:
    """Extract features to be used in the profiles section such as speed

    Parameters
    ----------
    input_df
        raw pandas DataFrame
    helmet_number
        number of helmet

    Returns
    -------
        pandas DataFrame with the respective features computed
    """
    helmets_labels = (
        [helmets_labels] if isinstance(helmets_labels, str) else helmets_labels
    )
    elements_labels = helmets_labels + [darko_label] if darko_label else helmets_labels

    out_df = SpatioTemporalFeatures.get_speed(
        out_df,
        time_col_name="Time",
        element_name=elements_labels,
    )

    out_df = out_df.reset_index()
    return out_df


@st.cache_resource
def transform_df2plotly(
    input_df: pd.DataFrame, element_id: str, markers_pattern_re: str, sep: str
) -> pd.DataFrame:
    """Transform a dataframe into the plotly format
    |   Frame    |   X (m)  |   Y (m)  |   eid   |   mid   |

    being `eid` the element identifier (e.g. Helmet, DARKO, etc), and `mid` the marker identifier

    Parameters
    ----------
    input_df
        input pandas DataFrame
    element_id
        see eid explanation above
    markers_pattern_re
        regex to groupby element id and markers
    sep
        separation used in col name form element id and marker id

    Returns
    -------
        Transformed pandas DataFrame
    """
    elements_grouped = input_df.groupby(
        input_df.columns.str.extract(markers_pattern_re, expand=False),
        axis=1,
    )
    groups = []
    for group_name, group in elements_grouped:
        _mapping_cols = get_mapping_cols(element_id, group_name, sep)
        group = group.rename(_mapping_cols, axis=1)
        eid = (
            element_id + "_" + group_name.split(" - ")[0]
            if element_id == "Helmet"
            else element_id
        )
        mid = group_name.split(" - ")[1] if element_id == "Helmet" else group_name
        group["eid"] = eid
        group["mid"] = mid
        groups.append(group)
    out_df = pd.concat(groups, axis=0)
    return out_df


@st.cache_resource
def get_best_markers(elements_cat_df: pd.DataFrame, ret_filtered_df: bool):
    """Get markers with lowest amount of NaN values"""

    instances = elements_cat_df.eid.unique()
    nan_counter_by_marker = {}
    for instance_id in instances:
        nan_counter_by_marker[instance_id] = {}
        markers = elements_cat_df[elements_cat_df.eid == instance_id].mid.unique()
        for marker_id in markers:
            n_nans = (
                elements_cat_df[
                    (elements_cat_df.eid == instance_id)
                    & (elements_cat_df.mid == marker_id)
                ]["X (m)"]
                .isna()
                .sum()
            )
            nan_counter_by_marker[instance_id][marker_id] = n_nans
    LOGGER.info(nan_counter_by_marker)
    if not ret_filtered_df:
        return nan_counter_by_marker
    elements_filtered_by_best_marker = []
    for instance_id, nans_counter in nan_counter_by_marker.items():
        best_marker_id = min(
            nans_counter,
            key=nans_counter.get,
        )
        elements_filtered_by_best_marker.append(
            elements_cat_df[
                (elements_cat_df.eid == instance_id)
                & (elements_cat_df.mid == best_marker_id)
            ]
        )
    out_df = pd.concat(elements_filtered_by_best_marker, axis=0)
    out_df = out_df.sort_index().reset_index()
    return out_df
