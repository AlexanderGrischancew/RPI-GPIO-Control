import tkinter
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from sys import *
import time

OS = sys.platform #Current O.S.

#------if OS is Linux--------
if "w" not in OS:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
#----------------------------


#-----Paths for Linux--------
if "w" not in OS:
    Configspath = "/home/pi/GPIO/Configs.txt"
    picture1path = "/home/pi/GPIO/RPI.gif"
    picture2path = "/home/pi/GPIO/Pulse.gif"
#----------------------------

#-----Paths for Windows--------
if "w" in OS:
    Configspath = "Configs.txt"
    picture1path = "RPI.gif"
    picture2path = "Pulse.gif"
#------------------------------


#------------------------globals/konstants----------------
global StateList#List with states (0/1 [off/on])
StateList = list(("0"*28))

global Blacklist #List with pins that are expertmode only
Blacklist = list("2387901")
Blacklist.append("14")
Blacklist.append("15")
Blacklist.append("10")
Blacklist.append("11")

version = "Version: 1.8" #Displayed Version
#--------------------------------------------------------

#------------------------Button operations-----------------------
def ChangeStateOff(OldButton,Oldtext,Oldrow,Oldcolumn,GPIOSET,COLOUR):
    OldButton.destroy()
    OldButton = Button(fenster, width=11, bg=COLOUR, text=Oldtext, command=lambda:ChangeStateOn(OldButton,Oldtext,Oldrow,Oldcolumn,GPIOSET,COLOUR))
    OldButton.grid(row=Oldrow, column=Oldcolumn, padx=20,pady=1)
    GPIO.output(GPIOSET,False)
    StateList[GPIOSET] = "0" 


def ChangeStateOn(OldButton,Oldtext,Oldrow,Oldcolumn,GPIOSET,COLOUR):
    if str(GPIOSET) in Blacklist:
        Configurations = open(Configspath, "r")
        while 1:
            Line = Configurations.readline()
            if Line == "":
                break
            if Line[0] == '#':
                continue

            if Line[0] == "3":
                if Line[2] == "Y":
                    break
                if Line[2] == "N":
                    messagebox.showerror(title="Error",message="Pin "+Oldtext+" is a special Pin\n to controll you have to enable Expert Mode in Options")
                    return
            else:
                continue
        Configurations.close()
        
    OldButton.destroy()
    OldButton = Button(fenster, width=11, bg="orange", text=Oldtext, command=lambda:ChangeStateOff(OldButton,Oldtext,Oldrow,Oldcolumn,GPIOSET,COLOUR))
    OldButton.grid(row=Oldrow, column=Oldcolumn, padx=20,pady=1)
    GPIO.setup(GPIOSET, GPIO.OUT)
    GPIO.output(GPIOSET,True)
    StateList[GPIOSET] = "1"
    

def Pulse(GPIOID):
    if str(GPIOID) in Blacklist:
        Configurations = open(Configspath, "r")
        while 1:
            Line = Configurations.readline()
            if Line == "":
                break
            if Line[0] == '#':
                continue

            if Line[0] == "3":
                if Line[2] == "Y":
                    break
                if Line[2] == "N":
                    messagebox.showerror(title="Error",message="Pin "+str(GPIOID)+" is a special Pin\n to controll you have to enable Expert Mode in Options")
                    return
            else:
                continue
        Configurations.close()
        
    GPIO.setup(GPIOID, GPIO.OUT)
    GPIO.output(GPIOID,True)
    time.sleep(0.1)
    GPIO.output(GPIOID,False)
#----------------------------------------------------------------    


#---------------------------File operations----------------------
def SaveFile():
    GPIOString = "GPIO States:\n"
    Configurations = open(Configspath, "r")
    while 1:
        Line = Configurations.readline()
        if Line == "":
            break
        if Line[0] == '#':
            continue

        if Line[0] == "3":
            if Line[2] == "Y":
                GPIOString = GPIOString + "EXPERT\n"
            if Line[2] == "N":
                GPIOString = GPIOString + "NORMAL\n"
            break
    GPIOString = GPIOString + ">"+str(StateList).replace("'","").replace(" ","").replace("[","").replace("]","")
    SaveFile = filedialog.asksaveasfilename()
    File = open(SaveFile, "w")
    File.write(GPIOString)
    File.close()
    

