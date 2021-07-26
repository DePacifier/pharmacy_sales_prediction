import dvc.api
import pandas as pd

# function that gets data from dvc


def get_dvc_data(file_name: str, version: str = 'initial-data', repo: str = 'https://github.com/DePacifier/pharmacy_sales_prediction') -> pd.DataFrame:
    path = f'data/{file_name}'
    data_url = dvc.api.get_url(path=path, repo=repo, rev=version)
    data = pd.read_csv(data_url)

    return data
