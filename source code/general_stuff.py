import numpy as np
import math

decimal_precision = 2


def compute_comp_len(interval, precision=decimal_precision):
    return math.ceil(math.log2((interval[1] - interval[0]) * 10**precision))


# meh, useless pt o linie
def generate_component(lenn):
    x = np.random.randint(2, size=lenn)
    return x


def get_floats(arr, interval, component_len, components_count):
    arr = np.asarray(arr)
    floats = []
    pwr = 2**component_len - 1
    for component in np.split(arr, components_count):
        tmp = 0
        for bit in component:
            tmp *= 2
            tmp += bit
        floats.append(interval[0] + tmp * (interval[1] - interval[0])/pwr)
    return floats




# testing
if __name__ == "__main__":
    comp_count = 30
    intervaal = [-500, 500]
    comp_len = compute_comp_len(intervaal)
    print(comp_len)
    x = np.random.randint(2, size=comp_len*comp_count)
    print(get_floats(x, intervaal, comp_len, comp_count))




