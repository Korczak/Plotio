
import serial

arduino = serial.Serial(port="COM6", baudrate=115200, timeout=0.1)

for i in range(0, 100):
	text = f"KOMENDA,{i},0,1".encode()
	arduino.write(text)
	
	reading = True
	while(reading):
		response = arduino.readline().decode()
		if response != None:
			processed_response = response.split(",")
			is_done = bool(int(processed_response[1]))
			if is_done:
				reading = False