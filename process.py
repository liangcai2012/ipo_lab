import sys
sys.path.insert(0, '..')
import ipo_lab
import matplotlib.pyplot as plt

def pop_by_hot(df, h_scope, p_scope):
    hot = []
    pop = []
    total = 0
    dbz = 0 #num of divide by zero
    oos = 0 # num of dots out of scope of hot and pop valus
    for i, row in df.iterrows():
        total += 1
        if row["ipo_price"] == 0 or row["open_price"] == 0:
            dbz += 1
            continue
        h = row["open_price"]*1.0/row["ipo_price"]
        p = row["pm"]*1.0/row["open_price"]
        if p > 2 or p < 1:
            print i, row["symbol"], row["ipo_price"], row["open_price"], row["pm"]
        if h< h_scope and p < p_scope:
            hot.append(h)
            pop.append(p)
        else:
            oos += 1
    print "total:", total, "zero: ",dbz, "out of scope:", oos
    return hot, pop

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
h, p = pop_by_hot(data, 2, 3)
#years, total, pov = distribution_pm(data, 1.02)
#for i in range(len(years)):
#    print years[i], "%.2f"%(pov[i]*1.0/total[i])
#p1 = plt.bar(years, total, 0.35)
#p2 = plt.bar(years, pm_ratio, 0.35)
#plt.show()


