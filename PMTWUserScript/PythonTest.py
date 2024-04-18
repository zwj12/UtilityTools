import threading
import time

class UtilityClass:
    def incr(i):
        return i+1
        

def print_numbers(start, end, utilityClass):
    i = start
    while i < end:
        time.sleep(1)
        print(i)
        i = utilityClass.incr(i)

thread = threading.Thread(target=print_numbers, args=(1, 6, UtilityClass))
thread.start()
thread.join()