import time
import spidev

KEY1 = 0xAA # key used in critical commands
KEY2 = 0x55 # key used in critical commands
BRAKE_TORQUE = 100
OFF = 0
ON = 1
AN0 = 0
AN1 = 1
AN2 = 2
AN3 = 3
AN4 = 4
AN5 = 5
AN6 = 6
AN7 = 7


COMMAND_FIRMWARE =        0xFE #Read firmware value (integer value)
COMMAND_LED  =            0xFD #Debug LED
COMMAND_SERVO1 =          0xFC #Move Servo1
COMMAND_SERVO2 =          0xFB #Move Servo2
COMMAND_LCD_L1 =          0xFA #Write LCD line1
COMMAND_LCD_L2 =          0xF9 #Write LCD line2
COMMAND_IR_EMITTERS =     0xF8 #IR Emmiters ON/OFF
COMMAND_STOP =            0xF7 #Stop motors freeley
COMMAND_MOVE =            0xF6 #Move motors with no PID control
COMMAND_BRAKE =           0xF5 #Stop motors with brake torque
COMMAND_BAT_MIN =         0xF4 #Configure low battery level
COMMAND_MOVE_PID =		0xF3 #Move motor with PID control
COMMAND_CALIBRATE =		0xF2 #Calibrate motors
COMMAND_PID_CFG =         0xF1 #Configure kp, ki and kd PID control values
COMMAND_ENCL_RESET =		0xF0 #Preset the value of encoder1
COMMAND_ENCR_RESET =      0xEF #Preset the value of encoder2
COMMAND_ENC_SAVE =        0xEE #Save encoders position
COMMAND_RAMP_CFG =        0xED #Configure acceleration ramp parameters
COMMAND_MOV_DIF_SI =      0xEC #Move motors with SI units system
COMMAND_DIF_SI_CFG =      0xEB #Configure SI movement parameters
COMMAND_MOVE_1M =         0xEA #Move 1 motor with no PID control
COMMAND_STOP_1M =         0xE9 #Stop 1 motor
COMMAND_BRAKE_1M =        0xE8 #Brake 1 motor

#Read Commands-> requests to Bot'n Roll ONE 
COMMAND_ADC0 =            0xDF #Read ADC0
COMMAND_ADC1 =            0xDE #Read ADC1
COMMAND_ADC2 =            0xDD #Read ADC2
COMMAND_ADC3 =            0xDC #Read ADC3
COMMAND_ADC4 =            0xDB #Read ADC4
COMMAND_ADC5 =            0xDA #Read ADC5
COMMAND_ADC6 =            0xD9 #Read ADC6
COMMAND_ADC7 =            0xD8 #Read ADC7
COMMAND_BAT_READ =		0xD7 #Read ADC battery
COMMAND_BUT_READ =		0xD6 #Read ADC button
COMMAND_OBSTACLES =       0xD5 #Read IR obstacle sensors
COMMAND_IR_SENSORS =      0xD4 #Read IR sensors instant value
COMMAND_ENCL =            0xD3 #Read Encoder1 position
COMMAND_ENCR =            0xD2 #Read Encoder2 position
COMMAND_ENCL_INC =		0xD1 #Read Encoder1 Incremental value
COMMAND_ENCR_INC =		0xD0 #Read Encoder2 Incremental value
#COMMAND_LINE_READ	0xCF #Read Line Value (0-8000)


