import pandas as pd

def load_data(path):
    df = pd.read_csv(path, index_col=[0], date_parser=lambda x:pd.datetime.strptime(x, "%Y%m%d"))
    sdf = df.sort_index()
    return sdf

