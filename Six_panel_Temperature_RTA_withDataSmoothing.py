import os
import time
import serial
from seabreeze.spectrometers import Spectrometer, list_devices
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, CheckButtons, TextBox, RadioButtons, Slider
np.seterr(divide='ignore', invalid='ignore') #ignores divide by zero and divide by NaN
import serial.serialutil
import serial.tools.list_ports



ports = serial.tools.list_ports.comports()
if (ports != []):
    port = ports[0]
    print("Arduino is connected to " + port.device)
    arduino = serial.Serial(port=port.device, baudrate=9600, timeout=20)
    axTemperature_title = "Temperature"
else:
    print("Connect Arduino for Temperature Sensing")
    axTemperature_title = "Arduino disconnected"

file = open("Temperature_vs_time.txt", 'w')
file.write("#time(s), Temperature,  Setpoint \n")
file.close()

def detect_temperature_heater():
    ports = serial.tools.list_ports.comports()
    len_ports = (len(ports))
    axTemperature_title = "Temperature" 
    # print(len_ports) 

    t1 = time.time()-t0
    t1 = "{:0.2f}".format(t1)
    

    if (len_ports !=0):
        try:
            data = arduino.readline()
            arduino.flushInput()  #### This is essential to keep reading the latest data sent by arduino, not old data that would be buffered
            temperature = data.decode('utf-8').strip()
            if (temperature == ''):
                return None
            
            stringToWrite = (str(t1)+ "\t"+ str(temperature))  
            axTemperature_title = "Temperature: " + str(temperature)+r" $^o$C"
            # print((stringToWrite))
            f = open('Temperature_vs_time.txt', 'a')
            f.write(stringToWrite+'\n')
            f.close()
                      
        except serial.serialutil.SerialException:
            print("Reconnect and restart the program.")

    else:
        axTemperature_title = "Arduino disconnected"
        print(axTemperature_title)

    
    return None

def get_from_last_line_of_file(fname):
    f = open(fname, "rb")
    f.seek(-3, 2)
    while (f.read(1)!=b'\n'):
        f.seek(-2, 1)

    t1, T = (f.readline().decode('utf-8').split("\t"))
    # print(float(t1))
    # print(float(T))
    f.close()
    if(float(t1)>20000):
        os._exit(0)

    return float(t1), float(T)


device = list_devices()
#print(device)

specR = Spectrometer.from_serial_number('FLMT05853')
specT = Spectrometer.from_serial_number('USB4K202409')

#set integration time
integrationTimeR = 100000 #time in microsecond
integrationTimeT = 30000
specR.integration_time_micros(integrationTimeR) #time in microsecond
specT.integration_time_micros(integrationTimeT) #time in microsecond

R_ydat = specR.intensities()
# print("len_Rydat = ", len(R_ydat))
R_wavelength = specR.wavelengths()

T_ydat = specR.intensities()
# print("len_Tydat = ", len(T_ydat))

T_wavelength = specR.wavelengths()




###### definition of buttons ########
def LightR(event):
    statusR = checkProcessR.get_status()[0]    #A boolean value, true of checkbox is ticked    
    if( statusR == False):
        x_, y_ = (lnR.get_data())
        plt.figure()
        plt.plot(x_, y_)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity")
        np.savetxt('brightR.txt', np.transpose([x_, y_]))
        plt.show()

def DarkR(event):
    statusR = checkProcessR.get_status()[0]    #A boolean value, true of checkbox is ticked
    if( statusR == False):
        x_, y_ = (lnR.get_data())
        plt.figure()
        plt.plot(x_, y_)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity")
        np.savetxt('darkR.txt', np.transpose([x_, y_]))
        plt.show()

###### definition of buttons ########
def LightT(event):
    statusT = checkProcessT.get_status()[0]    #A boolean value, true of checkbox is ticked
    if(statusT == False):
        x_, y_ = (lnT.get_data())
        plt.figure()
        plt.plot(x_, y_)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity")
        np.savetxt('brightT.txt', np.transpose([x_, y_]))
        plt.show()

def DarkT(event):
    statusT = checkProcessT.get_status()[0]    #A boolean value, true of checkbox is ticked
    if(statusT == False):
        x_, y_ = (lnT.get_data())
        plt.figure()
        plt.plot(x_, y_)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity")
        np.savetxt('darkT.txt', np.transpose([x_, y_]))
        plt.show()



########################## define axR and axT #######################
fig, ([axR, axT, axA], [axTemperature, axAutosave, axSmooth]) = plt.subplots(2, 3, figsize=(12, 5))



