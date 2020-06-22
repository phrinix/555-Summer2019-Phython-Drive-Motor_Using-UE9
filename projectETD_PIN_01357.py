"""
Purpose - Control the motor

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
"""

# IMPORT tkiner module
from tkinter import *
"import ue9"
"import LabJackPython"
# Global Variable
PASSWORD = "111"
HEIGHT = 400
WIDTH = 600
# GUI to control motor
class control_system:
    start_check = 0                                     # Default Direction: cw=0, ccw=1
    d_speed = 10000                                     # Default Speed
    speed = d_speed                                     # Initial Speed is Default Speed
    d_direction = 0                                     # Default Direction: cw=0, ccw=1
    fio_mask = 0b10101011
    fio_dir = 0b00001011
    fio_state = 0b00000000
    # Set up GUI frame, buttons, lables, TextBox(Entry), etc.
    def __init__(self, master):
        master.title("Motor Control System")          # Title for form
        canvas = Canvas(master, height=HEIGHT,width=WIDTH)      # Set up Form Size
        canvas.pack();
        master.resizable(False,False)                 # Doesn't allow to change size of GUI
        # relx is distrance from left wall, rely is distance from top wall (1.0 = 100%)
        frame = Frame(master)                           # Set up the frame to work in
        frame.place(relx=0.05, rely=0.05, relwidth=0.9,relheight=1)
       
        self.headingL = Label(frame, text="Motor Control System", fg="blue", font = ("",20))
        self.headingL.place(relx=0, rely=0, relwidth=1,relheight=0.08)
        self.ipL= Label(frame, text = "Enter IP address")
        self.ipL.place(relx=0, rely=0.1, relwidth=0.2,relheight=0.05)
        self.ipaddressE = Entry(frame)
        self.ipaddressE.place(relx=0.02, rely=0.15, relwidth=0.2,relheight=0.05)
        self.connectBT = Button(frame, text="Connect", command = self.ip_address_connect)
        self.connectBT.place(relx=0.04, rely=0.22, relwidth=0.14,relheight=0.05)
        self.ipwarnL = Label(frame,text="")
        self.ipwarnL.place(relx=0.23, rely=0.15, relwidth=0.3,relheight=0.05)
        
        self.passInfoL = Label(frame, text="Enter password and press start")
        self.passInfoL.place(relx=0.02, rely=0.4, relwidth=0.3,relheight=0.05)
        self.passPutE = Entry(frame)
        self.passPutE.place(relx=0.02, rely=0.45, relwidth=0.3,relheight=0.05)
        self.passStatusL = Label(frame, text="")
        self.passStatusL.place(relx=0.23, rely=0.45, relwidth=0.52,relheight=0.05)
        self.startBT = Button(frame, text="Start",bg="green",fg="white")
        self.startBT.place(relx=0.02, rely=0.5, relwidth=0.2,relheight=0.1)
        self.stopBT = Button(frame, text="Stop",bg="red",fg="white")
        self.stopBT.place(relx=0.02, rely=0.6, relwidth=0.2,relheight=0.1)
            
        self.fastslowL = Label(frame, text="FAST                                                   SLOW")
        self.fastslowL.place(relx=0.6, rely=0.12, relwidth=0.4,relheight=0.02)
        self.slider = Scale(frame, from_=52000, to=10000, orient=HORIZONTAL, showvalue=0)
        self.slider.place(relx=0.6, rely=0.16, relwidth=0.4,relheight=0.1)
        self.cwBT = Button(frame, text="ClockWise")
        self.cwBT.place(relx=0.6, rely=0.3, relwidth=0.2,relheight=0.1)
        self.ccwBT = Button(frame, text="Counter ClockWise")
        self.ccwBT.place(relx=0.8, rely=0.3, relwidth=0.2,relheight=0.1)
                    
        self.resetBT = Button(frame, text="Reset",bg="blue",fg="white")
        self.resetBT.place(relx=0.8, rely=0.5, relwidth=0.2,relheight=0.1)
        self.setdefaultBT = Button(frame, text="Set as default")
        self.setdefaultBT.place(relx=0.8, rely=0.6, relwidth=0.2,relheight=0.1)
        self.quittBT = Button(frame, text="Quit",bg="grey", command = self.q)
        self.quittBT.place(relx=0.4, rely=0.7, relwidth=0.2,relheight=0.1)
        
    
    def ip_address_connect(self):               # Make the connection
        try:
            
            ip_address = self.ipaddressE.get()
            if ip_address == "":
                ip_address = "NOPE"
