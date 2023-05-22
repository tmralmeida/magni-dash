# magni-dash
Dashboard for Magni dataset.


# Package installation

Install [miniconda](http://docs.conda.io/en/latest/miniconda.html). Then, you can install all packages required by running:

```
conda env create -f ex_environment.yml
```

Then, our own package:
```
pip install .
```

Set the [path](https://github.com/tmralmeida/magni-dash/blob/main/magni_dash/config/constants.py) to a directory with the following structure:

------------
    ├── Scenario1       <- Folder with tsv files for scenario 1 
        ├── file_name_{pp}.csv 
    ├── Scenario2        <- Folder with tsv files for scenario 2 
        ├── file_name_{pp}.csv 
    ├── Scenario3      <- Folder with tsv files for scenario 3 
        ├── file_name_{pp}.csv 
        ├── file_name_{merged}.csv (eyt data synched with trajectories)
    ├── Scenario4      <- Folder with tsv files for scenario 4 
        ├── file_name_{pp}.csv
    ├── Scenario5      <- Folder with tsv files for scenario 5 
        ├── file_name_{pp}.csv  

--------


# Launching dashboard

Run:

```
streamlit run magni_dash/Welcome.py
```