
# flow == (period, phase, amount)   (phase < period)

def gcd(a, b):
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def lcmm(*args):
    return reduce(lcm, args)

def bisect_monotonic_interval(merged, lt, lv, rt, rv):

    sv = lv - _value_at_time(lt, merged)

    lo = lt
    hi = rt
    while lo < hi:
        mid = (lo+hi)//2

        v = _value_at_time(mid, merged) + sv

        if v >= 0: lo = mid+1
        else: hi = mid
    return lo

def _merged_event_interval_monotonic(merged, startTime, endTime, value):

    nextdectime = endTime
    nextinctime = endTime

    t = startTime
    for x in merged:
        diff = (x[0] - (((t - x[1]) % x[0])))
        if diff == x[0]:
            xnt = t
        else:
            xnt = t + diff

        if x[2] > 0:
            if xnt < nextinctime:
                nextinctime = xnt
        else:
            if xnt < nextdectime:
                nextdectime = xnt


    if nextinctime < nextdectime:
        inc = True
        t = nextinctime
    else:
        inc = False
        t = nextdectime

    sv = _value_at_time(startTime - 1, merged)

    v = _value_at_time(startTime, merged) - sv + value
    if v < 0:
        return (startTime, v, v - value, v - value)

    pt = startTime
    pv = v
    vmin = value
    if v < vmin:
        vmin = v

    while t < endTime:

        if inc:

            if t > pt + 1:
                v = _value_at_time(t - 1, merged) - sv + value
                if v < vmin:
                    vmin = v
                if v < 0:
                    t = bisect_monotonic_interval(merged, pt, pv, t - 1, v)
                    v = _value_at_time(t, merged) - sv + value
                    return (t, v, v - value, vmin - value)
                pt = t - 1
                pv = v
            
            v = _value_at_time(t, merged) - sv + value
            if v < vmin:
                vmin = v
            if v < 0:
                return (t, v, v - value, vmin - value)
            pt = t
            pv = v

            nextdectime = endTime
            for x in merged:
                if x[2] < 0:
                    diff = (x[0] - (((t + 1 - x[1]) % x[0])))
                    if diff == x[0]:
                        xnt = t + 1
                    else:
                        xnt = t + 1 + diff
                    if xnt < nextdectime:
                        nextdectime = xnt
            t = nextdectime

            inc = False
        else:

            if t > pt + 1:
                v = _value_at_time(t - 1, merged) - sv + value
                if v < vmin:
                    vmin = v
                if v < 0:
                    t = bisect_monotonic_interval(merged, pt, pv, t - 1, v)
                    v = _value_at_time(t, merged) - sv + value
                    return (t, v, v - value, vmin - value)
                pt = t - 1
                pv = v
 
            v = _value_at_time(t, merged) - sv + value
            if v < vmin:
                vmin = v
            if v < 0:
                return (t, v, v - value, vmin - value)
            pt = t
            pv = v

            nextinctime = endTime
            for x in merged:
                if x[2] > 0:
                    diff = (x[0] - (((t + 1 - x[1]) % x[0])))
                    if diff == x[0]:
                        xnt = t + 1
                    else:
                        xnt = t + 1 + diff
                    if xnt < nextinctime:
                        nextinctime = xnt
            t = nextinctime
            inc = True

    diff = _value_at_time(endTime - 1, merged) - sv

    v = diff + value
    if v < vmin:
        vmin = v

    if v < 0:
        t = endTime - 1
        t = bisect_monotonic_interval(merged, pt, pv, t, v)
        v = _value_at_time(t, merged) - sv + value
        return (t, v, v - value, vmin - value)

    ret = (endTime, v, diff, vmin - value)
    return ret

def _merged_event_interval_slow(merged, startTime, endTime, value):
    dv = value - _value_at_time(startTime - 1, merged)

    vmin = value
    diff = 0    

    for i in xrange(startTime, endTime):
        v = dv + _value_at_time(i, merged)
        if v < vmin:
            vmin = v
        if v < 0:
            return (i, v, v - value, vmin - value)
    
    return (endTime, v, v - value, vmin - value)

def _merged_event_interval(merged, startTime, endTime, value):

    l = len(merged)
    nexttimes = [0] * l

    t = startTime

    nt = endTime
    for i in xrange(l):
        x = merged[i]
        diff = (x[0] - (((t - x[1]) % x[0])))
        if diff == x[0]:
            xnt = t
        else:
            xnt = t + diff

        nexttimes[i] = xnt
        if xnt < nt:
            nt = xnt

    t = nt

    diff = 0
    _dmin = 0

    while t < endTime:
        nt = endTime
        for i in xrange(l):
            xnt = nexttimes[i]
            if t == xnt:
                x = merged[i]
                value += x[2]
                diff += x[2]
                
                xnt = t + x[0]
                nexttimes[i] = xnt
                if xnt < nt:
                    nt = xnt
            else:
                if xnt < nt:
                    nt = xnt

        if diff < _dmin:
            _dmin = diff

        if value < 0:
            return (t, value, diff, _dmin)

        assert t < nt

        t = nt

    return (t, value, diff, _dmin)

