def mortgage(rate,loan,years,interval):
        intervals = {'Weekly':52,'Monthly':12,'Daily':365}
        units =  {'Weekly':'week','Monthly':'month','Daily':'day'}
        p = loan
        n = intervals[interval] * years
        r = rate/12

        pay = round(p*((r*(r+1)**n)/(((r+1)**n)-1)),2)
        return str(pay),str(round((pay*n),2)),units[interval]
mortgage(0.06,12,12,'Daily')