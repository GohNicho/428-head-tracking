Connecting 2 Bluetooth Shield with Serial Terminal

1) Set the SoftwareSerial pins to BT_TX: 6 BT_RX: 77
2) Upload the HC05_Bluetooth_Master.ino onto 1 of the Arduino
3) Upload the HC_Bluetooth_Slave.ino onto the other Arduino
4) Download and open the 2 serperate Serial Terminal
5) Change the settings on both Serial Terminal to BaudRate: 38400, DataBit: 8, StopBit: 1, Verify: N
6) Change the ComNum on the 1st Serial Terminal to the 1st Arduino COMPort
7) Change the ComNum on the 2nd Serial Terminal to the 2nd Arduino COMPort
8) The red & green LED on the module will flash in intervals indicting that they are inquiring for each other
9) After a while only the green LED will flash in 1sec intervals indicating that they are connected
10) The connection is successful now, and you can type any character on the Serial Terminal which will than send to the other Serial Terminal
