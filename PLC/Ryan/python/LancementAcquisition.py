# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 09:00:31 2018

@author: roussel
"""

import ModbusClient
import datetime
#
#####################################################################
#

class Connexion () :
    def __init__(self) :
        self.plcAddress='192.168.0.1'           ##'192.168.1.35'
        self.runCoil=0
        self.startTable=100
        self.registersByAcquisition=4 # CHANGE: 3 TO 4
        # On peut lire au maximum 125 registres à la fois
        self.maxOfSimultaneouslyReadingAcquisitions=30  # 40x3 < 125 # 30x4 < 125 CHANGE!
        self.connexion=None
        self.dataCollection=[]
        #
        # Start the connexion with the PLC
        self.initialize()
#
########
#
    def initialize(self) :
        self.connexion=ModbusClient.ModbusClient(self.plcAddress, 502)
        self.connexion.Connect()
        print("PLC {} is now connected...".format(self.plcAddress))
#
########
#
    def close(self) :
        self.connexion.close()
        print("The connexion with PLC {} is closed.".format(self.plcAddress))
#
########
#    
    def startAcquisition(self) :
        print("Start the data acquisition by the PLC")
        self.connexion.WriteSingleCoil(self.runCoil,1)
        self.dataCollection=[]
#
########
#                
    def stopAcquisition(self) :
        self.connexion.WriteSingleCoil(self.runCoil,0)
        print("The data acquisition by the PLC is interrupted.")
#
########
#                
    def stopAcquisitionWithCollect(self) :
        self.connexion.WriteSingleCoil(self.runCoil,0)
        print("The data acquisition by the PLC is interrupted.")
        # Lecture du nombre d'acquisition
        registers=self.connexion.ReadInputRegisters(0,1)
        numberOfAcquisitions=registers[0]
        # Lancement de la collecte des acquisitions
        self.collectData(numberOfAcquisitions)
        # Lancement de la sauvegarde sur disque 
        self.storeData()
#
########
#        
    def collectData(self,numberOfAcquisitionsToObtain):
        # On peut lire au maximum 125 registres à la fois
        # Il faut 
        print("Start the transfer of the first {} acquisitions...".format(numberOfAcquisitionsToObtain))
        numberOfReadedAcquistions=0
        while (numberOfAcquisitionsToObtain>numberOfReadedAcquistions) :
            startRegister=self.startTable+(numberOfReadedAcquistions*self.registersByAcquisition)
            numberOfAcquisitionsToRead=min(self.maxOfSimultaneouslyReadingAcquisitions,numberOfAcquisitionsToObtain-numberOfReadedAcquistions)
            numberOfRegisters=numberOfAcquisitionsToRead*self.registersByAcquisition
            print("Lecture de {} mots à partir de {}".format(numberOfRegisters,startRegister))
            registers=self.connexion.ReadInputRegisters(startRegister, numberOfRegisters)
            # Reconstruction et enregistrement des acquisitions
            for ref in range(numberOfAcquisitionsToRead):
                place=ref*self.registersByAcquisition
                timeMSB, timeLSB = registers[place], registers[place+1]
                IOvectorMSB, IOvectorLSB = registers[place+2], registers[place+3]
                time = (timeMSB << 8) + timeLSB
                IOvector = (IOvectorMSB << 8) + IOvectorLSB
                # Enregistrement des acquisitions
                self.dataCollection.append((time,IOvector))
            numberOfReadedAcquistions+=numberOfAcquisitionsToRead
        print("The transfer is done.")
#
########
#
        
    def storeData(self,name='Data'):
        """Enregistrement des acquisitions dans un fichier au format CSV (français)"""
        # Constitution du texte (avec entête) décrivant les acquisitions
        text="Time;IO vector \n"
        for data in self.dataCollection :
            time,IOvector=data
            IOvector="{:b}".format(IOvector)
            text+="{:>32};{:0>32}\n".format(time,IOvector)
        # Ecriture du texte dans le fichier 'NAME_DATE.csv'
        date = datetime.datetime.now()
        fileName="{}_{}_{:0>2}_{:0>2}_{:0>2}h{}min{}s.csv".format(name,date.year,date.month,date.day,date.hour,date.minute,date.second)
        file=open(fileName,'w')
        file.write(text)
        file.close()
        print("{} acquisitions stored on '{}' file.".format(len(self.dataCollection),fileName))
#
#####################################################################
#        
myConnexion=Connexion()
#myConnexion.startObservation()
#myConnexion.stopAcquisitionWithCollect()
        
