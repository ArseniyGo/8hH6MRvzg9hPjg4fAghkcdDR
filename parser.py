op = open('msg.txt', 'w')
op.write('0')
op.close()
print(open('msg.txt', 'r').readline().split())
