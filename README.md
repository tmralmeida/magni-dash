# magni-dash
Dashboard for Magni dataset.


# Launch dashboard

Install [miniconda](http://docs.conda.io/en/latest/miniconda.html). Then, you can install all packages required by running:

```
conda env create -f ex_environment.yml
```

Set the [path](https://github.com/tmralmeida/magni-dash/blob/main/magni_dash/config/constants.py) to a directory with the following structure:

------------
    ├── Scenario{i}       <- Folder with csv files for scenario i
        ├── file_name_{merged}.csv 
--------


# Launching dashboard

Run:

```
streamlit run magni_dash/Welcome.py
```