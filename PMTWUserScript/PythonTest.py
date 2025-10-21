"""PythonTest.py
"""

def multiply(a,b):
    print("Will compute", a, " * ", b)
    c = a * b
    return c
    

if __name__ == '__main__':
    # 获取用户输入
    a = int(input("请输入 a 的值: "))
    b = int(input("请输入 b 的值: "))    
    c = multiply(a, b)
    print(f"{a} multiply {b} is {c}")