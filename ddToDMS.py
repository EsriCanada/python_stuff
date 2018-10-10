#This function converts decimal degrees to Degrees, Minutes, Seconds, and takes into account the negative values
def getDMS(dd):
    from math import ceil,floor
    if round(dd)>0:
        d = int(floor(dd))
    elif round(dd)<0:
        d = int(ceil(dd))
    m = abs((dd-int(dd))*60)
    s = m%1.0*60
    DMS = str(d)+"°"+ str(int(round(m)))+"'"+str(round(s,2))+'"'
    return DMS
