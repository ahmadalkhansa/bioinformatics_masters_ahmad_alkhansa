def get_lowest(filename):
    d={}
    maxv = float(‘inf’)
    f=open(filename)
    for line in f:
        v= line.split()
        sid=v[0]
        eva=float(v[10]
        d[v[sid]]=min(d.get(sid,maxv),eva)
    return d

for k in d.keys():
    print(k, d[k])

