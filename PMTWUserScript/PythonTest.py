import matplotlib.pyplot as plt
import numpy as np
 

try:
    a = float("3.15a")
    print(a)
except Exception as ex:
    print(f"Unexpected {ex=}, {type(ex)=}")