#############Reflection axis############################

lnR, = axR.plot(R_wavelength, R_ydat, color = 'r')
axR.set_xlabel("Wavelength (nm)")
axR.set_ylabel("Intensity")
axR.set_title("Spectrometer: FLMT05853")
axR.tick_params(direction = 'in')

########################## define checkbutton R #######################

axR_Process = axR.inset_axes([0.0, 0.0, 0.1, 0.05])
checkProcessR = CheckButtons(
            ax=axR_Process,
            labels = 'R', 
            label_props={'color' : 'red',}
)
axR_Process.spines['top'].set_visible(False)
axR_Process.spines['right'].set_visible(False)

################# define brightR ###################
dx = 0.15
dy = 0.09
x_button_bottomLeftCorner = 0.85
y_button_bottomLeftCorner = 0.9

axR_bright = axR.inset_axes([x_button_bottomLeftCorner, y_button_bottomLeftCorner, dx, dy])
ButtonBrightR = Button(axR_bright, 'Bright')
ButtonBrightR.on_clicked(LightR)

axR_dark = axR.inset_axes([x_button_bottomLeftCorner-1.1*dx, y_button_bottomLeftCorner, dx, dy])
ButtonDarkR = Button(axR_dark, 'Dark')
ButtonDarkR.on_clicked(DarkR)

axT_bright = axT.inset_axes([x_button_bottomLeftCorner, y_button_bottomLeftCorner, dx, dy])
ButtonBrightT = Button(axT_bright, 'Bright')
ButtonBrightT.on_clicked(LightT)

axT_dark = axT.inset_axes([x_button_bottomLeftCorner-1.1*dx, y_button_bottomLeftCorner, dx, dy])
ButtonDarkT = Button(axT_dark, 'Dark')
ButtonDarkT.on_clicked(DarkT)



#######################################################

lnT, = axT.plot(T_wavelength, T_ydat, color = 'teal')
axT.set_xlabel("Wavelength (nm)")
axT.set_ylabel("Intensity")
axT.set_title("Spectrometer: USB4K202409")
axT.tick_params(direction = 'in')

########################## define checkbutton T #######################

axT_Process = axT.inset_axes([0.0, 0.0, 0.1, 0.05])
checkProcessT = CheckButtons(
            ax=axT_Process,
            labels = 'T', 
            label_props={'color' : 'b',}
)
axT_Process.spines['top'].set_visible(False)
axT_Process.spines['right'].set_visible(False)



##### Define Absorption Axis ######
lnA, = axA.plot(T_wavelength, T_ydat, color = 'green')
axA.set_xlabel("Wavelength (nm)")
axA.set_ylabel("Intensity")
axA.set_title("Check on R, T and A")
axA.tick_params(direction = 'in')


############### define checkbutton for absorption ##############

axA_Process = axA.inset_axes([0.0, 0.0, 0.1, 0.05])
checkProcessA = CheckButtons(
            ax=axA_Process,
            labels = 'A', 
            label_props={'color' : 'g',}
)
axA_Process.spines['top'].set_visible(False)
axA_Process.spines['right'].set_visible(False)



############### Temperature panel ##################
axTemperature.set_title(axTemperature_title)
axTemperature.tick_params(direction = 'in')
axTemperature.set_ylim(20, 200)
axTemperature.set_ylabel(r"Temperature ($^o$C)")
TemperatureLine, = axTemperature.plot([], [], '.' , color = 'b')




#### Autosave axis tick removal #################
axAutosave.set_yticks([])
axAutosave.set_xticks([])
############### defining the autosave button #############################
ax_ASbutton = axAutosave.inset_axes([0.05, 0.85, 0.4, 0.1])# [left, bottom, width, height]
checkAutosave = CheckButtons(ax_ASbutton, ['Autosave'], [False])

basefilename_autosave = "Pdms_rate_thickness_"
ax_textbox = axAutosave.inset_axes([0.05, 0.67, 0.9, 0.1])
text_box = TextBox(ax_textbox, '', initial=basefilename_autosave)
ax_textbox.text(0, -0.8, 'Enter the sample name') #arguments take x, y, str



ax_Interval_slider = axAutosave.inset_axes([0.05, 0.2, 0.4, 0.1])
interval_slider = Slider(
    ax=ax_Interval_slider,
    label='',
    valmin=1,
    valmax=90,
    valinit=45,
    valstep=1
)
axAutosave.text(0.05, 0.4, 'Set Autosave Interval below') #arguments take x, y, str


