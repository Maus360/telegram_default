import json
def query(week,day,korp,time):
    with open('/home/special20/development/scrap/1/tutorial/bsuir2.json') as data_file:
        data = json.load(data_file)
    '''corp={'1':[],
          '2':[],
          '3':[],
          '4':[],
          '5':[],
          '7':[],
          '':[]}
    #print(data[1])
    for i in data:
        corp[i['corp'][0]].append(i['classroom'][0])

    for i in sorted(corp):
        corp[i]=sorted(list(set(corp[i])))
        print(i,corp[i])
    with open('/home/special20/development/scrap/1/tutorial/class.json','w') as data_f:
        json.dump(corp,data_f)
    '''
    with open('/home/special20/development/scrap/1/tutorial/class.json') as data_file:
        corp = json.load(data_file)
    #week='4'
    #day=3
    #korp='1'
    #time='15:20-16:55'
    #print(len(data[32]['week'][0]))
    invalid=[i['classroom'][0] for i in data if i['time'][0]==time and i['day'][0]==2 and i['corp'][0]==korp and (week in i['week'][0] or len(i['week'][0])==0)]

    invalid=sorted(list(set(invalid)))
    print('\n','Недоступны: ',invalid)
    valid=[i for i in corp[korp] if i not in invalid]

    print('\n','Доступны: ',valid)
    return valid
