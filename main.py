import machine
import utime
import time

led_pin = machine.Pin(25, machine.Pin.OUT)
vib_pin = machine.Pin(2, machine.Pin.OUT)
ldr_pin = machine.ADC(26)  # Create an ADC object on ADC0 (GP26)
#vib1_pin = machine.Pin(2, machine.Pin.OUT)
# SIM800L module UART connection setup
uart = machine.UART(1, baudrate=9600, tx=machine.Pin(8), rx=machine.Pin(9))
help_btn = machine.Pin(22, machine.Pin.IN)
help_btn.init(machine.Pin.IN, machine.Pin.PULL_UP)
trig_pins = [machine.Pin(pin, machine.Pin.OUT) for pin in [19, 20, 21]]
echo_pins = [machine.Pin(pin, machine.Pin.IN) for pin in [16, 17, 18]]
sensor1_val = 0
sensor2_val = 0
sensor3_val = 0
#*****************************************************************************************
def measure_distance(trig_pin, echo_pin):
    trig_pin.value(0)
    utime.sleep_us(2)
    trig_pin.value(1)
    utime.sleep_us(5)
    trig_pin.value(0)
    while echo_pin.value() == 0:
        pass
    pulse_start = utime.ticks_us()
    while echo_pin.value() == 1:
        pass
    pulse_end = utime.ticks_us()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 0.0343 / 2
    return distance


# ..............................................................................................
#....................................................................
light_value = ldr_pin.read_u16()  # Read the analog value from ADC
print(light_value)  # Display the light intensity value

if light_value > 11000:
    vib_pin.value(0)
    time.sleep(1) 
    for _ in range(6):
        vib_pin.value(0)
        time.sleep(0.2)
        vib_pin.value(1)
        time.sleep(0.1)
#.............................................................................
led_pin.value(1)
time.sleep(0.6)
led_pin.value(0)
vib_pin.value(1)
callv = 1
safe_distance = 30
safe_distance2 = 80
light_executed = False  # Flag to indicate if the light code has been executed
while True:
    light_value = ldr_pin.read_u16()  # Read the analog value from ADC
    print(light_value)  # Display the light intensity value
    distances = []
    for i in range(3):
      distance = measure_distance(trig_pins[i], echo_pins[i])
        distances.append(distance)
        if i == 0:
            sensor1_val = distance
        elif i == 1:
            sensor2_val = distance
        elif i == 2:
            sensor3_val = distance
        #print("Distance {}: {:.2f} cm".format(i+1, distance)) 
    print("Average Distance: {:.2f} cm".format(sum(distances) / len(distances)))
    print("Sensor 1 value:", sensor1_val)
    print("Sensor 2 value:", sensor2_val)
    print("Sensor 3 value:", sensor3_val)
    print("")  
    if sensor1_val < safe_distance and sensor2_val < safe_distance and sensor3_val < safe_distance: # LEFT, RIGHT, and UP
        vib_pin.value(0)
        time.sleep(2)
        vib_pin.value(1)       
    elif sensor1_val < safe_distance and sensor3_val < safe_distance: # UP and RIGHT
        for _ in range(6):
            vib_pin.value(0)
            time.sleep(0.1)
            vib_pin.value(1)
            time.sleep(0.1)          
    elif sensor1_val < safe_distance and sensor2_val < safe_distance: # UP and LEFT
        for _ in range(4):
            vib_pin.value(0)
            time.sleep(0.1)
            vib_pin.value(1)
            time.sleep(0.1)  
    elif sensor2_val < safe_distance and sensor3_val < safe_distance: # LEFT and RIGHT
        for _ in range(8):
            vib_pin.value(0)
            time.sleep(0.1)
            vib_pin.value(1)
            time.sleep(0.1)  
    elif sensor1_val < safe_distance2: # UP
        for _ in range(3):
            vib_pin.value(0)
            time.sleep(0.1)
            vib_pin.value(1)
            time.sleep(0.1) 
    elif sensor2_val < safe_distance: # LEFT
        for _ in range(2):
            vib_pin.value(0)
            time.sleep(0.1)
            vib_pin.value(1)
            time.sleep(0.1)
    elif sensor3_val < safe_distance: # RIGHT
        vib_pin.value(0)
        time.sleep(0.1)
        vib_pin.value(1)
    else:
        vib_pin.value(1)
        
        
    
    if help_btn.value() == 0: #FOR MAKING A CALL
        if callv == 1:
            callv = 0
            vib_pin.value(0)
            time.sleep(0.3)
            vib_pin.value(1)        
            phone_number = "0745595889"
            message = ("HELP ME, LOCATION: https://www.google.com/maps/@-0.7161091,37.1469624,17z?authuser=0&entry=ttu")        
            try:
                uart.write("AT\r\n")
                time.sleep(1)
                uart.write("AT+CMGF=1\r\n")  # Set SMS mode to text
                time.sleep(1)
                uart.write('AT+CMGS="{}"\r\n'.format(phone_number))
                time.sleep(1)
                uart.write(message)
                time.sleep(1)
                uart.write(chr(26))  # Send Ctrl+Z to end the message
                time.sleep(1)
                print("SMS sent")
            except Exception as e:
                print("Error:", str(e))
                time.sleep(0.2)
            print("SMS sent")           
            callv = 1
        
            vib_pin.value(0)
            time.sleep(0.3)
            vib_pin.value(1)    
     # Checking light value and controlling vibration accordingly
    if light_value < 10000 and not light_executed:  # Execute only if light value is below 10000 and light code hasn't been executed yet
        vib_pin.value(0)
        time.sleep(1)        
        for _ in range(4):
            vib_pin.value(0)
            time.sleep(0.2)
            vib_pin.value(1)
            time.sleep(0.1)      
        light_executed = True  # Set flag to True after executing the code        
    elif light_value > 11000 and light_executed:  # Reset flag when light value goes above 11000
        light_executed = False       
        vib_pin.value(0)
        time.sleep(1)       
        for _ in range(6):
            vib_pin.value(0)
            time.sleep(0.2)
            vib_pin.value(1)
            time.sleep(0.1)                       
    vib_pin.value(1)
    time.sleep(0.5)  # Time to wait before checking for the obstacle