def LoadFile():
    Filename = filedialog.askopenfilename()
    File = open(Filename, "r")
    while 1:
        Line =  File.readline()
        if Line == "":
            break
        if Line[0] == '#':
            continue

        if Line[0] == ">":
            global LoadStateList
            LoadStateList = Line.replace(">","").split(",")
            break
    buttons(True)
#---------------------------------------------------------------
    
    
def Reset(Fenster,NewFenster,clean):
    if clean == "check":
        Configurations = open(Configspath, "r")
        Line = Configurations.readline()
        while Line != "<!End>":
            Line = Configurations.readline()
            if Line == "":
                break
            if Line[0] == '#':
                continue
            if Line[0] == "2":
                if Line[2] == "Y":
                    GPIO.cleanup()
                    print("GPIO.cleanup()")
        Configurations.close()
    if clean == "clean":
        GPIO.cleanup()
        print("GPIO.cleanup()")
        global StateList
        StateList = list(("0"*28))
        buttons(False)
    if Fenster != "NONE":
        Fenster.destroy()
    else:
        NewFenster.attributes('-topmost', 1)

        
#--------------Options menu---------------------------------------
def Save():
    Configurations = open(Configspath, "w")
    Configurations.write("Configs:\n")

    if CleanUpVarAfter.get() == 1:
        CleanUpStringAfter = "2.Yes\n"
    else:
        CleanUpStringAfter = "2.No\n"
    Configurations.write(CleanUpStringAfter)
    
    if  ExpertVar.get() == 1:
         ExpertVarString = "3.Yes\n"
    else:
         ExpertVarString = "3.No\n"
    Configurations.write(ExpertVarString)
    Configurations.close()
    Reset(OptionsFenster,fenster,False)
            
    
def OpenOptions():
    #---------Options Gui---------#
    global OptionsFenster
    OptionsFenster = Toplevel()
    OptionsFenster.attributes('-topmost', 1)
    OptionsFenster.title("GPIO Controll Options")
    OptionsFenster.geometry("250x300")

    Label(OptionsFenster, text="Options:").grid(row=0, column=0)

    global CleanUpVarAfter
    CleanUpVarAfter = IntVar()
    CleanUpCheckAfter = Checkbutton(OptionsFenster, text="AutoCleanUp when exit", variable=CleanUpVarAfter)

    global ExpertVar
    ExpertVar = IntVar()
    ExpertCheck = Checkbutton(OptionsFenster, text="Enable Expert Mode", variable=ExpertVar)
        #---Datei auslesen---#
    Configurations = open(Configspath, "r")
    Line = Configurations.readline()
    while Line != "<!End>":
        Line = Configurations.readline()
        if Line == "":
            break
        if Line[0] == '#':
            continue
        if Line[0] == "1":
            if Line[2] == "Y":
                pass
        if Line[0] == "2":
            if Line[2] == "Y":
                CleanUpCheckAfter.select()
        if Line[0] == "3":
            if Line[2] == "Y":
                ExpertCheck.select()
    Configurations.close()
    #---------------------------#

    CleanUpCheckAfter.grid(row=2,column=1,sticky=W)
    ExpertCheck.grid(row=3,column=1,sticky=W)
    
    buttonSave = Button(OptionsFenster, width=10, text="SAVE", command=Save)
    buttonSave.grid(row=10, column=1,pady=1)

    buttonExit = Button(OptionsFenster, width=10, text="EXIT", command=lambda:Reset(OptionsFenster,fenster,False))
    buttonExit.grid(row=11, column=1,padx=20,pady=1)
    
    #----------------------------#

#----------------------------------------------------------------


#------------------Erstellen des GUI-----------------------------
fenster = Tk()
fenster.title("GPIO Controll")
fenster.geometry("500x800")

FensterMenu = Menu(fenster)
fenster.config(menu=FensterMenu)
FileMenu=Menu(FensterMenu)
FensterMenu.add_cascade(label="Program",menu=FileMenu)
FileMenu.add_command(label="Options",command=OpenOptions)
FileMenu.add_command(label="Exit",command=lambda:Reset(fenster,fenster,"check"))