def _merge_flows(flows):
    flows = flows[:]

    flows.sort(lambda x,y: y[1] - x[1] if x[0] == y[0] else y[0] - x[0])

    merged = []

    last_period = -1
    last_phase = -1

    for (period, phase, amount) in flows:
        if period == last_period and phase == last_phase:
            merged[-1] = (period, phase, merged[-1][2] + amount)
        else:
            merged.append ( (period, phase, amount) )
            last_period = period
            last_phase = phase

    merged = filter(lambda x:x[2] != 0, merged)

    l = lcmm (*map(lambda x:x[0], merged))

    return (l, merged)

    

def time_of_underflow(startTime, initialValue, flows):
    l, merged = _merge_flows(flows)
    return _time_of_underflow(startTime, initialValue, l, merged)

def times_of_under_and_overflows(startTime, initialValue, minValue, maxValue, flows):
    l, merged =_merge_flows(flows)
    
    underflow = _time_of_underflow(startTime, initialValue - minValue, l, merged)
    
    merged_negative = map(lambda x:(x[0],x[1],-x[2]), merged)

    overflow = _time_of_underflow(startTime, maxValue - initialValue, l, merged_negative)

#    return (underflow, None)
    return (underflow, overflow)

def times_of_under_and_overflows_monotonic(startTime, initialValue, minValue, maxValue, flows):
    l, merged =_merge_flows(flows)
    
    underflow = _time_of_underflow_monotonic(startTime, initialValue - minValue, l, merged)
    
    merged_negative = map(lambda x:(x[0],x[1],-x[2]), merged)

    overflow = _time_of_underflow_monotonic(startTime, maxValue - initialValue, l, merged_negative)

    return (underflow, overflow)

def times_of_under_and_overflows_slow(startTime, initialValue, minValue, maxValue, flows):
    l, merged =_merge_flows(flows)
    
    underflow = _time_of_underflow_slow(startTime, initialValue - minValue, l, merged)
    
    merged_negative = map(lambda x:(x[0],x[1],-x[2]), merged)

    overflow = _time_of_underflow_slow(startTime, maxValue - initialValue, l, merged_negative)

    return (underflow, overflow)


def _time_of_underflow(starttime, initialvalue, l, merged):

    t = starttime

    diff = 0
    _min = 0
    _max = 0

    value = initialvalue

    t, tval, diff, _min = _merged_event_interval(merged, starttime, starttime + l, value)
    if tval < 0:
        return t

    if diff >= 0:
        return None
       
    iterations = 1 + (initialvalue + _min) // - diff

    laststarttime = starttime + iterations * l
    value = initialvalue + iterations * diff

    t, tval, diff, _min = _merged_event_interval(merged, laststarttime, laststarttime + l, value)

    if tval < 0:
        return t

    assert false

def _time_of_underflow_slow(starttime, initialvalue, l, merged):

    t = starttime

    diff = 0
    _min = 0
    _max = 0

    value = initialvalue

    t, tval, diff, _min = _merged_event_interval_slow(merged, starttime, starttime + l, value)
    if tval < 0:
        return t

    if diff >= 0:
        return None
       
    iterations = 1 + (initialvalue + _min) // - diff

    laststarttime = starttime + iterations * l
    value = initialvalue + iterations * diff

    t, tval, diff, _min = _merged_event_interval_slow(merged, laststarttime, laststarttime + l, value)

    if tval < 0:
        return t

    assert False


def _time_of_underflow_monotonic(starttime, initialvalue, l, merged):

    t = starttime

    diff = 0
    _min = 0
    _max = 0

    value = initialvalue

    t, tval, diff, _min = _merged_event_interval_monotonic(merged, starttime, starttime + l, value)
    if tval < 0:
        return t

    if diff >= 0:
        return None
       
    iterations = 1 + (initialvalue + _min) // - diff

    laststarttime = starttime + iterations * l
    value = initialvalue + iterations * diff

    t, tval, diff, _min = _merged_event_interval_monotonic(merged, laststarttime, laststarttime + l, value)

    if tval < 0:
        return t

    assert False



def _value_at_time(time, merged):
    v = 0
    for period, phase, amount in merged:
        v += amount * ((time - phase) // period)

    return v


if __name__ == "__main__":

    i = 10
    j = 112
    flows = [(500, 0, 100), (600, 0, 50), (1,0,-1)]

    for i in xrange(0, 100):
        for j in xrange(0, 300):
#             print `(i, j)`
             um, om = times_of_under_and_overflows_monotonic (j, i, 0, 107, flows)
             u, o = times_of_under_and_overflows (j, i, 0, 107, flows)

             print `(u, o, um, om)`

#             print `(um, om)`
             assert u == um
             assert o == om

