import streamlit as st

from magni_dash.st_components.common import run_configs


run_configs(scenario_id=3)
with st.expander("See description"):
    st.write(
        """
            Scenario 3 has two variations: 3A, in
            which the teleoperated robot moves as a regular differential
            drive robot, and 3B, where the robot moves in an omnidirectional way.
            In both cases, an operator drives the mobile
            robot using a remote controller.
            """
    )
