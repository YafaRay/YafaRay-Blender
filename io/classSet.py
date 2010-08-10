#!/usr/bin/env python

class DemoClass:
    pass
    
l = ["orthographic", "perspective", "architecture", "angular"]
for t in l:
    setattr(_type, t, t)

a = DemoClass()
print(DemoClass.angular + " " + DemoClass.orthographic)