FilesMenu=Menu(FensterMenu)
FensterMenu.add_cascade(label="Files",menu=FilesMenu)
FilesMenu.add_command(label="Load",command=LoadFile)
FilesMenu.add_command(label="Save",command=SaveFile)

Resetimg = tkinter.PhotoImage(file=picture1path)
buttonReset = tkinter.Button(fenster,image=Resetimg,text="CleanUp",command=lambda:Reset("NONE",fenster,"clean"),compound=TOP,relief=GROOVE)
buttonReset.grid(row=0, column=2)

buttonExit = Button(fenster, width=10, text="EXIT", command=lambda:Reset(fenster,fenster,"check"))
buttonExit.grid(row=21, column=2)

VersionLabel = Label(text=version,fg="blue")
VersionLabel.grid(row=0,column=0,sticky=N)
#----------------------------------------------------------------
  

#---------Buttons Reihe 1---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def buttons(Check):
    button0StandartCol1 = Button(fenster, width=11, bg="Red", text="3.3V", command=DISABLED)
    button0StandartCol1.grid(row=1, column=0, padx=20,pady=1)
    
    button1StandartCol1 = Button(fenster, width=11, bg="light slate blue", text="GPIO2(SDA1)", command=lambda:ChangeStateOn(button1StandartCol1,"GPIO2(SDA1)",2,0,2,"light slate blue"))
    button1StandartCol1.grid(row=2, column=0,pady=1)
    if Check == True:
        if LoadStateList[2] == "1":
            ChangeStateOn(button1StandartCol1,"GPIO2(SDA1)",2,0,2,"light slate blue")

    button2StandartCol1 = Button(fenster, width=11, bg="light slate blue", text="GPIO3(SCL1)", command=lambda:ChangeStateOn(button2StandartCol1,"GPIO3(SCL1)",3,0,3,"light slate blue"))
    button2StandartCol1.grid(row=3, column=0,pady=1)
    if Check == True:
       if LoadStateList[3] == "1":
            ChangeStateOn(button2StandartCol1,"GPIO3(SCL1)",3,0,3,"light slate blue")

    button3StandartCol1 = Button(fenster, width=11, bg="lime green", text="GPIO4", command=lambda:ChangeStateOn(button3StandartCol1,"GPIO4",4,0,4,"lime green"))
    button3StandartCol1.grid(row=4, column=0, pady=1)
    if Check == True:
        if LoadStateList[4] == "1":
            ChangeStateOn(button3StandartCol1,"GPIO4",4,0,4,"lime green")

    button4StandartCol1 = Button(fenster, width=11, bg="Grey30", text="GND", command=DISABLED)
    button4StandartCol1.grid(row=5, column=0, pady=1)

    button5StandartCol1 = Button(fenster, width=11, bg="lime green", text="GPIO17", command=lambda:ChangeStateOn(button5StandartCol1,"GPIO17",6,0,17,"lime green"))
    button5StandartCol1.grid(row=6, column=0, pady=1)
    if Check == True:
        if LoadStateList[17] == "1":
            ChangeStateOn(button5StandartCol1,"GPIO17",6,0,17,"lime green")

    button6StandartCol1 = Button(fenster, width=11, bg="lime green", text="GPIO27", command=lambda:ChangeStateOn(button6StandartCol1,"GPIO27",7,0,27,"lime green"))
    button6StandartCol1.grid(row=7, column=0, pady=1)
    if Check == True:
        if LoadStateList[27] == "1":
            ChangeStateOn(button6StandartCol1,"GPIO27",7,0,27,"lime green")

    button7StandartCol1 = Button(fenster, width=11, bg="lime green", text="GPIO22", command=lambda:ChangeStateOn(button7StandartCol1,"GPIO22",8,0,22,"lime green"))
    button7StandartCol1.grid(row=8, column=0, pady=1)
    if Check == True:
        if LoadStateList[22] == "1":
            ChangeStateOn(button7StandartCol1,"GPIO22",8,0,22,"lime green")

    button8StandartCol1 = Button(fenster, width=11, bg="Red", text="3.3V", command=DISABLED)
    button8StandartCol1.grid(row=9, column=0, pady=1)

    button9StandartCol1 = Button(fenster, width=11, bg="light slate blue", text="GPIO10(_MOSI)", command=lambda:ChangeStateOn(button9StandartCol1,"GPIO10(_MOSI)",10,0,10,"light slate blue"))
    button9StandartCol1.grid(row=10, column=0, pady=1)
    if Check == True:
        if LoadStateList[10] == "1":
            ChangeStateOn(button9StandartCol1,"GPIO10(_MOSI)",10,0,10,"light slate blue")

    button10StandartCol1 = Button(fenster, width=11, bg="light slate blue", text="GPIO9(_MOSI)", command=lambda:ChangeStateOn(button10StandartCol1,"GPIO9(_MOSI)",11,0,9,"light slate blue"))
    button10StandartCol1.grid(row=11, column=0, pady=1)
    if Check == True:
        if LoadStateList[9] == "1":
            ChangeStateOn(button10StandartCol1,"GPIO9(_MOSI)",11,0,9,"light slate blue")

    button11StandartCol1 = Button(fenster, width=11, bg="light slate blue", text="GPIO11(_SCLK)", command=lambda:ChangeStateOn(button11StandartCol1,"GPIO11(_SCLK)",12,0,11,"light slate blue"))
    button11StandartCol1.grid(row=12, column=0, pady=1)
    if Check == True:
        if LoadStateList[11] == "1":
            ChangeStateOn(button11StandartCol1,"GPIO11(_SCLK)",12,0,11,"light slate blue")

    button12StandartCol1 = Button(fenster, width=11, bg="Grey30", text="GND", command=DISABLED)
    button12StandartCol1.grid(row=13, column=0, pady=1)

    button13StandartCol1 = Button(fenster, width=11, bg="Yellow", text="ID_SC(GPIO0)", command=lambda:ChangeStateOn(button13StandartCol1,"ID_SC(GPIO0)",14,0,0,"Yellow"))
    button13StandartCol1.grid(row=14, column=0, pady=1)
    if Check == True:
        if LoadStateList[0] == "1":
            ChangeStateOn(button13StandartCol1,"ID_SC(GPIO0)",14,0,0,"Yellow")

    button14StandartCol1 = Button(fenster, width=11, bg="lime green", text="GPIO5", command=lambda:ChangeStateOn(button14StandartCol1,"GPIO5",15,0,5,"lime green"))
    button14StandartCol1.grid(row=15, column=0, pady=1)
    if Check == True:
        if LoadStateList[5] == "1":
            ChangeStateOn(button14StandartCol1,"GPIO5",15,0,5,"lime green")

    button15StandartCol1 = Button(fenster, width=11, bg="lime green", text="GPIO6", command=lambda:ChangeStateOn(button15StandartCol1,"GPIO6",16,0,6,"lime green"))
    button15StandartCol1.grid(row=16, column=0, pady=1)
    if Check == True:
        if LoadStateList[6] == "1":
            ChangeStateOn(button15StandartCol1,"GPIO6",16,0,6,"lime green")

    button16StandartCol1 = Button(fenster, width=11, bg="lime green", text="GPIO13", command=lambda:ChangeStateOn(button16StandartCol1,"GPIO13",17,0,13,"lime green"))
    button16StandartCol1.grid(row=17, column=0, pady=1)
    if Check == True:
        if LoadStateList[13] == "1":
            ChangeStateOn(button16StandartCol1,"GPIO13",17,0,13,"lime green")

    button17StandartCol1 = Button(fenster, width=11, bg="lime green", text="GPIO19", command=lambda:ChangeStateOn(button17StandartCol1,"GPIO19",18,0,19,"lime green"))
    button17StandartCol1.grid(row=18, column=0, pady=1)
    if Check == True:
        if LoadStateList[19] == "1":
            ChangeStateOn(button17StandartCol1,"GPIO19",18,0,19,"lime green")

    button18StandartCol1 = Button(fenster, width=11, bg="lime green", text="GPIO26", command=lambda:ChangeStateOn(button18StandartCol1,"GPIO26",19,0,26,"lime green"))
    button18StandartCol1.grid(row=19, column=0, pady=1)
    if Check == True:
        if LoadStateList[26] == "1":
            ChangeStateOn(button18StandartCol1,"GPIO26",19,0,26,"lime green")

    button19StandartCol1 = Button(fenster, width=11, bg="Grey30", text="GND", command=DISABLED)
    button19StandartCol1.grid(row=20, column=0, pady=1)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#----------Butoons Reihe 2---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    button0StandartCol2 = Button(fenster, width=11, bg="Red", text="5.0V", command=DISABLED)
    button0StandartCol2.grid(row=1, column=3, padx=20)

    button1StandartCol2 = Button(fenster, width=11, bg="Red", text="5.0V", command=DISABLED)
    button1StandartCol2.grid(row=2, column=3, sticky=N)

    button2StandartCol2 = Button(fenster, width=11, bg="Grey30", text="GND", command=DISABLED)
    button2StandartCol2.grid(row=3, column=3, sticky=N)

    button3StandartCol2 = Button(fenster, width=11, bg="light slate blue", text="GPIO14(_TXD)", command=lambda:ChangeStateOn(button3StandartCol2,"GPIO14(_TXD)",4,3,14,"light slate blue"))
    button3StandartCol2.grid(row=4, column=3, sticky=N)
    if Check == True:
        if LoadStateList[14] == "1":
            ChangeStateOn(button3StandartCol2,"GPIO14(_TXD)",4,3,14,"light slate blue")

    button4StandartCol2 = Button(fenster, width=11, bg="light slate blue", text="GPIO15(_RXD)", command=lambda:ChangeStateOn(button4StandartCol2,"GPIO15(_RXD)",5,3,15,"light slate blue"))
    button4StandartCol2.grid(row=5, column=3, sticky=N)
    if Check == True:
        if LoadStateList[15] == "1":
            ChangeStateOn(button4StandartCol2,"GPIO15(_RXD)",5,3,15,"light slate blue")

    button5StandartCol2 = Button(fenster, width=11, bg="lime green", text="GPIO18", command=lambda:ChangeStateOn(button5StandartCol2,"GPIO18",6,3,18,"lime green"))
    button5StandartCol2.grid(row=6, column=3, sticky=N)
    if Check == True:
        if LoadStateList[18] == "1":
            ChangeStateOn(button5StandartCol2,"GPIO18",6,3,18,"lime green")

    button6StandartCol2 = Button(fenster, width=11, bg="Grey30", text="GND", command=DISABLED)
    button6StandartCol2.grid(row=7, column=3, sticky=N)

    button7StandartCol2 = Button(fenster, width=11, bg="lime green", text="GPIO23", command=lambda:ChangeStateOn(button7StandartCol2,"GPIO23",8,3,23,"lime green"))
    button7StandartCol2.grid(row=8, column=3, sticky=N)
    if Check == True:
        if LoadStateList[23] == "1":
            ChangeStateOn(button7StandartCol2,"GPIO23",8,3,23,"lime green")

    button8StandartCol2 = Button(fenster, width=11, bg="lime green", text="GPIO24", command=lambda:ChangeStateOn(button8StandartCol2,"GPIO24",9,3,24,"lime green"))
    button8StandartCol2.grid(row=9, column=3, sticky=N)
    if Check == True:
        if LoadStateList[24] == "1":
            ChangeStateOn(button8StandartCol2,"GPIO24",9,3,24,"lime green")

    button9StandartCol2 = Button(fenster, width=11, bg="Grey30", text="GND", command=DISABLED)
    button9StandartCol2.grid(row=10, column=3, sticky=N)

    button10StandartCol2 = Button(fenster, width=11, bg="lime green", text="GPIO25", command=lambda:ChangeStateOn(button10StandartCol2,"GPIO25",11,3,25,"lime green"))
    button10StandartCol2.grid(row=11, column=3, sticky=N)
    if Check == True:
        if LoadStateList[25] == "1":
            ChangeStateOn(button10StandartCol2,"GPIO25",11,3,25,"lime green")

    button11StandartCol2 = Button(fenster, width=11, bg="light slate blue", text="GPIO8(_CE0_N)", command=lambda:ChangeStateOn(button11StandartCol2,"GPIO8(_CE0_N)",12,3,8,"light slate blue"))
    button11StandartCol2.grid(row=12, column=3, sticky=N)
    if Check == True:
        if LoadStateList[8] == "1":
            ChangeStateOn(button11StandartCol2,"GPIO8(_CE0_N)",12,3,8,"light slate blue")

    button12StandartCol2 = Button(fenster, width=11, bg="light slate blue", text="GPIO7(_CE1_N)", command=lambda:ChangeStateOn(button12StandartCol2,"GPIO7(_CE1_N)",13,3,7,"light slate blue"))
    button12StandartCol2.grid(row=13, column=3, sticky=N)
    if Check == True:
        if LoadStateList[7] == "1":
            ChangeStateOn(button12StandartCol2,"GPIO7(_CE1_N)",13,3,7,"light slate blue")

    button13StandartCol2 = Button(fenster, width=11, bg="Yellow", text="ID_SC(GPIO1)", command=lambda:ChangeStateOn(button13StandartCol2,"ID_SC(GPIO1)",14,3,1,"Yellow"))
    button13StandartCol2.grid(row=14, column=3, sticky=N)
    if Check == True:
        if LoadStateList[1] == "1":
            ChangeStateOn(button13StandartCol2,"ID_SC(GPIO1)",14,3,1,"Yellow")

    button14StandartCol2 = Button(fenster, width=11, bg="Grey30", text="GND", command=DISABLED)
    button14StandartCol2.grid(row=15, column=3, sticky=N)

    button15StandartCol2 = Button(fenster, width=11, bg="lime green", text="GPIO12", command=lambda:ChangeStateOn(button15StandartCol2,"GPIO12",16,3,12,"lime green"))
    button15StandartCol2.grid(row=16, column=3, sticky=N)
    if Check == True:
        if LoadStateList[12] == "1":
            ChangeStateOn(button15StandartCol2,"GPIO12",16,3,12,"lime green")

    button16StandartCol2 = Button(fenster, width=11, bg="Grey30", text="GND", command=DISABLED)
    button16StandartCol2.grid(row=17, column=3, sticky=N)

    button17StandartCol2 = Button(fenster, width=11, bg="lime green", text="GPIO16", command=lambda:ChangeStateOn(button17StandartCol2,"GPIO16",18,3,16,"lime green"))
    button17StandartCol2.grid(row=18, column=3, sticky=N)
    if Check == True:
        if LoadStateList[16] == "1":
            ChangeStateOn(button17StandartCol2,"GPIO16",18,3,16,"lime green")

    button18StandartCol2 = Button(fenster, width=11, bg="lime green", text="GPIO20", command=lambda:ChangeStateOn(button18StandartCol2,"GPIO20",19,3,20,"lime green"))
    button18StandartCol2.grid(row=19, column=3, sticky=N)
    if Check == True:
        if LoadStateList[20] == "1":
            ChangeStateOn(button18StandartCol2,"GPIO20",19,3,20,"lime green")

    button19StandartCol2 = Button(fenster, width=11, bg="lime green", text="GPIO21", command=lambda:ChangeStateOn(button19StandartCol2,"GPIO21",20,3,21,"lime green"))
    button19StandartCol2.grid(row=20, column=3, sticky=N)
    if Check == True:
        if LoadStateList[21] == "1":
            ChangeStateOn(button19StandartCol2,"GPIO21",20,3,21,"lime green")

    ButtonsErstellt = True
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------PulseButtons------------------------------

