
# flow == (period, phase, amount)   (phase < period)

def gcd(a, b):
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def lcmm(*args):
    return reduce(lcm, args)


def _nextevent(time, x):

    diff = (x[0] - (((time - x[1]) % x[0])))
    if diff == x[0]:
        return time
    return time + diff

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

        #xnt = _nextevent(t, merged[i])
        nexttimes[i] = xnt
        if xnt < nt:
            nt = xnt

    t = nt

    diff = 0
    _dmin = 0
    _dmax = 0

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
        if diff > _dmax:
            _dmax = diff

        if value < 0:
            return (t, value, diff, _dmin, _dmax)

        t = nt

    return (t, value, diff, _dmin, _dmax)

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

    l = lcmm (*map(lambda x:x[0], merged))

    return (l, flows)

    

def time_of_underflow(startTime, initialValue, flows):
    l, merged = _merge_flows(flows)
    return _time_of_underflow(startTime, initialValue, l, merged)

def times_of_under_and_overflows(startTime, initialValue, minValue, maxValue, flows):
    l, merged =_merge_flows(flows)
    
    underflow = _time_of_underflow(startTime, initialValue - minValue, l, merged)
    
    merged_negative = map(lambda x:(x[0],x[1],-x[2]), merged)

    overflow = _time_of_underflow(startTime, maxValue - initialValue, l, merged_negative)

    return (underflow, overflow)

def _time_of_underflow(startTime, initialValue, l, merged):

    t = startTime

    diff = 0
    _min = 0
    _max = 0

    value = initialValue

    t, tval, diff, _min, _max = _merged_event_interval(merged, startTime, startTime + l, value)
    if tval < 0:
        return t

    if diff >= 0:
        return None
       
    iterations = 1 + (initialValue + _min) // - diff

    lastStartTime = startTime + iterations * l
    value = initialValue + iterations * diff

    t, tval, diff, _min, _max = _merged_event_interval(merged, lastStartTime, lastStartTime + l, value)

    if tval < 0:
        return t

    assert False


if __name__ == "__main__":


    for i in xrange(0, 100):
        for j in xrange(0, 300):
            u, o = times_of_under_and_overflows (j, i, 0, 110, [(10,0,1), (10,0,-1), (100,0,5), (100,0,-4), (100,0,-5), (10,0,1), (10, 0, -5)])

