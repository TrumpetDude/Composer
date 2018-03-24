from random import randint

'''
0=rest/end note
1=start/change note
2=continue note
'''


r=0
iterations = 64
rhythm = ""
for subdivision in range(0,iterations):
    if r==0:
        r=[0,1,1,1][randint(0,3)]
    else:
        r=[0,1,2,2,2][randint(0,4)]
    rhythm = rhythm+str(r)
print(rhythm)

