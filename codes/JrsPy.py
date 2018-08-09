# -*- coding: utf-8 -*-
import random as r
import time as t

class Fish(object):
    def __init__(self):
        self.x = r.randint(0,10)
        self.y = r.randint(0,10)
    
    def move(self):
        self.x -= 1
        print "Now I'm at %d,%d" % (self.x,self.y)
    
    def __call__(self,name):
        print "my name is ",name

class Shark(Fish):
    def __init__(self):
        #Fish.__init__(self)
        #super().__init__() #3.x
        super(Shark,self).__init__()
        self.hungry = True
    
    def eat(self):
        if self.hungry:
            print "happy to eat!"
            self.hungry = False
        else:
            print "no more food!"
class Base:
    num = 0
    def __init__(self):
        self.count = 0
    def getCount(self):
        return self.count
    def setCount(self,a):
        self.count = a
    def delCount(self):
        del self.count
    x = property(getCount,setCount,delCount)

#__new__
class CapStr(str):
    def __new__(cls,string):
        string = string.upper()
        return str.__new__(cls,string)

class New_int(int):
    def __add__(self,other):
        return int.__sub__(self,other)
    def __sub__(self,other):
        return int.__add__(self,other)

class MyTimer:
    def __init__(self):
        self.start = 0
        self.stop =0
        self.lasted = []
        self.prompt = "计时未开始！"
        self.unit = ["年","月","日","小时","分钟","秒"]
    
    def __str__(self):
        return self.prompt
    
    __repr__ = __str__

    def begin(self):
        self.start = t.localtime()
        print "计时开始！"
    
    def end(self):
        self.stop = t.localtime()
        print "计时结束！"
        self._calc()

    def _calc(self):
        self.lasted = []
        self.prompt = "总共运行了"
        for index in range(6):
            self.lasted.append(self.stop[index]-self.start[index])
            if self.lasted[index]:
                self.prompt +=(str(self.lasted[index]+self.unit[index]))

def JrsSo(call_back = None):
    links = []
    if call_back:
        links.extend(call_back("jrs") or [])
    print links

if __name__ == '__main__':
    shark = Shark()
    shark.eat()
    shark.eat()
    shark.move()
    shark.move()
    print issubclass(Shark,Fish),isinstance(shark,Shark),hasattr(shark,'hungry'),getattr(shark,'qq','no such thing!')
    a = Base()
    c = Base()
    c.count = 10
    c.num = 10
    Base.count = 100
    Base.num = 100
    print a.count,a.num
    print c.count,c.num
    bb = Base()
    print bb.x
    bb.x = 2
    print bb.x

    a = CapStr("I love you!")
    print a

    a = New_int(3)
    b = New_int(5)
    print a-b

    JrsSo(call_back=Fish())
