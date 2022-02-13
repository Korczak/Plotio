
import serial

arduino = serial.Serial(port="COM4", baudrate=115200, timeout=0.1)

for i in range(0, 100):
	text = f"KOMENDA,{i},0,1".encode()
	arduino.write(text)
	
	reading = True
	while(reading):
		response = arduino.readline().decode()
		print(f"RESPONSE: {response}")
		if response != None:
			processed_response = response.split(",")
			if len(processed_response) > 0:
				is_done = bool(int(processed_response[1]))
				if is_done:
					reading = False