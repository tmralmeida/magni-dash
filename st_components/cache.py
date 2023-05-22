import streamlit as st
import pandas as pd
import logging
from typing import List, Union, Optional, Dict

from data_preprocessing.spatio_temporal_features import (
    SpatioTemporalFeatures,
)
from utils.common import (
    get_mapping_cols,
    get_mapping_cols_tobii,
    get_mapping_cols_centroids,
    GroupsInfo,
)
from config.constants import TRAJECTORY_DATA_TYPE

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
    raw_df = raw_df.loc[
        :,
        (~raw_df.columns.str.contains("^Unnamed"))
        & (~raw_df.columns.str.contains("Type")),
    ]
    return raw_df


@st.cache_data
def preprocess_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    """interpolation and divide by 1000 to get measurements in meters"""
    preprocessed_df = raw_df.copy()
    trajectories_condition = preprocessed_df.columns[
        (preprocessed_df.columns.str.endswith(" X"))
        | ((preprocessed_df.columns.str.endswith(" Y")))
        | ((preprocessed_df.columns.str.endswith(" Z")))
    ]
    preprocessed_df[trajectories_condition] = preprocessed_df[
        trajectories_condition
    ].interpolate()
    preprocessed_df[trajectories_condition] /= 1000
    return preprocessed_df


@st.cache_data
def extract_features(
    out_df: pd.DataFrame,
    magents_labels: Union[str, List[str]],
    darko_label: Optional[str],
) -> pd.DataFrame:
    """Extract features to be used in the profiles section such as speed

    Parameters
    ----------
    input_df
        raw pandas DataFrame
    magents_labels
        moving agents labels
    darko_label
        darko robot label

    Returns
    -------
        pandas DataFrame with the respective features computed
    """
    magents_labels = (
        [magents_labels] if isinstance(magents_labels, str) else magents_labels
    )
    elements_labels = magents_labels + [darko_label] if darko_label else magents_labels

    out_df = SpatioTemporalFeatures.get_speed(
        out_df,
        time_col_name="Time",
        element_name=elements_labels,
    )

    out_df = out_df.reset_index()
    return out_df


@st.cache_resource
def transform_df2plotly(
    input_df: pd.DataFrame, groups_info
) -> pd.DataFrame:
    """Transform a dataframe into the plotly best suited format
    |   Frame    |   axis i (um)  |   axis i+1 (um)  |   axis i+2(um)   |   eid   | optional [mid]

    being `eid` the element identifier (e.g. Helmet, DARKO, etc), and `mid` the marker identifier
    and axis can be X, Y, Z (being um meters)

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
    groups_info = [groups_info] if isinstance(groups_info, GroupsInfo) else groups_info
    groups = []
    for group_info in groups_info:
        element_id = group_info.element_id
        elements_grouped = input_df.groupby(
            input_df.columns.str.extract(group_info.markers_pattern_re, expand=False),
            axis=1,
        )
        for group_name, group in elements_grouped:
            if element_id == "Helmet" and len(group_name.split("-")) == 1:
                tobii = len(group_name.split(" ")) == 2
                # eyt or centroids
                _mapping_cols = (
                    get_mapping_cols_tobii(
                        element_id,
                        group_name,
                        group_info.label_sep,
                    )
                    if tobii
                    else get_mapping_cols_centroids(
                        element_id, group_name, group_info.label_sep
                    )
                )
                group = group.rename(_mapping_cols, axis=1)
                eid = element_id + "_" + group_name.split(" ")[0]
            else:
                _mapping_cols = get_mapping_cols(
                    element_id, group_name, group_info.label_sep
                )
                group = group.rename(_mapping_cols, axis=1)
                eid = (
                    element_id + "_" + group_name.split(" - ")[0]
                    if element_id == "Helmet"
                    else element_id
                )
                mid = group_name.split(" - ")[1] if element_id == "Helmet" else group_name
                group["mid"] = mid
            group["eid"] = eid
            groups.append(group)
    out_df = pd.concat(groups, axis=0)
    return out_df


@st.cache_resource
def get_best_markers(input_df: pd.DataFrame):
    """Get markers with lowest amount of NaN values"""
    x_coordinate = input_df[input_df.columns[input_df.columns.str.endswith("X")]]
    x_cols = x_coordinate.columns

    instances = set(x_coordinate.columns.str.split(" - ").str[0])
    instances = list(filter(lambda x: len(x.split(" ")) == 1, instances))
    nan_counter_by_marker = {}
    for instance_id in instances:
        nan_counter_by_marker[instance_id] = {}
        markers = (
            x_coordinate[x_cols[x_cols.str.startswith(f"{instance_id} -")]]
            .columns.str.split(regex=r" (/d) ")
            .str[2]
        )
        for marker_id in markers:
            n_nans = x_coordinate[f"{instance_id} - {marker_id} X"].isna().sum()
            nan_counter_by_marker[instance_id][marker_id] = n_nans
    LOGGER.info(nan_counter_by_marker)
    return nan_counter_by_marker


@st.cache_resource
def filter_best_markers(elements_cat_df: pd.DataFrame, nan_counter_by_marker: Dict):
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
