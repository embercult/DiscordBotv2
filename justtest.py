import time

old = time.time()

while True:
    time.sleep(5)
    print(time.time() - old)
    if time.time() - old > 10:
        print(time.time() - old)
        print ("passed")