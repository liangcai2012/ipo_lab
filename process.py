import sys
sys.path.insert(0, '..')
import ipo_lab
import matplotlib.pyplot as plt

def distribution_pm(df, valve):
    start_year = df.index[0].year
    end_year = df.index[-1].year
    years = end_year - start_year + 1
    total = [0] * years
    pm_over_valve= [0] * years

    for i, row in df.iterrows():
        year = i.year - start_year
        total[year] +=1
        if row["pm"]/row["open_price"] >= valve:
            pm_over_valve[year]+=1
    return range(start_year, end_year+1), total, pm_over_valve

data = ipo_lab.load_data("./ipo_open.csv")
years, total, pov = distribution_pm(data, 1.02)
for i in range(len(years)):
    print years[i], "%.2f"%(pov[i]*1.0/total[i])
p1 = plt.bar(years, total, 0.35)
p2 = plt.bar(years, pm_ratio, 0.35)
plt.show()
