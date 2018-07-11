import random as r

class Fish(object):
    def __init__(self):
        self.x = r.randint(0,10)
        self.y = r.randint(0,10)
    
    def move(self):
        self.x -= 1
        print "Now I'm at %d,%d" % (self.x,self.y)

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
