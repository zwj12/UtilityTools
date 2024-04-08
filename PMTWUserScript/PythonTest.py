import tkinter
import tkinter.messagebox
import threading
import time
import socket

# class Parent1:
#     def __init__(self):
#         print("Parent1 constructor")

#     def add(self):
#         print('self is {0} @Parent1.add'.format(self))

# class Parent2:
#     def __init__(self):
#         print("Parent2 constructor")

#     def add(self):
#         print('self is {0} @Parent2.add'.format(self))

# class Parent3:
#     def __init__(self):
#         print("Parent3 constructor")

#     def add(self):
#         print('self is {0} @Parent3.add'.format(self))

# class Child(Parent1,Parent2,Parent3):    # 顺序为Parent1,Parent2,Parent3
#     def __init__(self):
#         super().__init__()               # 使用简化写法，调用了 Parent1 的构造方法

#     def add(self):
#         print('self is {0} @Child.add'.format(self))
#         super().add()

# child = Child()
# child.add()

#输出结果：Parent1 constructor


class A:
    def __init__(self):
        print("A enter")
        super().__init__()
        print("A exit")
        
    def add(self):
        print('A add enter')
        super().add()
        print('A add exit')

class B(A):
    def __init__(self):
        print("B enter")
        super().__init__()
        print("B exit")
        
    def add(self):
        print('B add enter')
        super().add()
        print('B add exit')
        

class C:
    def __init__(self):
        print("C enter")
        super().__init__()
        print("C exit")
        
    def add(self):
        print('C add enter')
        super().add()
        print('C add exit')

class E(A):
    def __init__(self):
        print("E enter")
        super().__init__()
        print("E exit")
        
    def add(self):
        print('E add enter')
        super().add()
        print('E add exit')

class D(B, C):
    def __init__(self):
        print("D enter")
        super().__init__()
        print("D exit")
        
    def add(self):
        print('D add enter')
        super().add()
        print('D add exit')

print(D.__mro__)  
d = D()
d.add()