#           self.myUE9 = ue9.UE9(ethernet = True, ipAddress = ip_address)
            self.ipwarnL.configure(text="Connected", fg="green")
            self.startBT.configure(command = self.start_security)
            self.stopBT.configure(command = self.stop_pressed)
            self.stopBT.after(100,self.check_estop)
            self.start_check = 1
            
        except:
            self.ipwarnL.configure(text="Wrong IP Address! Try again!", fg="red")
            self.passStatusL.configure(text="IP Address Lost !! Connect Again", fg="red")
            self.startBT.configure(command = self.empty)
            self.cwBT.configure(command = self.empty)
            self.ccwBT.configure(command = self.empty)
            self.slider.configure(command = self.empty2)
            self.resetBT.configure(command = self.empty)
            self.setdefaultBT.configure(command = self.empty)
            self.stopBT.configure(command = self.empty)
     
    def start_security(self):                   # Checks for password and start
        if self.passPutE.get() == PASSWORD:
            self.passStatusL.configure(text="Working", fg="Green")
            self.passPutE.delete(0,END)
            self.cwBT.configure(command = self.cw_pressed)
            self.ccwBT.configure(command = self.ccw_pressed)
            self.slider.configure(command = self.speed_changed)
            self.resetBT.configure(command = self.reset_pressed)
            self.setdefaultBT.configure(command = self.set_default)
            self.slider.set(self.speed)
            if self.d_direction == 0:
                self.cw_pressed();
            else:
                self.ccw_pressed();
            self.start_check = 1
            
        else:
            self.passStatusL.configure(text="Wrong password! Try again!", fg="red")   
            self.passPutE.delete(0,END)


    def stop_pressed(self):                     # Emergence Stop 
#        self.fio_state = 0b00000000
        self.passStatusL.configure(text="!! EMERGENCY BUTTON PRESSED !! Enter Password !", fg="red")
        self.cwBT.configure(command = self.empty,bg="#f0f0ed",fg="black")
        self.ccwBT.configure(command = self.empty,bg="#f0f0ed",fg="black")
        self.slider.configure(command = self.empty2)
        self.resetBT.configure(command = self.empty)
        self.setdefaultBT.configure(command = self.empty)
        self.init_motor()
        self.start_check = 0
       
        
    def speed_changed(self,var):                    # Change speed
        self.speed = var
        self.init_motor()
        
       
    def cw_pressed(self):                           # Turns Clock Wise
        self.cwBT.configure(bg="#63B624",fg="white")
        self.ccwBT.configure(bg="#f0f0ed",fg="black")
        self.fio_state = 0b00000011
        self.init_motor()
    def ccw_pressed(self):                          # Turns Counter-Clock Wise
        self.cwBT.configure(bg="#f0f0ed",fg="black")
        self.ccwBT.configure(bg="#63B624",fg="white")
        self.fio_state = 0b00001001
        self.init_motor()
    def set_default(self):                          # Set default Settings
        self.d_speed = self.speed
        if self.fio_state == 0b00000011:
            self.d_direction = 0
        else:
            self.d_direction = 1
        
        
    def reset_pressed(self):                        # Reset to default Settings
        self.slider.set(self.d_speed)
        self.speed = self.d_speed
        if self.d_direction == 0:
           self.cw_pressed();
        else:
           self.ccw_pressed();
        
    def empty(self):
        pass
    def empty2(self,var):
        pass
    def q(self):                                    # Stop the motor when program quits
       
        self.fio_state = 0b00000000
        self.init_motor()
        form.destroy()
    # Sends and Updates the data to LabJack 
    def init_motor(self):
        self.myUE9.timerCounter(TimerClockBase=1, TimerClockDivisor=1,Timer0Mode = 0, NumTimersEnabled = 1, UpdateConfig = 1, Timer0Value = int(self.speed))
        self.results = self.myUE9.feedback(FIOMask = self.fio_mask, FIODir = self.fio_dir, FIOState = self.fio_state)
    def check_estop(self):                              # Checks for the Physical Reset and Stop Button
        self.init_motor()
        if(self.start_check == 1):
            if (self.results["FIOState"] & 0b00100000) == 0b00100000:
                self.stop_pressed()    
            if (self.results["FIOState"] & 0b10000000) == 0b10000000:
                self.reset_pressed() 
        self.stopBT.after(100,self.check_estop)



form = Tk();                                # Create instance named form
a = control_system(form)
form.mainloop()                             # Makes GUI in loop running
a.q()                                       # Stop the motor when program quits
