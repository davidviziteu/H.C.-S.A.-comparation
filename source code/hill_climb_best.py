import multiprocessing as mp
import threading as th
import numpy as np
import time
import math
import functions
import general_stuff as g
import sys
from datetime import datetime

#         start_time = time.time()
#         print(" dimension: ", i, " time: ", (time.time() - start_time))

workers = 1
iterations = 10**4
sample_size = 1
dimensions = [5, 10, 30]
output_file = "hc_best.txt"


def write_to_file(l, msg):
    l.acquire()
    try:
        with open("hc_best.txt", "a") as fl:
            fl.write(msg)
    finally:
        l.release()


def best_hc(fnc, interval, n, iters, lock, seed, smpl_sz):
    smpl_sz = int(smpl_sz)
    print(f'started process {seed} iterations = {iters}')
    np.random.seed(seed)
    comp_len = g.compute_comp_len(interval)
    for dimension in n:
        for s in range(0, smpl_sz):
            print(f'process[{seed}] now at sample = {s}, dimension = {dimension}')
            total_bits = comp_len * dimension
            f_min = math.inf
            start_time = time.time()
            for iii in range(0, iters):
                bits_arr = np.random.randint(2, size=total_bits)
                floats = g.get_floats(bits_arr, interval, comp_len, dimension)
                res = fnc(floats)
                if res < f_min:
                    f_min = res
                while 1:
                    best_idx = None
                    for idx, itm in enumerate(bits_arr):
                        bits_arr[idx] = not bits_arr[idx]
                        floats = g.get_floats(bits_arr, interval, comp_len, dimension)
                        floats = np.around(floats, g.decimal_precision)
                        res = fnc(floats)
                        if res < f_min:
                            f_min = res
                            best_idx = idx
                        bits_arr[idx] = not bits_arr[idx]
                    if best_idx is None:
                        break
                    bits_arr[best_idx] = not bits_arr[best_idx]
            write_to_file(lock, f'{f_min} {time.time() - start_time} {dimension}\n')

        # print(" dimension: ", i, " time: ", (time.time() - start_time))


if __name__ == "__main__":
    print("HILL CLIMB FIRST IMPROVEMENT")
    if sys.argv[1].lower() == "r":
        print("rastrigin")
        with open(output_file, "a") as file:
            now = datetime.now()
            file.write(f'\n\n rastrigin - {now.strftime("%d/%m/%Y %H:%M:%S")} w/ {iterations} iterations\n')
        domain = [-5.12, 5.12]
        thrd_lock = mp.RLock()
        threads_arr = []
        for ii in range(0, workers):
            t = mp.Process(target=best_hc,
                           args=(functions.rastrigin, domain, dimensions, iterations, thrd_lock, ii, sample_size/workers))
            threads_arr.append(t)
            t.start()

    elif sys.argv[1].lower() == "m":
        print("michalewicz")
        with open(output_file, "a") as file:
            now = datetime.now()
            file.write(f'\n\n michalewicz - {now.strftime("%d/%m/%Y %H:%M:%S")} w/ {iterations} iterations\n')
        domain = [0, np.pi]
        thrd_lock = mp.RLock()
        threads_arr = []
        for ii in range(0, workers):
            t = mp.Process(target=best_hc,
                           args=(functions.michalewicz, domain, dimensions, iterations, thrd_lock, ii, sample_size/workers))
            threads_arr.append(t)
            t.start()

    elif sys.argv[1].lower() == "d":
        print("dejong")
        with open(output_file, "a") as file:
            now = datetime.now()
            file.write(f'\n\n dejong - {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
        domain = [-5.12, 5.12]
        thrd_lock = mp.RLock()
        process_arr = []
        for ii in range(0, workers):
            t = mp.Process(target=best_hc,
                           args=(functions.dejong, domain, dimensions, iterations, thrd_lock, ii, sample_size/workers))
            process_arr.append(t)
            t.start()

    elif sys.argv[1].lower() == "s":
        print("schwefel")
        with open(output_file, "a") as file:
            now = datetime.now()
            file.write(f'\n\n schwefel - {now.strftime("%d/%m/%Y %H:%M:%S")} w/ {iterations} iterations\n')
        domain = [-500, 500]
        thrd_lock = mp.RLock()
        threads_arr = []
        for ii in range(0, workers):
            t = mp.Process(target=best_hc,
                           args=(functions.schwefel, domain, dimensions, iterations, thrd_lock, ii, sample_size/workers))
            threads_arr.append(t)
            t.start()

    elif sys.argv[1].lower() == "all":
        # ---------------------------------------- ALL --------------------------------------------
        print("rastrigin")
        with open(output_file, "a") as file:
            now = datetime.now()
            file.write(f'\n\n rastrigin - {now.strftime("%d/%m/%Y %H:%M:%S")} w/ {iterations} iterations\n')
        domain = [-5.12, 5.12]
        thrd_lock = mp.RLock()
        threads_arr = []
        for ii in range(0, workers):
            t = mp.Process(target=best_hc,
                           args=(functions.rastrigin, domain, dimensions, iterations, thrd_lock, ii, sample_size/workers))
            threads_arr.append(t)
            t.start()
        for ii in range(0, workers):
            threads_arr[ii].join(None)

        print("michalewicz")
        with open(output_file, "a") as file:
            now = datetime.now()
            file.write(f'\n\n michalewicz - {now.strftime("%d/%m/%Y %H:%M:%S")} w/ {iterations} iterations\n')
        domain = [0, np.pi]
        thrd_lock = mp.RLock()
        threads_arr = []
        for ii in range(0, workers):
            t = mp.Process(target=best_hc,
                           args=(functions.michalewicz, domain, dimensions, iterations, thrd_lock, ii, sample_size/workers))
            threads_arr.append(t)
            t.start()
        for ii in range(0, workers):
            threads_arr[ii].join(None)

        print("dejong")
        with open(output_file, "a") as file:
            now = datetime.now()
            file.write(f'\n\n dejong - {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
        domain = [-5.12, 5.12]
        thrd_lock = mp.RLock()
        process_arr = []
        for ii in range(0, workers):
            t = mp.Process(target=best_hc,
                           args=(functions.dejong, domain, dimensions, iterations, thrd_lock, ii, sample_size/workers))
            process_arr.append(t)
            t.start()
        for ii in range(0, workers):
            process_arr[ii].join(None)

        print("schwefel")
        with open(output_file, "a") as file:
            now = datetime.now()
            file.write(f'\n\n schwefel - {now.strftime("%d/%m/%Y %H:%M:%S")} w/ {iterations} iterations\n')
        domain = [-500, 500]
        thrd_lock = mp.RLock()
        threads_arr = []
        for ii in range(0, workers):
            t = mp.Process(target=best_hc,
                           args=(functions.schwefel, domain, dimensions, iterations, thrd_lock, ii, sample_size/workers))
            threads_arr.append(t)
            t.start()
        for ii in range(0, workers):
            threads_arr[ii].join(None)

    else:
        print("incorrect args")


# help
