# -*- coding: utf-8 -*-
"""
Created on Dec 1 2020

ccoDiscreteSignal.py rev 0
@author: Celso Bation Co
"""

def PiecewiseData(fn,n,res,T):
    '''
    fn  are the waveform functions
    n   is  the number of waveforms
    res is  the time resolution
    T   is  the period of the waveform
    x   is  the domain data
    y   is  the range data
    '''
    x=np.linspace(0,n*T,num=n*res);y=np.ones(len(x))
    for i in range(len(x)):
        y[i]=fn.subs(t,x[i]%T)
    y=np.array(y)
    return x, y

from sympy import Union, Intersection

    
class DiscreteSignal:
    
    def __init__(self,  res=1000, domain="t"):
        
        self.res=res
        self.t=symbols(domain)
        self.PieceWiseFunction=[]
        self.TopPulses=[]
        self.BottomPulses=[]
        self.RisePulses=[]
        self.FallPulses=[]
        self.Now=0 
        self.start=0
        self.UniverseElements=[]
        self.TopElements=[]
        self.BottomElements=[]
        self.RiseElements=[]
        self.FallElements=[]
        self.stems=[]
        self.riseStems=[]
        self.fallStems=[]
        self.PieceWiseText="Piecewise("
        
    def RisingEdge(self, r=1, t0=0):
        m=1/r
        b=-t0/r
        return [m*self.t+b,(t0<=self.t)&(self.t<r+t0)]

    def FallingEdge(self,r=1,t0=0):
        m=-1/r
        b=(t0+r)/r
        return [m*self.t+b,(t0<=self.t)&(self.t<r+t0)]

    def TopEdge(self,r=1,t0=0):
        return [1,(t0<=self.t)&(self.t<r+t0)]

    def BottomEdge(self,r=1,t0=0):
        return [0,(t0<=self.t)&(self.t<r+t0)]

    def Clear(self):
        self.PieceWiseFunction=[]
        self.TopPulses=[]
        self.BottomPulses=[]
        self.RisePulses=[]
        self.FallPulses=[]
        self.Now=0 
        self.start=0
        self.UniverseElements=[]
        self.TopElements=[]
        self.BottomElements=[]
        self.RiseElements=[]
        self.FallElements=[]
        self.stems=[]
        self.riseStems=[]
        self.fallStems=[]
            
                
    def Function(self,stream,start=0):
        self.Clear()
        self.start=start
        self.stream=stream
        self.sum=sum(self.stream)
        self.time=linspace(0,self.sum,self.res)
      
        for i in range(self.sum+2):
            self.UniverseElements.append(i)
            self.stems.append(0)
            self.riseStems.append(0)
            self.fallStems.append(0)
        #print(len(self.riseStems))
            
        if start==0:
            for i in range(len(self.stream)):
                if i%2:
                    self.PieceWiseFunction.append(self.TopEdge(r=self.stream[i],t0=self.Now))
                    self.TopPulses.append([self.Now,self.stream[i]])
                    self.Now=self.Now+self.stream[i]
                    self.PieceWiseFunction.append(self.FallingEdge(t0=self.Now))
                    if self.Now>0:self.FallPulses.append([self.Now-1,1])

                                                                         
                    
                else:
                    self.PieceWiseFunction.append(self.BottomEdge(r=self.stream[i],t0=self.Now))
                    self.BottomPulses.append([self.Now,self.stream[i]])            
                    self.Now=self.Now+self.stream[i]
                    self.PieceWiseFunction.append(self.RisingEdge(t0=self.Now))
                    self.RisePulses.append([self.Now,1]) 
                    
        else:
            for i in range(len(self.stream)):
                if i%2:
                    self.PieceWiseFunction.append(self.BottomEdge(r=self.stream[i],t0=self.Now))
                    self.BottomPulses.append([self.Now,self.stream[i]])            
                    self.Now=self.Now+self.stream[i]
                    self.PieceWiseFunction.append(self.RisingEdge(t0=self.Now))
                    self.RisePulses.append([self.Now,1])
                    
                else:
                    self.PieceWiseFunction.append(self.TopEdge(r=self.stream[i],t0=self.Now))
                    self.TopPulses.append([self.Now,self.stream[i]])
                    self.Now=self.Now+self.stream[i]
                    self.PieceWiseFunction.append(self.FallingEdge(t0=self.Now))
                    if self.Now>0:self.FallPulses.append([self.Now-1,1])
                            
        self.TopElements=self.GeneratesElements(self.TopPulses)
        self.BottomElements=self.GeneratesElements(self.BottomPulses)
        self.RiseElements=self.GeneratesElements(self.RisePulses)
        self.FallElements=self.GeneratesElements(self.FallPulses)
        
        for i in self.FallElements:self.fallStems[i]=1
        for i in self.RiseElements:self.riseStems[i]=1
        for i in self.TopElements:self.stems[i]=1
        self.fallStems=self.fallStems[0:self.Now]
        self.riseStems=self.riseStems[0:self.Now]
        self.stems=self.stems[0:self.Now]        

        self.PieceWiseText="Piecewise(\\newline"
        for i in self.PieceWiseFunction:
            self.PieceWiseText=self.PieceWiseText+str(i)+",\\newline"
        self.PieceWiseText=self.PieceWiseText+")"  
            

    def DetectElements(self,stems):
        l=len(stems);et=[];er=[];ef=[]
        for i in range(l):
            if stems[i]==1:et.append(i)
            if i>0:
                if And(stems[i-1]==0,stems[i]==1):er.append(i)
            if i<l-1:
                if And(stems[i]==1,stems[i+1]==0):ef.append(i)
        return [et,er,ef]

    def DetectPulses(self,stems):
        l=len(stems);pl=[];pr=[];pf=[];pi=[]
        for i in range(1,l-1):
                
                if And(stems[i-1]==1,stems[i]==1,stems[i+1]==1):pl.append(i)
                if And(stems[i-1]==0,stems[i]==1,stems[i+1]==1):pr.append(i)
                if And(stems[i-1]==1,stems[i]==1,stems[i+1]==0):pf.append(i)
                if And(stems[i-1]==0,stems[i]==1,stems[i+1]==0):pi.append(i)
        return [pl,pr,pf,pi]


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

            
    def UnionElements(self,Inputs):
        L1=len(Inputs)
        temp=[]
        for j in range(L1):temp.append(Inputs[j])
        return max(temp)            
            
    def InvertElement(self,Input):
        if Input==0:return 1
        else:return 0
    
    def EmptyStem(self):
        return list(np.zeros(len(self.stems)))
        
    def UniverseStem(self):
        return list(np.ones(len(self.stems)))
        

