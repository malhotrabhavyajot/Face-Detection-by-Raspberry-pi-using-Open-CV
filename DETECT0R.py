
for i in range(25):
	print("COULD NOT CONNECT TO RPi  eth0 (0x33FF)")
	print("Retrying("+str(i)+")")		
	j=0
	while(j<15000000):
		j+=1
