import re
print 111
if __name__ == "__main__":
    re.search(r'JRS',"I love JRS!")
    jrs = re.search(r'(([01]{0,1}\d{0,1}\d|2[0,4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0,4]\d|25[0-5])','192.168.25.6')
    print jrs
