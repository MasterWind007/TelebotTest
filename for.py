
buttons=[1,2,3,4,5,6,7,8,9,0]
cols = 4
bb=[buttons[i:i+cols] for i in range(0, len(buttons), cols) ]
print(bb)