Pulseimg = tkinter.PhotoImage(file=picture2path)

#3.3V

B2Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(2))
B2Pulse.grid(row=2, column=2, padx=2,pady=1,sticky=W)

B3Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(3))
B3Pulse.grid(row=3, column=2, padx=2,pady=1,sticky=W)

B4Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(4))
B4Pulse.grid(row=4, column=2, padx=2,pady=1,sticky=W)

#GND

B17Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(17))
B17Pulse.grid(row=6, column=2, padx=2,pady=1,sticky=W)

B27Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(27))
B27Pulse.grid(row=7, column=2, padx=2,pady=1,sticky=W)

B22Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(22))
B22Pulse.grid(row=8, column=2, padx=2,pady=1,sticky=W)

#3.3V

B10Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(10))
B10Pulse.grid(row=10, column=2, padx=2,pady=1,sticky=W)

B9Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(9))
B9Pulse.grid(row=11, column=2, padx=2,pady=1,sticky=W)

B11Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(11))
B11Pulse.grid(row=12, column=2, padx=2,pady=1,sticky=W)

#GND

B0Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(0))
B0Pulse.grid(row=14, column=2, padx=2,pady=1,sticky=W)

B5Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(5))
B5Pulse.grid(row=15, column=2, padx=2,pady=1,sticky=W)

B6Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(6))
B6Pulse.grid(row=16, column=2, padx=2,pady=1,sticky=W)

