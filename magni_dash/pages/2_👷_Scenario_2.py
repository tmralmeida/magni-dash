import streamlit as st

from magni_dash.st_components.common import run_configs


run_configs(scenario_id=2)
with st.expander("See description"):
    st.write(
        """
            Scenario 2 features the same room layout as Scenario 1A
            (i.e., without semantics). In addition to the basic goaldriven navigation,
            this scenario introduces people performing
            different tasks. These tasks aim to emulate regular activities
            performed in industrial contexts, such as transporting stacks
            of different objects between various goal locations.
            """
    )
