import sys
sys.path.insert(0, '..')
import ipo_lab
import pandas as pd
#import matplotlib.pyplot as plt

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
#        x_train.append([row["x1"], row["x2"], row["x3"], row["x4"], row["exchange"]])
        x_train.append([row["x1"]])
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
        #if(1 == clf.predict([[row["x1"], row["x2"], row["x3"], row["x4"], row["exchange"]]])[0]):
        p = clf.predict([[row["x1"]]])
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



x, y = ipo_lab.histo('./ipo.csv', "x1", 15, 1.02, 1)
print x
print y
