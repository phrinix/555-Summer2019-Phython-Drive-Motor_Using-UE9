# 555-Summer2019-Phython-Drive-Motor_Using-UE9
# Python
With learning, research and coding, this project was completed in 6 hrs. Before this I wasn't having any experience of Phython.

# About Project

Purpose - Control the motor's Speed and Direction

Descrption - To control a motor direction and speed using LabJack UE9. We use FIO0 which is connected to enable pin
             to control the speed of motor. We use FIO1 and FIO3 to change direction of motor. We also check for the 
             on-board push buttons through FIO5 and FIO7 check are for reset and stop respectively.
Program Working - We start program with initializing the GUI with use of Tkinter. At start, only IP Address Connect
                  Button us functional and all other are non-functional. Once we established correct connection,
                  Start and Stop button gets functional. Motor can be stopped with stop button if it was running
                  previously. However to start it you need to enter correct password in password box. Once right password
                  is enterd and start is pressed, motor will start with default settings which are ClockWise and 50% duty cycle.
                  Now all buttons are functional. When reset is pressed it will come back to default settings. ClockWise and
                  CounterClockWise Button change the direction of motor and Slider changes the speed of motor. If stop button
                  is pressed, it will make all button non-functional other then IP Address Connect and Start button. To start
                  again you need to enter correct password again.