B13Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(13))
B13Pulse.grid(row=17, column=2, padx=2,pady=1,sticky=W)

B19Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(19))
B19Pulse.grid(row=18, column=2, padx=2,pady=1,sticky=W)

B26Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(26))
B26Pulse.grid(row=19, column=2, padx=2,pady=1,sticky=W)

#GND


#---------------------Col "3"----------------------------------------

#3.3V

#3.3V

#GND

B14Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(14))
B14Pulse.grid(row=4, column=2, padx=2,pady=1,sticky=E)

B15Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(15))
B15Pulse.grid(row=5, column=2, padx=2,pady=1,sticky=E)

B18Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(18))
B18Pulse.grid(row=6, column=2, padx=2,pady=1,sticky=E)

#GND

B23Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(23))
B23Pulse.grid(row=8, column=2, padx=2,pady=1,sticky=E)

B24Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(24))
B24Pulse.grid(row=9, column=2, padx=2,pady=1,sticky=E)

#GND

B25Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(25))
B25Pulse.grid(row=11, column=2, padx=2,pady=1,sticky=E)

B8Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(8))
B8Pulse.grid(row=12, column=2, padx=2,pady=1,sticky=E)

B7Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(7))
B7Pulse.grid(row=13, column=2, padx=2,pady=1,sticky=E)

B1Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(1))
B1Pulse.grid(row=14, column=2, padx=2,pady=1,sticky=E)

