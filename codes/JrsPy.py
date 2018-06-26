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

if __name__ == '__main__':
    shark = Shark()
    shark.eat()
    shark.eat()
    shark.move()
    shark.move()
