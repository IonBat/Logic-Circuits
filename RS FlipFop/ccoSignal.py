# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 08:52:47 2014

cbco rev 1
@author: CBCO
"""

"""
import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)
import scipy as sp  # SciPy (signal and image processing library)

import matplotlib as mpl          # Matplotlib (2D/3D plotting library)
import matplotlib.pyplot as plt   # Matplotlib's pyplot: MATLAB-like syntax
from pylab import *               # Matplotlib's pylab interface
ion()                             # Turned on Matplotlib's interactive mode

import guidata                    # GUI generation for easy dataset editing and display

import guiqwt                     # Efficient 2D data-plotting features
import guiqwt.pyplot as plt_      # guiqwt's pyplot: MATLAB-like syntax
plt_.ion()                        # Turned on guiqwt's interactive mode


Within Spyder, this interpreter also provides:
    * special commands (e.g. %ls, %pwd, %clear)
    * system commands, i.e. all commands starting with '!' are subprocessed
      (e.g. !dir on Windows or !ls on Linux, and so on)

@Article{Hunter:2007,
  Author    = {Hunter, J. D.},
  Title     = {Matplotlib: A 2D graphics environment},
  Journal   = {Computing In Science \& Engineering},
  Volume    = {9},
  Number    = {3},
  Pages     = {90--95},
  abstract  = {Matplotlib is a 2D graphics package used for Python
  for application development, interactive scripting, and
  publication-quality image generation across user
  interfaces and operating systems.},
  publisher = {IEEE COMPUTER SOC},
  year      = 2007
}

