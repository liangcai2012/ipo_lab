import pandas as pd
from datetime import datetime

_p = lambda x:"%.2f"%x
_dt = lambda x: datetime.strptime(str(x), "%H%M%S")

def load_data_sort_by_date(path):
    df = pd.read_csv(path, index_col=[0], date_parser=lambda x:pd.datetime.strptime(x, "%Y%m%d"))
    sdf = df.sort_index()
    return sdf

def load_data(path):
    df = pd.read_csv(path)
    return df

def distribution(df, col, num):
    sdf = df.sort_values(by=[col])
    lb = sdf.iloc[0][col]
    rb = sdf.iloc[-1][col]
    step = (rb - lb)/num
    x = []
    y = []
    start = lb
    n = 0
    for i, row in sdf.iterrows():
        if row[col] > start + step:
            x.append(start)
            y.append(n)
            n = 0
            start += step
            for i in range(int((row[col] - start)/step)):
                x.append(start)
                y.append(0)
                start += step
        n += 1
    return x, y, step

def histo(df, col, n, valve, dt):
    num = len(df)/n 
    if len(df)%n > 0:
        num += 1
    sdf = df.sort_values(by=[col])
    idx = -1
    t = 0
    f = 0
    sec = 1 
    xax = []
    yax = []
    for i, row in sdf.iterrows():
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

def luw_dist(df, valve, top):
    res = [[0,0]]
    for i, row in df.iterrows():
        struws = row["underwriter"] 
        try:
            uws = row["underwriter"].split('-')
        except:
            continue
        for uw in uws:
            uwint = int(uw)
            if uwint > len(res):
                for k in range(uwint - len(res)):
                    res.append([0,0])
            res[uwint-1][0] += 1
            if row['y'] > valve:
                res[uwint - 1][1] += 1
    res_df  = pd.DataFrame(data = res, columns=['num', 'p1'])
    sdf = res_df.sort_values(by="num", ascending=False).iloc[:top] 
    id = []
    num = []
    p = []

    for i, row in sdf.iterrows():
        id.append(i)
        num.append(row["num"])
        p.append(row["p1"]*1.0/row["num"])

    return id, num, p


def exchange_dist(df, valve):
    res = [[0,0], [0,0],[0,0]]
    for i, row in df.iterrows():
        if row["exchange"] < 1 or row["exchange"]>3:
            print 'unexpected exchange', row[symbol], row['exchange']
            continue
        res[row["exchange"]-1][0]+= 1
        if row['y']>valve:
            res[row["exchange"]-1][1]+=1
    return res
  
def simple_filter(df, valve):
    sum = 0
    p = 0
    p30 = p1h = p1d = 0
    bin = [0]*12
    profit = 0
    for i, row in df.iterrows():
#        if 0.955 < row["x1"]<1.035: 
#            continue
#        if row["x2"] > 180000:
#            continue
#        if row["t10"]<93200:
#            continue
#        uwlist = row["underwriter"].split('-')
#        found = False
#        for u in uwlist:
#            if u == '13':
#                found = True
#                break
#        if found:
#            continue

#      the following filtered out 22 symbols and 11 are good
#        if  0.6 < row["x3"]< 0.9:
#            continue
        
##      The following filtered out 138 symbols and 95 are good         
#        if row['exchange'] != 1:
#            print row["symbol"], row["y"]
#           continue
##       The following filter only filtered out 3 symbols while 2 of them are good
#        if len(row["symbol"]) > 4:
#            print row["symbol"], row["y"]
#            continue
##       The following filter only filtered out 4 symbols while 2 of them are good        
#        if 0.75 < row["x3"]<0.9:
#            print row["symbol"], row["y"]
#            continue

        sum += 1
#        if row["p1d"] > valve:
        if row["p1d"] > 1.01:
            p += 1
#            profit += 0.02
            profit += row["pc1d"] - 1.01
        else:
#            if row["y"] == 1 and row["p1d"] == 1:
#                print row["symbol"], row["x1"], row["x3"]
            if row["p30"] > valve:
                p30+=1
            if row["p1h"] > valve:
                p1h += 1
            if row["p1d"] > valve:
                p1d += 1
#            if row["pc10"] < 0.9:
#                print row["symbol"], row["y"], row["t10"], row["x1"], row["x3"], row["pl10"], row["tl10"], row["pc10"]
#            profit += row["pc1d"] - 1

#        if 0 <= row["t10"]<=11:
#            bin[row["t10"]] += 1
#        if 10<= row["t10"] <= 11:
#            if row["p30"] < row["y"]:
#                print row["symbol"], row["y"], row["t10"], row["p30"], row["t30"]
    print p, p30, p1h, p1d, sum, p*1.0/sum, sum*1.0/len(df)
#    print bin 
    print 'profit:', profit

# but when price exceed in a time frame
def simple_strat_2(df, col, valve, vhigh, years):
    total_profit = 0
    print vhigh, '---', 
    for y in years:
        
        total = 0
        triggered = 0
        bad = 0
        missing = 0
        profit = 0
        bad_profit = 0
        missing_profit = 0
        above_valve = 0
        for i, row in df.iterrows():
            d = row["date"]
            if y != d/10000:
                continue
#            if 0.975 < row["x1"]<1.018: 
#                continue
#            if row["x2"] > 180000:
#                continue
            total += 1
            if row["p1m"]>=valve or row["y"] >= vhigh:
                triggered += 1

                if row["y"] >=vhigh:
                    profit += vhigh-1.0 
                    above_valve += 1
                else:
                    profit += row[col] - valve

                if row["y"] < vhigh and row[col] < valve:
                    bad += 1
                    bad_profit += row[col]-valve
                else:
                    topen = _dt(row["topen"])
                    t1m= _dt(row["t1m"])
                    t10 = _dt(row["t10"])
#                    print row["symbol"], row["y"], row["p1m"],  row["pc10"], (t1m-topen).total_seconds(), (t10-topen).total_seconds() 
#                if 1.04 <= row["y"] < 1.05:
#                    print row["symbol"], row["pc10"]
            else:
                profit += row["pc10"] - 1
                if row[col] > valve:
                    missing += 1
                    missing_profit += row[col]-valve
        if total == 0:
            continue
        total_profit += profit
#    print y, total, _p(triggered*1.0/total), _p(above_valve*1.0/total),  _p(bad*1.0/total), _p(missing*1.0/total), profit, bad_profit, missing_profit
        print profit, 
    print total_profit