ax_SecondsMinutes =  axAutosave.inset_axes([0.6, 0.05, 0.35, 0.30])# [left, bottom, width, height]
radioButton = RadioButtons(ax_SecondsMinutes, ('Seconds', 'Minutes'))



ax_SaveButton = axAutosave.inset_axes([0.55, 0.85, 0.4, 0.1])# [left, bottom, width, height]
ButtonSave = Button(ax_SaveButton, 'Save')
def saveData(event):
    currentTemperature = TemperatureLine.get_ydata()[-1]
    temperatureLabel = str(currentTemperature).replace(".", "p")
    print(temperatureLabel)

    x_, y_ = (lnR.get_data())
    filename = "R_"+text_box.text+temperatureLabel+"C.txt"
    np.savetxt(filename, np.transpose([x_, y_]))
    

    x_, y_ = (lnT.get_data())
    filename = "T_"+text_box.text+temperatureLabel+"C.txt"
    np.savetxt(filename, np.transpose([x_, y_]))

    x_, y_ = (lnA.get_data())
    filename = "A_"+text_box.text+temperatureLabel+"C.txt"
    np.savetxt(filename, np.transpose([x_, y_]))
    return None
ButtonSave.on_clicked(saveData)

######## buttons in axSmooth axis ##############
axSmooth.set_xticks([])
axSmooth.set_yticks([])


ax_slider_boxcar = axSmooth.inset_axes([0.05, 0.1, 0.8, 0.1])
sliderBoxLen = Slider(
    ax=ax_slider_boxcar,
    label='',
    valmin=1,
    valmax=100,
    valinit=45,
    valstep=1
)
axSmooth.text(0.05, 0.25, 'Boxcar [min: 1, max: 100]')

ax_slider_scan = axSmooth.inset_axes([0.05, 0.5, 0.8, 0.1])
sliderScan = Slider(
    ax=ax_slider_scan,
    label='',
    valmin=1,
    valmax=10,
    valinit=4,
    valstep=1
)
axSmooth.text(0.05, 0.65, 'Scans [min: 1, max: 10]')
axSmooth.text(0.05, 0.9, 'Spectra Smoothing')





def init():
    axTemperature.set_xlim(0, 5)
    return lnR, lnT, lnA, TemperatureLine,


        
        

