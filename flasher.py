import PySimpleGUI as sg
import PIL.Image
import io
import os
import sys
import time
import glob
import base64
import _thread
import contextlib
import esptool


sys.stdout = open('output.txt', 'w')
sg.theme('DarkBlue')
names = glob.glob("/dev/ttyUSB*")

layout = [ 
 [sg.Image('logo.png', key='-LOGO-', size=(300, 150), expand_x=True, expand_y=True )],
 [sg.Text('Select COM Port:'), sg.Combo(names, font=('Arial Bold', 14), size=(18, 1), readonly=False, key='-PORTS-')],
 [sg.Text('Firmware Image:'), sg.InputText(size=(33, 1)), sg.FileBrowse(key="-FILE-")],
 [sg.Text('', size=(18,1)), sg.Button('Upgrade', size=(20, 1))] ]



window = sg.Window(title="MakerMade Flash Utility v1.1", layout=layout, size=(450, 400), location=(800, 300))

Port = ''
Firmware = ''
UploadSpeed = '115000'
FlashMode = 'dout'
FlashSize = '8M'
CPUSpeed  = '160Mhz'
Protocol  = 'esptool'
ChipType  = 'auto'

def WriteFirmware(filename):
    # Start ESPtool in it's own process as to not block the GUI thread

    # Erease the Flash first
    ## esptool --chip esp32 erase_flash
    # Write the new firmware to the flash 
    ## esptool --chip esp32 --port PORT write_flash -z 0x1000 Firmware

    config = "--erase-all --flash_size detect --chip auto --after reset --flash_mode dout --baud 115000 " + "--port " + port + " write_flash -z 0x1000 " + filename
    esptool._main(config)

while True:
      event, values = window.read()

      if event == sg.WINDOW_CLOSED:
         break
      
      if event == 'Upgrade':
         print (values['-PORTS-'])
         print (values['-FILE-'])


         _thread.start_new_thread( WriteFirmware, (config, ) )

         ProgressLayout = [
                   [sg.ProgressBar(100, orientation='h', expand_x=True, size=(20, 20),  key='-PBAR-')],
                   [sg.Text('', key='-OUT-', enable_events=True, font=('Arial Bold', 16), justification='center', expand_x=True)]]

         ProgressBar = sg.Window('Writing Firmware', ProgressLayout, size=(715, 150))

         ProgressStatus = 0
         
         while True:
               if(ProgressStatus > 99):
                 print ('Write complete')
                 quit()

               with open(r'output.txt', 'r') as fp:
                    lines = fp.readlines()
                    for row in lines:
                        for x in range(0,100, 2):
                            if row.find(str(x) + "%") > -1:
                               ProgressStatus = x
                             
                   ProgressBar['-PBAR-'].update(current_count=ProgressStatus)

window.close()
