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
        print("A")
        super().__init__()
        self.n = 2

    def add(self, m):
        print('self is {0} @A.add'.format(self))
        self.n += m

class B(A):
    def __init__(self):
        print("B")
        # super().__init__()
        self.n = 3

    def add(self, m):
        print('self is {0} @B.add'.format(self))
        super().add(m)
        self.n += 3

class C(A):
    def __init__(self):
        print("C")
        # super().__init__()
        self.n = 4

    def add(self, m):
        print('self is {0} @C.add'.format(self))
        super().add(m)
        self.n += 4

class D(B, C):
    def __init__(self):
        print("D")
        super().__init__()
        self.n = 5

    def add(self, m):
        print('self is {0} @D.add'.format(self))
        super().add(m)
        self.n += 5

d = D()
d.add(2)
print(d.n)
print(D.__mro__)    