#GND

B12Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(12))
B12Pulse.grid(row=16, column=2, padx=2,pady=1,sticky=E)

#GND

B16Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(16))
B16Pulse.grid(row=18, column=2, padx=2,pady=1,sticky=E)

B20Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(20))
B20Pulse.grid(row=19, column=2, padx=2,pady=1,sticky=E)

B21Pulse = Button(fenster,image=Pulseimg,command=lambda:Pulse(21))
B21Pulse.grid(row=20, column=2, padx=2,pady=1,sticky=E)
#----------------------------------------------------------------
#----------------------------------------------------------------------------------


#------------------------------Startup controll---------------------------
try:
    Configurations = open(Configspath, "r")
except:
    messagebox.showerror(title="Error",message="Error 1 \n  File 'Configs.txt' not found")
    sys.exit()
ConfigVar2 = False
ConfigVar3 = False
Check = False
while 1:
    Line = Configurations.readline()
    if Line == "":
        if ConfigVar2 != True:
            buttons(False)
            messagebox.showerror(title="Error",message="Error 3 \n  Configuration: '2.' in File 'Configs.txt' not found")
            fenster.destroy()
            sys.exit()
        if ConfigVar3 != True:
            buttons(False)
            messagebox.showerror(title="Error",message="Error 3 \n  Configuration: '3.' in File 'Configs.txt' not found")
            fenster.destroy()
            sys.exit()
        break
    
    if Line[0] == '#':
        continue   
    if Line[0] == "2":
        if Line[2] == "Y" or Line[2] == "N":
            ConfigVar2 = True
        else:
            buttons(False)
            messagebox.showerror(title="Error",message="Error 2 \n  Configuration: '2.' in File 'Configs.txt' wrong")
            fenster.destroy()
            sys.exit()

    if Line[0] == "3":
        if Line[2] == "Y" or Line[2] == "N":
            ConfigVar3 = True
        else:
            buttons(False)
            messagebox.showerror(title="Error",message="Error 2 \n  Configuration: '3.' in File 'Configs.txt' wrong")
            fenster.destroy()
            sys.exit()
    else:
        continue
Configurations.close()

buttons(False)
#------------------------------------------------------------------------
    
fenster.mainloop()
