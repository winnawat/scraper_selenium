import math
import numpy as np
import time


def sleep_poisson(poi_lambda=10, time_interval=60, max_sleep = 1.94):
    """
    Sleep function based on poisson distribution so as not to spam facebook
    Also wait until the next page loads
    poi_lambda (int): number of expected occurrences in a time interval for poisson distribution. Default is 10 clicks in 60 seconds.
    time_interval (int): Number used to divide the time interval. Default is 60. Dividing by 60 makes it 10 clicks in 1 second.
    This is equivalent to "mimicking a time delay of a human performing 10 actions in 1 seconds."
    max_sleep (float): Poisson is long tailed. We don't want to wait for longer than (default) 1.94s.
    """
    time.sleep(np.minimum((np.random.poisson(poi_lambda,1)/time_interval)[0], max_sleep))

def convert_likes(x):
    if type(x) == float:
        if math.isnan(x):
            return 0
        else:
            return int(x)
    if x.isnumeric():
        return int(x)
    if x == '':
        return 0
    if ' others' in x:
        x = x[:-7]
        print(x)
        if x[-1] == 'K':
            x = x.split(' ')[-1]
            return int(float(x[:-1]) * 1000)
    if x[-1] == 'K':
        return int(float(x[:-1]) * 1000)
    else:
        return 0

def get_value_of_array(x):
    if x == []:
        return np.nan
    else:
        return x[0]
    
def get_sponsored(x, sponsored_by):
    if isinstance(x, str):
        if any(kw in x for kw in sponsored_by):
            return 'SPONSORED'
        else:
            return 'ORGANIC'
    else:
        return 'ORGANIC'

def get_sponsor_name(x, sponsored_by, sponsored_label = 'sponsored'):
    if x[sponsored_label] == 'SPONSORED':
        for kw in sponsored_by:
            split_by_kw = x['texts'].split(kw)
            if len(split_by_kw) > 1:
                return split_by_kw[-1][1:].replace('.','')
    else:
        return 'ORGANIC'