#Read Commands-> Computer to Bot'n Roll ONE A
COMMAND_ARDUINO_ANA0 =	0xBF #Read analog0 value
COMMAND_ARDUINO_ANA1 =	0xBE #Read analog1 value
COMMAND_ARDUINO_ANA2 =	0xBD #Read analog2 value
COMMAND_ARDUINO_ANA3 =	0xBC #Read analog3 value
COMMAND_ARDUINO_DIG0 =	0xBB #Read digital0 value
COMMAND_ARDUINO_DIG1 =	0xBA #Read digital1 value
#COMMAND_ARDUINO_DIG2	0xB9 #Read digital2 value
COMMAND_ARDUINO_DIG3 =	0xB8 #Read digital3 value
COMMAND_ARDUINO_DIG4 =	0xB7 #Read digital4 value
COMMAND_ARDUINO_DIG5 =	0xB6 #Read digital5 value
COMMAND_ARDUINO_DIG6 =	0xB5 #Read digital6 value
COMMAND_ARDUINO_DIG7 =	0xB4 #Read digital7 value
COMMAND_ARDUINO_DIG8 =	0xB3 #Read digital8 value
COMMAND_ARDUINO_DIG9 =	0xB2 #Read digital9 value
COMMAND_ARDUINO_DIG10 =	0xB1 #Read digital10 value
COMMAND_ARDUINO_DIG11 =	0xB0 #Read digital11 value
COMMAND_ARDUINO_DIG12 =	0xAF #Read digital12 value
COMMAND_ARDUINO_DIG13 =	0xAE #Read digital13 value
COMMAND_ARDUINO_BUZ =     0xAD #Read Buzzer
COMMAND_ARDUINO_CMP =     0xAC #Read Compass
COMMAND_ARDUINO_SNR =     0xAB #Read Sonar
COMMAND_ARDUINO_GRP1 =    0xAA #Read gripper1
COMMAND_ARDUINO_GRP2 =    0x9F #Read gripper2

spi = spidev.SpiDev()

def begin():
    bus = 0
    device = 0
    spi.open(bus, device)
    spi.max_speed_hz = 500000
    spi.mode = 1
    print('BnrOneA Begin')
    
def spiRequestWord(comand):
    msg = [comand]
    msg.append(KEY1)
    msg.append(KEY2)
    spi.xfer2(msg)
    time.sleep(60/1000000.0)
    byte1 = spi.readbytes(1)
    time.sleep(60/1000000.0)
    byte2 = spi.readbytes(1)
    i = 0
    i = byte1[0]
    i = i << 8
    i = i+byte2[0]
    return i

def spiRequestByte(comand):
    msg = [comand]
    msg.append(KEY1)
    msg.append(KEY2)
    spi.xfer2(msg)
    time.sleep(60/1000000.0)
    byte1 = spi.readbytes(1)
    return byte1[0]
    
def led(state):
    msg = [COMMAND_LED]
    msg.append(KEY1)
    msg.append(KEY2)
    msg.append(state)
    result = spi.xfer2(msg)
    
def move(left,right):
    msg = [COMMAND_MOVE]
    msg.append(KEY1)
    msg.append(KEY2)
    speedL_H = left & 0xff
    speedL_L = (left & 0xff00) >> 8
    speedR_H = right & 0xff
    speedR_L = (right & 0xff00) >> 8
    msg.append(speedL_H)
    msg.append(speedL_L)
    msg.append(speedR_H)
    msg.append(speedR_L)
    result = spi.xfer2(msg)
    
def stop():
    msg = [COMMAND_STOP]
    msg.append(KEY1)
    msg.append(KEY2)
    result = spi.xfer2(msg)
    
def brake(torqueL,torqueR):
    msg = [COMMAND_BRAKE]
    msg.append(KEY1)
    msg.append(KEY2)
    msg.append(torqueL)
    msg.append(torqueR)
    result = spi.xfer2(msg)
    
def obstacleEmitters(state):
    msg = [COMMAND_IR_EMITTERS]
    msg.append(KEY1)
    msg.append(KEY2)
    msg.append(state)
    result = spi.xfer2(msg)
    
def readButton():
    result = spiRequestWord(COMMAND_BUT_READ)
    if (result>=0 and result<250):
       return 1
    elif (result>=250 and result<620):
       return 2
    elif (result>=620 and result<950):
       return 3
    else:
        return 0

def readBattery():
    result = spiRequestWord(COMMAND_BAT_READ)
    return (result/50.7)

def readFirmware():
    msg = [COMMAND_FIRMWARE]
    msg.append(KEY1)
    msg.append(KEY2)
    spi.xfer2(msg)
    time.sleep(60/1000000.0)
    byte1 = spi.readbytes(1)
    time.sleep(60/1000000.0)
    byte2 = spi.readbytes(1)
    time.sleep(60/1000000.0)
    byte3 = spi.readbytes(1)
    string = ""
    string += str(byte1[0])
    string += "."
    string += str(byte2[0])
    string += "."
    string += str(byte3[0])
    return string

def obstacleSensors():
    return spiRequestByte(COMMAND_OBSTACLES)
