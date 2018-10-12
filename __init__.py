import pandas as pd

def load_data(path):
    df = pd.read_csv(path, index_col=[0], date_parser=lambda x:pd.datetime.strptime(x, "%Y%m%d"))
    sdf = df.sort_index()
    return sdf


def histo(path, col, n, valve, dt):
    df = pd.read_csv(path)
    num = len(df)/n 
    if len(df)%n > 0:
        num += 1
    sdf = df.sort_values(by=['symbol'])
    idx = -1
    t = 0
    f = 0
    sec = 1 
    xax = []
    yax = []
    for i, row in df.iterrows():
        idx += 1
        if idx > num * sec:
            xax.append(row[col])
            if dt> 0:
                yax.append(t*1.0/(t+f))
            else:
                yax.append(f*1.0/(t+f))
            t = 0
            f = 0
            sec += 1
        if row["y"] > valve:
            t += 1
        else:
            f += 1

    return xax, yax
