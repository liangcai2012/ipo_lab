import pandas as pd
import matplotlib.pyplot as plt

def load_data(path):
    df = pd.read_csv(path, index_col=[0], date_parser=lambda x:pd.datetime.strptime(x, "%Y%m%d"))
    sdf = df.sort_index()
    return sdf

def distribution_pm(data, valve):
    start_year = data.index[0].year
    end_year = data.index[-1].year
    years = end_year - start_year + 1
    total = [0] * years
    pm_ratio = [0] * years

    for i, row in data.iterrows():
        year = i.year - start_year
        total[year] +=1
        if row["pm"]/row["open_price"] >= valve:
            pm_ratio[year]+=1
    return range(start_year, end_year+1), total, pm_ratio

data = load_data("./ipo_open.csv")
years, total, pm_ratio = distribution_pm(data, 1.02)
p1 = plt.bar(years, total, 0.35)
p2 = plt.bar(years, pm_ratio, 0.35)
plt.show()
