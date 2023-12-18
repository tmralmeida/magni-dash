
# magni-dash
Dashboard for Magni dataset.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://magni-dash.streamlit.app)

- Web app: <https://magni-dash.streamlit.app>
- Source code: <https://github.com/tmralmeida/magni-dash>


# Install

Install [miniconda](http://docs.conda.io/en/latest/miniconda.html). Then, you can install all packages required by running:

```
conda env create -f ex_environment.yml
```

# Launching dashboard

Set the [path](https://github.com/tmralmeida/magni-dash/blob/main/magni_dash/config/constants.py) to a directory with the following structure:

------------
    ├── Scenario{i}       <- Folder with csv files for scenario i
        ├── file_name_{merged}.csv 
--------



Run:

```
streamlit run Home.py
```