import sys
sys.path.insert(0, '..')
import ipo_lab
import pandas as pd
import matplotlib.pyplot as plt

def detect_overlap():
    df= ipo_lab.load_data("./ipo_open.csv")
    sdf = df.sort_values(by=['symbol'])
    prev_sym = ""
    for i, row in sdf.iterrows():
        if prev_sym == "":
            prev_sym = row["symbol"]
        else:
            if prev_sym == row["symbol"]:
                print row["symbol"], i
            prev_sym = row["symbol"]

    
def merge():
    df_open = ipo_lab.load_data("./ipo_open.csv")
    sdf_open = df_open.sort_values(by=['symbol'])
    with open("./ipo5.csv") as f:
        line = f.readline().strip()
        ls = line.split(',')
        ls.insert(1, "date")
        print ','.join(ls)
        line = f.readline().strip()
        while line:
            ls = line.split(',')
            symbol = ls[0]
            d= df_open.loc[df_open["symbol"] == symbol].iloc[0, 0]
            if d is None:
                print "--------- missing", symbol
                continue
            ls.insert(1,str(d))
            print ','.join(ls)
            line = f.readline().strip()
        print line

    exit()
    df= ipo_lab.load_data("./ipo.csv")
    sdf = df.sort_values(by=["symbol"])

    print "symbol,date,y,x1,x2,x3,x4,x5,underwriter,exchange"
    j = 0
    for i in range(len(sdf_open)):
        row_open = sdf_open.iloc[i]
        row = sdf.iloc[j]
        while row["symbol"] < row_open["symbol"]:
#            print "missing in ipo_open.csv", row["symbol"], row_open["symbol"]
            j+= 1
            row = sdf.iloc[j]

        if row["symbol"] > row_open["symbol"]:
#            print "missing in ipo.csv", row["symbol"], row_open["symbol"]
            continue

        line = []
        line.append(row["symbol"])
        line.append(str(row_open["date"]))
        line.append("%.3f"%row["y"])
        line.append("%.3f"%row["x1"])
        line.append(str(row["x2"]))
        line.append("%.3f"%row["x3"])
        line.append("%.3f"%row["x4"])
        line.append(str(row_open["minutes"]))
        line.append(str(row["underwriter"]))
        line.append(str(row["exchange"]))
        print ','.join(line)
        j+=1


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

def parse_uw():
    df = pd.read_csv('./ipo_uws.csv')
    uw_list = df["underwriter"]
    
    print uw_list
    uw_set = set(uw_list)
    print len(uw_list)
    print len(uw_set)

def filter_by_exch(valve):
    df = pd.read_csv('./ipo.csv')
    tt = tf = ff = ft = 0
    no = 0
    for i, row in df.iterrows():
        no += 1
        if no <= 0: 
            continue
       # if row["exchange"] == 1:
        if row["x1"] > 1.1:
            if row["y"] > valve:
                tt += 1
            else:
                ft += 1
        else:
            if row["y"] > valve:
                tf += 1
            else:
                ff += 1
    s = tt+tf+ft+ff
    print tt, tf, ft, ff, s, 'exchange filter true rate:', (tt+ff)*1.0/s, 'random:', (tt+tf)*1.0/s, 'svm:', tt*1.0/(tt + ft) 


def svm(training_size, valve):
    from sklearn import svm
    df = pd.read_csv('./ipo.csv')

    #training
    x_train = []
    y_train = []
    no = 0
    for i, row in df.iterrows():
        no += 1
        if no> training_size:
            break
        if row["y"]> valve:
            y_train.append(1)
        else:
            y_train.append(0)
        x_train.append([row["x1"], row["x2"], row["x3"], row["x4"], row["exchange"]])
#        x_train.append([float(row["x1"]), float(row["x2"])])
#    print y_train
#    print x_train
    clf = svm.SVC(gamma='scale',kernel='rbf')
    clf.fit(x_train, y_train)
    print clf

   #accuracy
    no = 0
    tt = tf = ff = ft = 0
    for i, row in df.iterrows():
        no += 1
        if no <= training_size:
            continue
#        if(1 == clf.predict([[row["x1"], row["x2"], row["x3"], row["x4"], row["exchange"]]])[0]):
        p = clf.predict([[row["x1"], row["x2"], row["x3"], row["x4"], row["exchange"]]])
#        print p
        if 1 == p[0]:
            if row["y"] > valve:
                tt += 1
            else:
                ft += 1
        else:
            if row["y"] > valve:
                tf += 1
            else:
                ff += 1
    s = tt+tf+ft+ff
    print tt, tf, ft, ff, s, 'svm true rate:', (tt+ff)*1.0/s, 'random:', (tt+tf)*1.0/s, 'svm:', tt*1.0/(tt + ft) 