t0 = time.time()
def update(frame):
    statusR = checkProcessR.get_status()[0]    #A boolean value, true of checkbox is ticked
    statusT = checkProcessT.get_status()[0]    #A boolean value, true of checkbox is ticked
    statusA = checkProcessA.get_status()[0]    #A boolean value, true of checkbox is ticked
    statusAutosave = checkAutosave.get_status()[0]

    #### determine autosave interval ####
    timeUnit = radioButton.value_selected
    intervalNum = interval_slider.val
    interval = int(intervalNum)
    # print(int(intervalNum))
    if(timeUnit=="Minutes"):
        interval = 60*interval
    # print("Data will be saved every "+str(interval)+ " seconds")

    

    #### detect boxcar and scans ######
    
    scanNum = sliderScan.val
    BoxLen = sliderBoxLen.val
    # scanNum = 4
    # BoxLen = 45
    initialTrim = 30

    
    wavelength = np.linspace(200, 850, 1303)
    xdatR, ydatR = specR.wavelengths()[2:], specR.intensities()[2:]
    xdatT, ydatT = specT.wavelengths()[2:], specT.intensities()[2:]
    for i in range(scanNum-1):
        ydatR = ydatR + specR.intensities()[2:]
        ydatT = ydatT + specT.intensities()[2:]
    ydatR = ydatR/scanNum
    ydatT = ydatT/scanNum

    
    
    

    

    
    

    lnR.set_data(xdatR, ydatR)
    axR.set_ylim(min(ydatR), max(ydatR))
    lnT.set_data(xdatT, ydatT)
    axT.set_ylim(min(ydatT), max(ydatT))
    axR.set_ylabel('Intensity')
    axT.set_ylabel('Intensity')
    axA.set_ylabel('Intensity')

    axA.set_title("Check on R, T and A")

    brightR_file_exists = os.path.isfile("brightR.txt")
    if(brightR_file_exists==False):
        print("Click Bright on R panel")
    darkR_file_exists = os.path.isfile("darkR.txt")
    if(darkR_file_exists==False):
        print("Click Dark on R panel")

    brightT_file_exists = os.path.isfile("brightT.txt")
    if(brightT_file_exists==False):
        print("Click Bright on T panel")
    darkT_file_exists = os.path.isfile("darkT.txt")
    if(darkT_file_exists==False):
        print("Click Dark on T panel")
    

    

    if(statusR):
        if(brightR_file_exists):
            brightR_dat = np.loadtxt("brightR.txt")
        if(darkR_file_exists):
            darkR_dat = np.loadtxt("darkR.txt")
        
        b = brightR_dat[:, 1]
        d = darkR_dat[:, 1]
        R = (ydatR-d)/(b-d)
        ydatR = R
        axR.set_ylim(-0.1, 1.12)
        axR.set_ylabel('R')

        xdatR = np.convolve(xdatR, np.ones(BoxLen)/BoxLen, mode = 'valid')
        ydatR = np.convolve(ydatR, np.ones(BoxLen)/BoxLen, mode = 'valid')
        ydatR = np.interp(wavelength, xdatR, ydatR)
        xdatR = wavelength
        lnR.set_data(xdatR, ydatR)

    if(statusT):
        if(brightT_file_exists):
            brightT_dat = np.loadtxt("brightT.txt")
        if(darkT_file_exists):
            darkT_dat = np.loadtxt("darkT.txt")
        b = brightT_dat[:, 1]
        d = darkT_dat[:, 1]
        T = (ydatT-d)/(b-d)
        ydatT = T
        axT.set_ylim(-0.1, 1.12)
        axT.set_ylabel('T')
        xdatT = np.convolve(xdatT, np.ones(BoxLen)/BoxLen, mode = 'valid')
        ydatT = np.convolve(ydatT, np.ones(BoxLen)/BoxLen, mode = 'valid')
        ydatT = np.interp(wavelength, xdatT, ydatT)
        xdatT = wavelength
        lnT.set_data(xdatT, ydatT)
        

    if(statusA):
        axA.set_title("Check on R and T")
        axA.set_ylabel('A')
        if(statusR and statusT):
            axA.set_title("Absorption, A = 1-T-R")
            A = 1-ydatT-ydatR
            lnA.set_data(xdatR, A)
            axA.set_ylim(-0.1, 1.2)

    
    
    returned_values = detect_temperature_heater()
    # if (returned_values != None):
    #     axTemperature_title_tmp = returned_values[0]
        # t1 = returned_values[1]
        # temperature = returned_values[2]
    
    
    t1, temperature = get_from_last_line_of_file('Temperature_vs_time.txt')
    axTemperature_title = "Temperature: " + str(temperature)+r" $^o$C"

    timeAxis, temperatureAxis = TemperatureLine.get_data()
    temperatureAxis = np.append(temperatureAxis, temperature)
    timeAxis = np.append(timeAxis, t1)
    axTemperature.set_xlim(0, t1+5)
    axTemperature.set_ylim(0, 220)

    TemperatureLine.set_data(timeAxis, temperatureAxis)
    axTemperature.set_title(axTemperature_title)



    ##### autosave widgets interaction ######
    currentTime_int = int(t1)
    timelabel = str(currentTime_int)
    temperatureLabel = str(int(temperature))
    textVal = text_box.text
    filenameR = "R_"+timelabel+"s_"+temperatureLabel+"C"+".txt"
    filenameT = "T_"+timelabel+"s_"+temperatureLabel+"C"+".txt"
    filenameA = "A_"+timelabel+"s_"+temperatureLabel+"C"+".txt"
    if(statusAutosave):
        if not os.path.exists(textVal): 
            os.makedirs(textVal) 
        text_box.stop_typing()
        if(currentTime_int%interval==0):
            if(statusR and statusT and statusR):
                print("data saved at", t1)

                x_, y_ = (lnR.get_data())
                np.savetxt(textVal+"/"+filenameR, np.transpose([x_, y_]))
                

                x_, y_ = (lnT.get_data())
                np.savetxt(textVal+"/"+filenameT, np.transpose([x_, y_]))

                x_, y_ = (lnA.get_data())
                np.savetxt(textVal+"/"+filenameA, np.transpose([x_, y_]))

                print(filenameR)
                print(filenameT)
                print(filenameA)
    else:
        text_box.begin_typing()
    

    axAutosave.set_xticks([])
    axAutosave.set_yticks([])


    
    return lnR, lnT, lnA, TemperatureLine,

frame = np.arange(0, 2*np.pi, 0.001)
ani = FuncAnimation(fig, update, frames=frame, init_func=init, interval = 200)


plt.tight_layout()
plt.show()

specR.close()
specT.close()