import os
import streamlit as st

from magni_dash.st_components.common import run_configs
from magni_dash.st_components.cache import (
    load_df,
    preprocess_df,
    transform_df2plotly,
    get_best_markers,
    extract_features,
    filter_best_markers,
)
from magni_dash.utils.common import GroupsInfo
from magni_dash.visualization.multi_trajectory import get_multi_element_trajectories
from magni_dash.config.constants import TRAJECTORY_SAMPLES_PATH


SCENARIO1_PATH = os.path.join(TRAJECTORY_SAMPLES_PATH, "Scenario1")

run_configs(scenario_id=1)
with st.expander("See description"):
    st.write(
        """ Scenario 1 is designed as a baseline to capture “regular”
            social behavior of walking people in a static environment. It
            has two variations: 1A which only includes static obstacles,
            and 1B which additionally includes floor markings and stop
            signs in a one-way corridor.
            """
    )


files = os.listdir(SCENARIO1_PATH)
files_target = list(filter(lambda x: x.endswith("pp.tsv"), files))

input_file = st.sidebar.selectbox(
    label="File", options=files_target, key="input_file", label_visibility="visible"
)

if st.session_state.input_file:
    df_path = os.path.join(SCENARIO1_PATH, input_file)
    raw_df = load_df(
        df_path=df_path,
        header=11,
        sep="\t",
        index_col="Frame",
    )
    best_markers_counter = get_best_markers(input_df=raw_df)
    preprocessed_df = preprocess_df(raw_df.copy())
    helmets = preprocessed_df.columns[
        preprocessed_df.columns.str.startswith("Helmet")
    ].tolist()
    helmets_labels = set(map(lambda x: x.split(" - ")[0], helmets))
    features_df = extract_features(
        preprocessed_df.copy(), magents_labels=list(helmets_labels), darko_label=None
    )
    features_cat = preprocessed_df.join(features_df)
    features_filtered = features_cat[
        features_cat.columns[
            (features_cat.columns.str.endswith("X"))
            | (features_cat.columns.str.endswith("Y"))
            | (features_cat.columns.str.endswith("speed (m/s)"))
        ]
    ]

    helmets_info = GroupsInfo(
        element_id="Helmet", markers_pattern_re=r"Helmet_(\d+ - \d).*", label_sep="_"
    )
    df_plot = transform_df2plotly(
        input_df=features_filtered.copy(), groups_info=helmets_info
    )
    best_makers_df = filter_best_markers(
        elements_cat_df=df_plot.copy(), nan_counter_by_marker=best_markers_counter
    )
    figs = get_multi_element_trajectories(best_makers_df)
    for fig in figs:
        st.plotly_chart(fig, use_container_width=True)