"""
from numpy           import linspace
from sympy import Union, Intersection, symbols, And, Or, Inverse

    
class DiscreteSignal:
    
    def __init__(self,  stream=[], res=1, domain="t"):
        
        self.res=res
        self.stream=stream
        self.signal=[]
        self.topPe=[]
        self.risePe=[]
        self.fallPe=[]
        self.impulsePe=[]
        self.bottomNe=[]
        self.riseNe=[]
        self.fallNe=[]
        self.impulseNe=[]
        self.topPs=[]
        self.risePs=[]
        self.fallPs=[]
        self.impulsePs=[]
        self.bottomNs=[]
        self.riseNs=[]
        self.fallNs=[]
        self.impulseNs=[]

       

    def Clear(self):
        self.stream=[]
        self.signal=[]
        self.topPe=[]
        self.risePe=[]
        self.fallPe=[]
        self.impulsePe=[]
        self.bottomNe=[]
        self.riseNe=[]
        self.fallNe=[]
        self.impulseNe=[]
        self.topPs=[]
        self.risePs=[]
        self.fallPs=[]
        self.impulsePs=[]
        self.bottomNs=[]
        self.riseNs=[]
        self.fallNs=[]
        self.impulseNs=[]

        
        
    def Function(self,stream,start=0):
        self.Clear()
        self.start=start
        self.stream=stream
        temp=sum(stream)
        self.time=linspace(0,temp,self.res*temp)
      
        #print(len(self.riseStems))
            
        if start==0:
            state=0
            for i in range(len(self.stream)):
                if i%2:
                    state=1
                else:
                    state=0
                for k in range(self.res*stream[i]):
                    self.signal.append(state)    
        else:
            state=1
            for i in range(len(self.stream)):
                if i%2:
                    state=0
                else:
                    state=1
                for k in range(self.res*stream[i]):
                    self.signal.append(state)    

    def GetPulses(self, signal=[]):
        if signal != []:
            self.signal=signal
            self.Clear()
        else:
            signal=self.signal
            self.Clear()
            self.signal=signal
        l=len(signal)
        self.time=linspace(0,l,self.res*l)
        l=len(signal);print(l)
        for i in range(1,l-1):
            if And(signal[i-1]==1,signal[i]==1,signal[i+1]==1):
                self.topPe.append(i)
                self.topPs.append([i-1,i,i+1])
            if And(signal[i-1]==0,signal[i]==1,signal[i+1]==1):
                self.risePe.append(i)
                self.risePs.append([i,i+1])
            if And(signal[i-1]==1,signal[i]==1,signal[i+1]==0):
                self.fallPe.append(i)
                self.fallPs.append([i-1,i])
            if And(signal[i-1]==0,signal[i]==1,signal[i+1]==0):
                self.impulsePe.append(i)
                self.impulsePs.append([i])
            if And(signal[i-1]==0,signal[i]==0,signal[i+1]==0):
                self.bottomNe.append(i)
                self.bottomNs.append([i-1,i,i+1])
            if And(signal[i-1]==1,signal[i]==0,signal[i+1]==0):
                self.fallNe.append(i)
                self.fallNs.append([i,i+1])
            if And(signal[i-1]==0,signal[i]==0,signal[i+1]==1):
                self.riseNe.append(i)
                self.riseNs.append([i-1,i])
            if And(signal[i-1]==1,signal[i]==0,signal[i+1]==1):
                self.impulseNe.append(i)
                self.impulseNs.append([i])
            
    def InvertSignal(self,signal):
        self.signalN=[]
        self.signal=signal
        l=len(signal)
        for i in signal:
            if i==0:
                self.signalN.append(1)
            else:
                self.signalN.append(0)
    
    def GenStem(self,pulses,type="p",logic="p"):
        l=len(pulses)
        mx=max(pulses)
        element=[]
        if logic=="p":
            signal=zero(1,mx)
            for i in range(1,l-1):
                if type=="p":
                    signal[i-1]=1;signal[i]=1;signal[i+1]=1
                    element.append([i-1,i,i+1])
                if type=="r":
                    signal[i-1]=0;signal[i]=1;signal[i+1]=1
                    element.append([i,i+1])
                if type=="f":
                    signal[i-1]=1;signal[i]=1;signal[i+1]=0
                    element.append([i-1,i])
                if type=="i":
                    signal[i-1]=0;signal[i]=1;signal[i+1]=0
                    element.append([i])
        else: 
            signal=ones(1,mx)
            for i in range(1,l-1):
                if type=="p":
                    signal[i-1]=0;signal[i]=0;signal[i+1]=0
                    element.append([i-1,i,i+1])
                if type=="r":
                    signal[i-1]=0;signal[i]=0;signal[i+1]=1
                    element.append([i-1,i])
                if type=="f":
                    signal[i-1]=1;signal[i]=0;signal[i+1]=0
                    element.append([i,i+1])
                if type=="i":
                    signal[i-1]=1;signal[i]=0;signal[i+1]=1
                    element.append([i])
        return element, signal    
    
        
            
        

   
 




"""
    def TexSet(self,element):
        return str(element).replace("[","\\{").replace("]","\\}")
            
    def GeneratesElements(self,pulses):
        elements=[]
        for i in pulses:
            a=i[0];b=i[1]
            for j in range(a,a+b):
                elements.append(j)        
        return elements
        
    def NumData(self, PieceWise):
        level=[]
        time=[]

        for i in range(len(self.time)-1):
            temp=PieceWise.subs(t,self.time[i]).evalf(2)
            level.append(Float(temp,3))
            time.append(self.time[i])
        return np.array(time), np.array(level)        

    def DelayStem(self,Input,n=1):
        L1=len(Input);Output=list(np.zeros(L1))
        for i in range(n,L1-n):
            Output[i]=Input[i-n]
        return Output
        
        
    def AdvanceStem(self,Input,n=1):
        L1=len(Input);Output=list(np.zeros(L1))
        for i in range(L1-n):
            Output[i]=Input[i+n]
        return Output

    def IntersectStems(self,Input):
        L=len(Input);LI=len(Input[0]);Output=[]
        for i in range(1,L):LI=min(LI,len(Input[i]))
        for i in range(L):
            temp=[]
            for j in range(LI):temp.append(Input[i][j])
            Output.append(min(temp))
        return Output
        
    def UnionStems(self,Input):
        L=len(Input);LI=len(Input[0]);Output=[]
        for i in range(1,L):LI=min(LI,len(Input[i]))
        for i in range(L):
            temp=[]
            for j in range(LI):temp.append(Input[i][j])
            Output.append(max(temp))
        return Output
        
    def InvertStem(self,Input):
        L=len(Input);Output=[]
        for i in range(L):
            if Input[i]==0:Output.append(1)
            else:Output.append(0)
        return Output

    def RSFlipFlop(self,S,R):
        L=min(len(S),len(R))
        sQS=list(np.zeros(L))
        sQR=list(np.ones(L))
        sQSp=list(np.ones(L))
        sQRp=list(np.zeros(L))
        for i in range(L):
            if i>0 :
                sQS[i]=self.UnionElements([S[i],sQRp[i-1]])
                sQR[i]=self.UnionElements([R[i],sQSp[i-1]])
            else:
                sQS[i]=self.UnionElements([S[i],sQRp[0]])
                sQR[i]=self.UnionElements([R[i],sQSp[0]])
                    
            sQSp[i]=self.InvertElement(sQS[i])
            sQRp[i]=self.InvertElement(sQR[i])
#            print(i,"S=",S[i],"R=",R[i],"QS=",sQS[i],"QR=",sQR[i])
            sQS[i]=self.UnionElements([S[i],sQRp[i]])
            sQR[i]=self.UnionElements([R[i],sQSp[i]])
            sQSp[i]=self.InvertElement(sQS[i])
            sQRp[i]=self.InvertElement(sQR[i])
#            print(i,"S=",S[i],"R=",R[i],"QS=",sQS[i],"QR=",sQR[i])
            sQS[i]=self.UnionElements([S[i],sQRp[i]])
            sQR[i]=self.UnionElements([R[i],sQSp[i]])
            sQSp[i]=self.InvertElement(sQS[i])
            sQRp[i]=self.InvertElement(sQR[i])
#            print(i,"S=",S[i],"R=",R[i],"QS=",sQS[i],"QR=",sQR[i])
                      
        return sQS, sQSp, sQR, sQRp 
            
    def IntersectElements(self,Inputs):
        L1=len(Inputs)
        temp=[]
        for j in range(L1):temp.append(Inputs[j])
        return min(temp)            

            
    
    def EmptyStem(self):
        return list(np.zeros(len(self.stems)))
        
    def UniverseStem(self):
        return list(np.ones(len(self.stems)))
        
"""
