conn = [1,2,4,5,1,4,5,5,5,1,2,3,4,1,1,1,1,1,2,3,4]
conn_len = len(conn)
index = 0

chop = []

start = 0
steps = 10

for i in range(steps):
    #print(conn[start])
    chop.append(conn[start])
    start = (start + 1) % conn_len

print(chop)

def checkList(the_list, minimum, maximum, chunk):
    for i in range(len(the_list)-1):
        if the_list[i] >= minimum and the_list[i] <= maximum:
            hits = 1
            for j in range(1,chunk):
                ite = i+j
                try:
                    if the_list[ite] >= minimum and the_list[ite] <= maximum:
                        hits +=1
                    if hits == chunk:
                        print("equal at:", i)
                        return True
                
                except IndexError:
                    print("shits happends")
                    return False
    return False  #Do not think it will ever get passed the other returns      


print(range(1,3))     
state = checkList(chop, 5,5,2)
print(state)