#data = ipo_lab.load_data("./ipo_open.csv")
#h, p = pop_by_hot(data, 2, 3)

#parse_uw()
#detect_overlap()

#v = 1.03
#svm(700, v)
#filter_by_exch(v)

#plot distribution y, x1-x4
def plot_y_dist():
    df = ipo_lab.load_data("./ipo5.csv")
    x, y, step = ipo_lab.distribution(df, 'p1m', 100)
    print len(x)
    plt.bar(x[:40], y[:40], width=step)
    plt.show()

def print_min_dist():
    dfm= ipo_lab.load_data("./ipo3.csv")
    bin = [0]*11
    for i, row in dfm.iterrows():
        if 0 <= row["t10"]<=11:
            bin[row["t10"]-1] += 1
        if 10<= row["t10"] <= 11:
            if row["p30"] < row["y"]:
                print row["symbol"], row["y"], row["t10"], row["p30"], row["t30"]
        else:
            #print "unexpected minutes", row["symbol"], row["t10"]
            continue
#    print bin
    
    
#plot distribution x1-x4
def plot_x1_4_dist():
    df = ipo_lab.load_data("./ipo.csv")
    fig, axs = plt.subplots(2, 2, sharey=True, tight_layout=True)
    cols = ['x1','x2','x3','x4']
    ends = [50,80,30,50]
#    ylims = [1200, 1200, 300, 300]
    for i in range(4):
        x, y, step = ipo_lab.distribution(df, cols[i], 100)
        axs[i/2][i%2].bar(x[:100-ends[i]], y[:100-ends[i]], width=step)
        axs[i/2][i%2].set_title('distribution of '+cols[i])
#        axs[i/2][i%2].set_ylim(0, ylims[i])
        
    plt.show()

#plot step x1-x4 with y wehen valve = 1.02
def plot_y_vs_x1_4_v102():
    df = ipo_lab.load_data("./out_bad.csv")
    fig, axs = plt.subplots(2, 2, sharey=True, tight_layout=True)
    cols = ['x1','x2','x3','x4']
    for i in range(4):
        x, y = ipo_lab.histo(df, cols[i], 20, 1.01, 1)
        print 'distribution of', cols[i]
        for l in range(len(x)):
            print x[l], y[l]
        axs[i/2][i%2].step(x, y)
        axs[i/2][i%2].set_title('y/'+cols[i])
    plt.show()

#plot step x1 with y when valve changes    
def plot_y_vs_x1_v101_104():
    df = ipo_lab.load_data("./ipo.csv")
    fig, axs = plt.subplots(2, 2, sharey=True, tight_layout=True)
    for i in range(101, 105):
        v = i/100.0
        x, y = ipo_lab.histo(df, "x1", 20, v, 1)
        l = "vavle = %.2f"%v
        m = i - 101
        axs[m/2][m%2].step(x, y)
        axs[m/2][m%2].set_title(l)
    plt.show()

def plot_y_vs_luw():
    df = ipo_lab.load_data("./ipo.csv")
    id, num, p = ipo_lab.luw_dist(df, 1.02, 25)
    print id, num, p
    x = []
    sum = 0
    for n in num:
        x.append(sum + n)
        sum += n
    plt.step(x, p)
    plt.show()

def print_y_vs_exchange():
    df = ipo_lab.load_data("./ipo.csv")
    ex_res = ipo_lab.exchange_dist(df, 1.02)
    sum = 0
    p = 0
    exchange = ['NASDAQ','NYSE','AMEX']
    for i in range(len(ex_res)):
        r = ex_res[i]
        print exchange[i], r[1]*1.0/r[0], r[0]
        sum+= r[0]
        p += r[1]
    print "TOTAL", p*1.0/sum, sum
    
#def dist_t10():
#    df = ipo_lab.load_data("./ipo5.csv")
#    for i, row in df.iterrows():


#merge()
#exit()
#plot_y_dist()
#plot_x1_4_dist()
#plot_y_vs_x1_4_v102()
#plot_y_vs_x1_v101_104()
#plot_y_vs_luw()
#print_y_vs_exchange()
#exit()

#detect_overlap()
#print_min_dist()
df = ipo_lab.load_data("./ipo5.csv")
#ipo_lab.simple_filter(df, 1.02)
for i in range(102, 115):
    ipo_lab.simple_strat_2(df, "pc10", 1.0001, i/100.0, range(2010, 2019))
#svm(1000, 1.02)
