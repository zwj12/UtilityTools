import matplotlib.pyplot as plt
import numpy as np
 
def Equidistant_spiral(a, b, num_points=5000, n=5):
    #a: 起始半径
    #b*2pi: 每圈增加的半径
    theta = np.linspace(0, 2 * np.pi * n, num_points)
    r = a + b * theta
 
    x = r * np.cos(theta)
    y = r * np.sin(theta)
 
    # print("theta: ", theta)
    print("r: ", r)
    # print("x: ", x)
    # print("y: ", y)
    plt.plot(x, y)
    plt.axis("equal")
    plt.title("Equidistant Spiral")
    plt.pause(10)
 
 
a = 0
b = 50
 
Equidistant_spiral(a, b, 36, 5)