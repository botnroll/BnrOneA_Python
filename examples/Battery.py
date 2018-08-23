import time
import BnrOneA

BnrOneA.begin() #Begin BnrOneA SPI comunication

while 1:
    rsp = BnrOneA.readBattery() #Request battery value from BnrOneA Robot
    print(rsp)
    time.sleep(1)
    

