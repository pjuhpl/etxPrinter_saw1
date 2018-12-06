# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:40:25 2018

@author: pju
"""

from pynput import keyboard
import os
import time
import datetime

#dirfileCun='C:/emmegi/STAR/LDT/'
#dirfileEtk='Z:/emmegifdd/ETX/'
#dirfileEtklog='Z:/emmegifdd/ETX/log/'
#dirfileTmp='Z:/emmegifdd/ETX/tmp/TMP.rtf'

dirfileCun='D:/PJU/drukarka/CUN/'
dirfileEtk='D:/PJU/drukarka/ET/'
dirfileEtklog='D:/PJU/drukarka/ET/log/'
dirfileTmp='D:/PJU/drukarka/ET/tmp/TMP.rtf'

linesEtk=5
drukuj = ''

def on_release(key):
    global drukuj
    if key == keyboard.KeyCode.from_char('0'):
        drukuj = ''
        drukuj += 'd'
    if key == keyboard.KeyCode.from_char('4'):
        drukuj += 'r'
    if key == keyboard.KeyCode.from_char('7'):
        drukuj += 'u'
    if key == keyboard.KeyCode.from_char('8'):
        drukuj += 'k'
        
    print(drukuj)
    
    if drukuj == 'druk':
        drukuj = ''
        dataOld = time.localtime(1423417361.451116)
        pliki = []
        v=-1
        for file in os.listdir(dirfileCun):
            if file.endswith(".CUN") or file.endswith(".DAT") or file.endswith(".TLS"):
                #print(file + time.strftime("      %m/%d/%Y %I:%M:%S %p",time.localtime(os.path.getmtime(dirCun + file))))
                
                dataNew=time.localtime(os.path.getmtime(dirfileCun + file))

                if dataNew >= dataOld:
                    pliki.append(file)
                    v += 1
                    dataOld=dataNew
        plikEt=pliki[v][0:len(pliki[v])-4] + '.txt'
        print('Ostatnio uzyty: ')
        print(pliki[v])
        
        if os.path.isfile(dirfileEtk + plikEt):
            fileEtk = open(dirfileEtk + plikEt, 'r').read()
            lines = fileEtk.split('\n') 
            fileEtklog = open(dirfileEtklog + pliki[v][0:len(pliki[v])-4] + '.log', 'a')
            
            if len(lines)>1: 
                for i in range(linesEtk):  
                    print(lines[i])
                    fileEtklog.write(lines[i] + '\n')
                    if i==4:
                        fileEtklog.write(str(datetime.datetime.now()) + '\n')
                    fileEtk = open(dirfileEtk + plikEt, 'w') 
                    for i in range(linesEtk,(len(lines))):
                        if i < len(lines)-1:
                            fileEtk.write(lines[i] + '\n')
                        else:
                            fileEtk.write(lines[i])
                    
                    fileTmp = open(dirfileTmp, 'w')
                    fileTmp.write('{\\rtf1\\ansi\\ansicpg1250\\deff0\\nouicompat\\deflang1045\\deflangfe1045{\\fonttbl{\\f0\\fnil\\fcharset238 Calibri;}')
                    fileTmp.write('{\\f1\\fnil\\fcharset2 Bar-Code 39;}{\\f2\\fnil\\fcharset0 Calibri;}} \n')
                    fileTmp.write('{\\*\\generator Riched20 6.3.9600}{\\*\mmathPr\\mnaryLim0\\mdispDef1\\mwrapIndent1440 }')
                    fileTmp.write('\\viewkind4\\uc1 \n\\pard\\sa200\\sl276\\slmult1\\f0\\fs22 ')
                    for k in range(linesEtk):
                        if k==0:
                            fileTmp.write(lines[k] + '\\line\\fs28 ')
                        if k==1:
                            fileTmp.write(lines[k] + '\\line\\f1\\fs36 *')
                        if k==2:
                            if lines[3][len(lines[3])-3:len(lines[3])] == 'CNC' :
                                fileTmp.write(lines[k] + '*\\f2  ' + lines[3][len(lines[3])-3:len(lines[3])] + '\\fs22\\line ')
                            else:
                                fileTmp.write(lines[k] + '*\\f2\\fs22\\line ')
                        if k==3:
                            if lines[3][len(lines[3])-3:len(lines[3])] == 'CNC' :
                                fileTmp.write(lines[k][0:len(lines[k])-4] + '\\line\\b\\fs28 ')
                            else:
                                fileTmp.write(lines[k] + '\\line\\b\\fs28 ')
                        if k==4:
                            wymiar = lines[k].split(';')
                            fileTmp.write(wymiar[0] + '\\b0\\fs22          ' + wymiar[1] + '  ;  ' + wymiar[2] + '\\lang21\\par}')  
                
                os.startfile(dirfileTmp, "print")
                fileEtk.close()    
                fileTmp.close()
                fileEtklog.close()
        

with keyboard.Listener(on_release=on_release) as listener:
    listener.join()
    
