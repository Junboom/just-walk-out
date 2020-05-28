import serial


#시리얼 통신 설정
port ="COM15"
brate = 9600
arduino =serial.Serial(port, baudrate = brate, timeout=None)



while True:
    #아두이노로부터 데이터를 계속 받아옴
    data= arduino.readline()

    # 아두이노에서 \n\r 을 보내는데 그거를 지워주려고 하는거임
    # a= 1,0 을 받아옴( 사람이 들어왔는지 안들어왔는지 들어오면 a=1 안들어오면 a=0)
    #str = data[:-2].decode()
    #print(str)
    #a= int(str)

    b=arduino.readline()[:-2].decode()
    b=b[:1]
    print(b)
    if b=="2":
        print("b=2야")

    c=b=arduino.readline()[:-2].decode()
    c = c[:1]
    print(c)
    if c=="4":
        print("c=4야")
