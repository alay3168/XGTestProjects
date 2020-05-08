import datetime
def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    yesterday = yesterday.strftime('%Y%m%d')
    return yesterday


yes = getYesterday()
print(yes[0:4])
print(yes[4:6])
print(yes[6:8])


ss = '10.58.122.240_20200427224142251_1.jpg'
print(ss.split('_')[0])

