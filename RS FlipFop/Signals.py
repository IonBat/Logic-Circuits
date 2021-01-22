# -*- coding: utf-8 -*-
"""
Created on Monday Dec 19, 2016 8:58:00

@author: Celso Co
"""

#Library

from ccoLatex01 import *  #This is the library for Python-Tex coding.

from matplotlib.pyplot import figure, show, axes, text, cla, draw, annotate
from matplotlib.pyplot import subplots_adjust, plot, subplot, gca, axis
from matplotlib.pyplot import show, stem, setp, hist, savefig, legend

from numpy import linspace, sqrt, zeros, ones

from sympy import And, Or, Function, symbols, var, Piecewise, Union, \
                  Intersection, Matrix, Eq, Ne, subsets
#initialize the PyLx as class PyLatex


Symposium="International Research Journal on Innovations in Engineering (IRJIEST) 2021"
title="\\textrm {Set Theory Foundation for the Description of \\\ SR Flipflop \
       Digital Circuits and Signals}"

#End To be filled by the user


author_data=[["Engr Celso Bation Co, Ph.D, PECE,~\IEEEmembership{Member,~IEEE}",
              "Electronics, Instrumentation \& Control Mechatronics Engineering",
              "Batangas State University",
              "Batangas City, Philippines",
              "celso.co@g.batstate-u.edu.ph"]
             ]

thanks_data=["Electronics, Instrumentation \& Control Mechatronics Engineering, \
             \\newline Batangas State University"]
#End To be filled by the user



thanks=""
for i in thanks_data:
    thanks+="\\IEEEcompsocthanksitem "+str(i)+"\n"

authors="";count=0
temp=""
ln=len(author_data)
for i in range(ln):
    temp="\
\\IEEEauthorblockN{ "+author_data[i][0]+"} \\\ \n\
\\IEEEauthorblockA{\\textit{"+author_data[i][1]+"} \\\ \n\
\\textit{"+author_data[i][2]+"}\\\ "+author_data[i][3]+" \\\ \n"+\
author_data[i][4]+"} \\\ \ \\\ \n"
    if i !=ln-1:temp+="\\and  \n"
 
    authors+=temp


PyArt=PyArticle(Headers="\
\\documentclass[10pt,journal]{IEEEtran} \n\
\\IEEEoverridecommandlockouts \n\
% {The preceding line is only needed to identify funding in the \
   first footnote. If that is unneeded, please comment it out.} \n\
\\usepackage[utf8]{inputenc} \n\
\\usepackage{longtable} \n\
\\usepackage{cite}  \n\
\\usepackage{amsmath,amssymb,amsfonts} \n\
\\usepackage{algorithmic} \n\
\\usepackage{makeidx}\n\
\\usepackage{graphicx} \n\
\\usepackage{textcomp} \n\
\\usepackage{xcolor} \n\
\\usepackage{graphicx}\n\
\\usepackage{float}\n\
\\usepackage{multicol}\n\
\\usepackage{ifpdf}\n\
\\usepackage{tikz} \n\
\\usepackage{parskip} \n\
\\usepackage[siunitx, american]{circuitikz}\n\
\\usetikzlibrary{automata, positioning, shapes, arrows} \n\
\\ifpdf\n\
\\usepackage[breaklinks,hidelinks]{hyperref}\n\
\\else \n\
\\usepackage{url}\n\
\\fi\n\
\\def\BibTeX{{\\rm B\\kern-.05em{\\sc i\\kern-.025em b}\\kern-.08em \n\
    T\\kern-.1667em\\lower.7ex\\hbox{E}\\kern-.125emX}} \n\
\\usepackage{parskip} \n\
\\begin{document} \n\
\\title{"+title+"\\\  \n\
%{\\footnotesize \\textsuperscript{*}Note: Sub-titles are not captured in Xplore \
and should not be used} \n\
\\thanks{"+thanks+"}} \n\
\\author{"+authors+" }\n\
\\maketitle  \n\
\\markboth{"+Symposium+"}%\n\
    {Shell \\MakeLowercase{\\textit{et al.}}: Bare Advanced Demo of \
    IEEEtran.cls for IEEE Computer Society Journals}\n")


#Handlers Shortcuts
#Shortcut Handlers

At=PyArt.Append_Text              #Append Frame variable
Ae=PyArt.Append_Expression        #Short cut for Append_Expression
Ce=PyArt.Append_Equation          #Short cut for Append_Equation
Af=PyArt.Append_Figure            #Short cut for Append_Figurge
Ad=PyArt.Append_Var_Dictionary    #Short cut for Append_Var_Dictionary
Pb=PyArt.Build                    #Build Latex File
Ml=PyArt.Math_Latex               #Convert text to Math Latex 
eQ=PyArt.eQ                       #Equation List
tD=PyArt.TxData                   #Text List
vD=PyArt.vD                       #Variable Dictionary     

Lx=latex


#Content

class DiscreteSignal:
    
    def __init__(self,  stream, start=0, res=1):
        self.start=start
        self.res=res
        self.stream=stream
        self.nt=[]
        self.PW=[]
        self.top=[]
        self.rise=[]
        self.delay_rise=[]
        self.impulse_up=[]
        self.bottom=[]
        self.fall=[]
        self.delay_fall=[] 
        self.impulse_down=[]
        self.transition=[]
        self.stems=self.GenStem()
        self.PWText=self.GenTextPiecewise()
        self.Pulses=self.GenPulses()
        self.StemTimePoints=self.GenStemTimePoints()
        
         
    def GenTextPiecewise(self,stream=[],startime=0):
        if stream==[]:
            stream=self.stream;
        if stream[0] == 0:
            start=0
            otherwise=1
        elif stream[0] == 1:
            start=1
            otherwise=0
        else:
            return "Initial value of stream must be either 0 or 1"
            
        ln=len(stream)
        x="Piecewise(("+str(start)+\
        ", And("+str(startime)+"<= t, t < "+str(stream[1]+startime)+") "
        for i in range(2,ln-1,2):
            x+= " | And("+str(stream[i]+startime)+"<= t, t < "+str(stream[i+1]+startime)+") "
        x+="),("+str(otherwise) + ", True))" 
        self.PWText=x
        return x

    def GenPiecewiseStem(self, PW, length):
        temp=[]
        for i in range(length):
            temp.append(PW.subs(t,i))
        self.PW=PW
        self.stems=temp
        self.nt=linspace(0,len(temp)-1,len(temp))
        return temp                

    def GenStem(self,stream=[]):
        if stream ==[]:stream=self.stream
        if stream[0] == 0:start=0
        elif stream[0] == 1:
            start=1
            stream[0]=0
        stems=[];
        for i in range(len(stream)-1):
            level=(start+i)%2
            for j in range(stream[i],stream[i+1]):
                    stems.append(level)
                 
        stream[0]=start            
        self.stems=stems 
        self.nt=linspace(0,len(stems)-1,len(stems))           
        return stems
    
    def GenStemTimePoints(self,stems=[]):
        if stems==[]:stems=self.stems
        ls=len(stems)
        TimePoints=[]
        for i in range(ls):
            if stems[i]==1:TimePoints.append(i)
        return TimePoints
    
    def OR_Stem(self,stems2,stems1=[]):
        if stems1==[]:stems1=self.stems        
        ln=min(len(stems1),len(stems2))    
        stems3=[]
        for i in range(ln):
            if Or(stems1[i] , stems2[i]):v=1
            else:v=0
            stems3.append(v)
        return stems3
    
    def AND_Stem(self,stems2,stems1=[]):
        if stems1==[]:stems1=self.stems        
        ln=min(len(stems1),len(stems2))    
        stems3=[]
        for i in range(ln):
            if And(stems1[i] , stems2[i]):v=1
            else:v=0
            stems3.append(v)
        return stems3
    
    def INVERT_Stem(self,stems1=[]):
        if stems1==[]:stems1=self.stems        
        ln=len(stems1)    
        stems=[]
        for i in range(ln):
            if stems1[i] == 0:v=1
            else:v=0
            stems.append(v)
        return stems
 
    def GenPulses(self,stems=[]):
        if stems==[]:
            stems=self.stems
            sw=1
        else:
            sw=0
        bottom=[];rise=[];delay_rise=[];impulse_up=[]
        top=[];fall=[];delay_fall=[];impulse_down=[];transition=[];
        sequence=[]
        for i in range(1,len(stems)-1):
            if And(stems[i-1]==0,stems[i]==0,stems[i+1]==0):
                bottom.append(i)
            elif And(stems[i-1]==0,stems[i]==1,stems[i+1]==1):
                rise.append(i)
                transition.append(i)
            elif And(stems[i-1]==0,stems[i]==0,stems[i+1]==1):
                delay_rise.append(i)
            elif And(stems[i-1]==0,stems[i]==1,stems[i+1]==0):
                impulse_up.append(i)
                transition.append(i)
            elif And(stems[i-1]==1,stems[i]==1,stems[i+1]==1):
                top.append(i)
            elif And(stems[i-1]==1,stems[i]==0,stems[i+1]==0):
                fall.append(i)
                transition.append(i)
            elif And(stems[i-1]==1,stems[i]==1,stems[i+1]==0):
                delay_fall.append(i)
            elif And(stems[i-1]==1,stems[i]==0,stems[i+1]==1):
                impulse_down.append(i)
                transition.append(i)
        if sw:
            self.top=top
            self.rise=rise
            self.delay_rise=delay_rise
            self.impulse_up=impulse_up
            self.bottom=bottom
            self.fall=fall
            self.delay_fall=delay_fall
            self.impulse_down=impulse_down
            self.transition=transition
        
        return [top,    rise, delay_rise, impulse_up, 
                bottom, fall, delay_fall, impulse_down, transition]
                
    def GenStream(self,stems):
        L=len(stems)
        ls=stems[0]
        if ls == 0:stream=[0]
        else:stream=[1]
        
        for i in range(1,L):
            if stems[i-1] != stems[i]:
                stream.append(i)
         
        stream.append(L)    
        return stream



    def SR_FF_Stems(self,S,R):
        L=min(len(S),len(R))
        QS=list(zeros(L))
        IQS=list(ones(L+1))
        QR=list(ones(L))
        IQR=list(zeros(L+1))

        for i in range(L):
            if S[i] + IQR[i] > 0:
                QS[i]=1
            elif S[i] + IQR[i] == 0:
                QS[i]=0
            if R[i] + IQS[i] > 0:
                QR[i]=1
            elif R[i] + IQS[i] == 0:
                QR[i]=0
            if QS[i]==1:
                IQS[i]=0
                IQS[i+1]=0
            else:
                IQS[i]=1
                IQS[i+1]=1
            if QR[i]==1:
                IQR[i]=0
                IQR[i+1]=0
            else:
                IQR[i]=1
                IQR[i+1]=1
           
        return QS, QR




def SymbolicVariableText(v):  
    p=v;p1="s"+p    
    vpulses=var(p1+" "+p1+"top "+p1+"rise "+p1+"up "+p1+"bottom "+p1+"fall "+
                p1+"down "+p1+"transition "+p1+"stream "+p1+"delay_rise "+
                p1+"delay_fall "+p1+"inv")
    spulses=p+" "+p+"_{\\sqcap} "+p+"_{\\nearrow} "+p+"_{\\bot} "+\
            p+"_{\\sqcup} "+p+"_{\\searrow} "+p+"_{\\top} "+p+"_{|} "+p+"_{stream} "+\
            p+"_{.\\nearrow} "+p+"_{^.\\searrow} "+"\\overline{"+p+"}"
    return str(vpulses)+"=symbols(r\""+spulses+"\")"

def FunctionVariableText(v):
    p=v;p1="f"+p    
    vpulses=var(p1+" "+p1+"top "+p1+"rise "+p1+"up "+p1+"bottom "+p1+"fall "+
                p1+"down "+p1+"transition "+p1+"stream "+p1+"delay_rise "+
                p1+"delay_fall "+p1+"inv")
    spulses=[p,p+"_{\\sqcap}",p+"_{\\nearrow}",p+"_{\\bot}",p+"_{\\sqcup}",
               p+"_{\\searrow}",p+"_{\\top}",p+"_{|}",p+"_{stream}",
               p+"_{.\\nearrow}",p+"_{^.\\searrow}","\\overline{"+p+"}"]
    ln=len(vpulses)
    fText=""
    for i in range(ln): 
        fText+=str(vpulses[i])+"=Function(r\""+spulses[i]+"\"); "
    return fText    


def SignalTable(T,DS,size="\\footnotesize"):
    table="\
\\begin{table}[H] \\caption{"+T+"}\
\\centering\
\\begin{tabular}{|p{.4cm}|p{.5cm}|p{6.5cm}|}\
\\hline Item&Pulse &Stem Set\\\ \
\\hline 00& "+size+Ml(stop)          +" & "+size+str(DS.top)+"\\\ \
\\hline 01& "+size+Ml(sbottom)       +" & "+size+str(DS.bottom)+"\\\ \
\\hline 02& "+size+Ml(srise)         +" & "+size+str(DS.rise)+"\\\ \
\\hline 03& "+size+Ml(sfall)         +" & "+size+str(DS.fall)+"\\\ \
\\hline 04& "+size+Ml(simpulse_up)   +" & "+size+str(DS.impulse_up)+"\\\ \
\\hline 05& "+size+Ml(simpulse_down) +" & "+size+str(DS.impulse_down)+"\\\ \
\\hline 06& "+size+Ml(sdelay_rise)   +" & "+size+str(DS.delay_rise)+"\\\ \
\\hline 07& "+size+Ml(sdelay_fall)   +" & "+size+str(DS.delay_fall)+"\\\ \
\\hline 08& "+size+Ml(stransition)    +" & "+size+str(DS.transition)+"\\\ \
\\hline \\end{tabular} \\end{table} "      
    return table

setVar=["A","B","C","D", "In", "Out", "S", "R", "QS", "QR"]

for i in setVar:
    sv=SymbolicVariableText(i)
    exec(sv)
    fv=FunctionVariableText(i)
    exec(fv)


   
ftop          = Function("\\sqcap")
fbottom       = Function("\\sqcup")
ffall         = Function("\\downarrow")
frise         = Function("\\uparrow")
fimpulse_up   = Function("\\bot")
fimpulse_down = Function("\\top")
finv          = Function("I_{nv}")
fdelay        = Function("D_{elay}")
fsignal       = Function("S_{ignal}")
fstream       = Function("S_{tream}")
ftransition   = Function("|")
fprior        = Function("P_{rior}")
fpost         = Function("P_{ost}") 
fstem         = Function("S_{tem}")
fpulse        = Function("P_{ulse}")

stop,   sbottom, sfall,    srise,    simpulse_up, simpulse_down, transition, t = symbols("\
\\sqcap \\sqcup  \\searrow \\nearrow \\bot        \\top          |     t           ")

sdelay_rise, sdelay_fall, sprior,  spost,  sstem   ,spulse    = symbols("\
.\\nearrow   ^.\\searrow  P_{rior} P_{ost} S_{tem}  P_{ulse}            ")

stop_unit_pulse,    sbottom_unit_pulse,  stransition, ssignal, sstream, dots  = symbols("\
\\nearrow\\searrow  \\senarrow\\nearrow  |            Signal   Stream   \\dots          ")

etop, ebottom, efall, erise = symbols("\
||    ..       |.     .|              ")

ptop, pbottom, pfall, prise, pdelay_fall, pdelay_rise, pimpulse_up, pimpulse_down = symbols("\
|||   ...      |..    .||    ||.          ..|          .|.          |.|                     ")



#Begin to be filled by user

#Abstract
Abstract="\
The SR (Set/Reset) Flipflop was the basic component of digital logic cirtcuits. \
There exists certain problem in articulating the behaviour of its circuits and \
signals characteristics from theoretical perspective. Although the cross couple \
OR gate with Inverter circuit had long been established, there existed a \
curiosity whether it can be synthersized out of the analysis of the input and \
output signals of SR Flipflop Gate. The characteristics of digital signal \
pulses was studied with the set theory as the working paradigm. The classification \
of pulses was designed taking into consideration the changes of logic state in \
an event. The prior and post event were conceptualized that provided meaningful \
platform of the pulses classification. The relation and equation of set theory were \
instrumental in the construction of simple latch and SR flipflop circuits. \
The signal behaviors were shown consistent with the design equations for  \
prior and post events. The operation of set theory on symbolic pulses were consistent."      


#End to be filled by user

At("\\begin{abstract}"+Abstract+"\\end{abstract}")
    

#Begin to be filled by user
#Keywords
Keywords=\
   "set theory, prior event, post event, pulse classification, SR flipflop, \
    simple latch, OR Gate, Inverter "
#End to be filled by user

At("\\begin{IEEEkeywords}"+Keywords+"\\end{IEEEkeywords}")
   
stream =[0, 5,  10, 15, 17, 23, 24, 34, 39, 40, 45, 50, 55, 57, 67, 75,  80]

f=Function("f")


dS=DiscreteSignal(stream)
exec("pwsignal="+dS.GenTextPiecewise())
nstems=dS.GenPiecewiseStem(pwsignal, 80) 
nIstems=dS.INVERT_Stem(nstems)
nt=linspace(0,len(nstems)-1,len(nstems))

print("\nProcessing Figure 1")  

figure(num=1)
subplots_adjust(hspace=1)
#subplot(2,1,1)
ax=gca();cla()
#axis([0,nSignal,-.1,1.5])
ax.set_title("")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(nt,nstems,"b",lw=2)

ax.text(4,1.0,"Top \nPulses\n $\\downarrow$")
ax.text(13,1.0,"Top \nUnit\nPulse\n $\\downarrow$")
ax.text(20.5,1.0,"Top \nImpulse\n $\\downarrow$")
ax.text(36.5,1.0,"Bottom \nImpulse\n $\\downarrow$")
ax.text(53,1.0,"Bottom \n Unit\nPulse\n $\\downarrow$")
ax.text(69,1.0,"Bottom \nPulses\n $\\downarrow$")
ax.text(25,.6,"Rise $\\rightarrow$\nPulse")
ax.text(66,.6,"$\\leftarrow$")
ax.text(68,.6,"Fall \nPulse")





savefig("FG001.png")



#1.0 Preliminary

At("\\section{Preliminary}")

At("Consider the piecewise signal as follows.")


exec("PWstream="+dS.PWText)


Ce(fsignal(t), PWstream)                                                       #1
ltD=len(tD);a=tD[ltD-1]
tD[ltD-1]=tD[ltD-1].replace("&","& \\\ ").\
    replace("15\\right)","15\\right) \\\ \\quad \ \ ").\
    replace("34\\right)","34\\right) \\\ \\quad \ \ ").\
    replace("50\\right)","50\\right) \\\ \\quad \ \ ").\
    replace("17\\right)","17\\right) \\\ \\quad \ \ ").\
    replace("39\\right)","39\\right) \\\ \\quad \ \ ").\
    replace("55\\right)","55\\right) \\\ \\quad \ \ ").\
    replace("80\\right)","80\\right) \\\ \\quad \ \ ")

At("The signal(t) could be expressed in term of set of unit time when logic \
    transition occurred. The transition could be either from 0 to 1 or 1 to 0. \
    It depended on the initial logic state. The initial logic state was  \
    either 0 or 1 at the first item of the list. For this case, the initial \
    state was 0 or say stream[0]=0. Thereafter stream[5]=1, stream[10]=0, \
    stream[15]=1 and so on. The symbol | represened the transition edge at specified \
    domain unit.")

Ae("stream(|) = "+str(stream));Ad(key="stream")                                #2
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("=","= \\newline ")

   
Istream =[1, 5,  10, 15, 17, 23, 24, 34, 39, 40, 45, 50, 55, 57, 67, 75,  80]

At("The inverse of "+vD["stream"][0][1]+" looked the same as "+vD["stream"][0][1]+
   " except for stream[0]=1. See Figure 2 \"Inverse of Stream\" plot. Hence." ) 
   
Ae("Inverse(stream(|))  = "+str(Istream))                                      #3                                       #2
ltD=len(tD)
#tD[ltD-1]=tD[ltD-1].replace("55","55 \\newline ")

At("The signal(t) was plotted in Figure 1. The annotations were Top Pulses, \
   Top Unit, Top Impulse, Rise Pulse, Bottom Impulse, Bottom Unit Pulse, \
   Fall Pulse, and Bottom Pulses. \
   \\\ \ \\\ \
   The stem plot of Figure 1 is shown in Figure 2 with the same annotations. ")

Af("FG001.png",caption="Classification of Pulses",height=.15)



print("Processing Figure 2")

figure(num=2)
subplots_adjust(hspace=1)

subplot(2,1,1)
ax=gca();cla()
#axis([0,nSignal,-.1,1.5])
ax.set_title("Inverse of Stream")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(nt,nIstems,"b",lw=2)


subplot(2,1,2)
ax=gca();cla()
ax.set_title("")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
stem(nt,nstems,use_line_collection=True)
#stem(nt,nSignal)


ax.text(4,1.0,"Top \nPulses\n $\\downarrow$")
ax.text(13,1.0,"Top \nUnit\nPulse\n $\\downarrow$")
ax.text(20.5,1.0,"Top \nImpulse\n $\\downarrow$")
ax.text(36.5,1.0,"Bottom \nImpulse\n $\\downarrow$")
ax.text(53,1.0,"Bottom \n Unit\nPulse\n $\\downarrow$")
ax.text(69,1.0,"Bottom \nPulses\n $\\downarrow$")
ax.text(25,.6,"Rise $\\rightarrow$\nPulse")
ax.text(66,.6,"$\\leftarrow$")
ax.text(68,.6,"Fall \nPulse")


savefig("FG002.png")
Af("FG002.png",caption="Inverse and Stem Plot of Figure 1",height=.15)


#1.1 Definition

At("\\subsection{Definition}")

At("The logic level at a given point in time is either low (.) or high \
   ($\\vert$) called stem. The event was represented by a couple of points in \
    time and defined in Table 1." )

At("\
\\begin{table}[H] \\caption{Event Classification}\
\\centering\
\\begin{tabular}{|p{.4cm}|p{2cm}|p{1cm}|p{1cm}|p{1.5cm}|}\
\\hline Item&Event Description &Stem Symbol&Stem Values &Remarks\\\ \
\\hline 00& low      &"+Ml(ebottom) +" &[0,0] &no change\\\ \
\\hline 01& rise     &"+Ml(erise)   +" &[0,1] &change\\\ \
\\hline 02& fall     &"+Ml(efall)   +" &[1,0] &change\\\ \
\\hline 03& high     &"+Ml(etop)    +" &[1,1] &no change\\\ \
\\hline \\end{tabular} \\end{table} ")      


   
At("Let a tuple of 3 units of time be defined as follows. \
    Tri-unit = \{prior, current, post\} = \{t-1, t, t+1\} = t where the t \
    could be used as the name of the set, e.g. 25 = \{24,25,26 \}. The anchor \
    was t=25. The prior event of tri-unit was prior = \{t-1, t\}=\{24,25\} while \
    the post event of it was post = \{t,t+1\}=\{25,26\}. The pulse clasification \
    and their symbols were shown in Table II.")




At("\
\\begin{table}[H] \\caption{Symbolic Pulses Classification}\
\\centering\
\\begin{tabular}{|p{.4cm}|p{1.6cm}|p{.9cm}|p{.9cm}|p{.8cm}|p{.5cm}|p{.5cm}|}\
\\hline Item&Pulse Description &Pulse Symbol&Stem Symbol&Stem Values \
                       &Prior Event&Post Event            \\\   \
\\hline 00& bottom       &"+Ml(sbottom)      +" &"+Ml(pbottom)      +" &[0,0,0] \
                         &"+Ml(ebottom)      +" &"+Ml(ebottom)+" \\\ \
\\hline 01& delay rise   &"+Ml(sdelay_rise)  +" &"+Ml(pdelay_rise)  +" &[0,0,1] \
                         &"+Ml(ebottom)      +" &"+Ml(erise)+" \\\ \
\\hline 02& fall         &"+Ml(sfall)        +" &"+Ml(pfall)        +" &[1,0,0] \
                         &"+Ml(efall)        +" &"+Ml(ebottom)+"\\\ \
\\hline 03& impulse (-)  &"+Ml(simpulse_down)+" &"+Ml(pimpulse_down)+" &[1,0,1] \
                         &"+Ml(efall)        +" &"+Ml(erise)+"\\\ \
\\hline 04& impulse (+)  &"+Ml(simpulse_up)  +" &"+Ml(pimpulse_up)  +" &[0,1,0] \
                         &"+Ml(erise)        +" &"+Ml(efall)+"\\\ \
\\hline 05& rise         &"+Ml(srise)        +" &"+Ml(prise)        +" &[0,1,1] \
                         &"+Ml(erise)        +" &"+Ml(etop)+"\\\ \
\\hline 06& delay fall   &"+Ml(sdelay_fall)  +" &"+Ml(pdelay_fall)  +" &[1,1,0] \
                         &"+Ml(etop)         +" &"+Ml(efall)+"\\\ \
\\hline 07& top          &"+Ml(stop)         +" &"+Ml(ptop)         +" &[1,1,1] \
                         &"+Ml(etop)         +" &"+Ml(etop)+"\\\ \
\\hline \\end{tabular} \\end{table} ")      




At("Let following functions be defined.")

Ce(fprior(spulse),(t-1,t))                                                     #4
Ce(fpost(spulse),(t,t+1))                                                      #5  
Ce(fpulse(spulse),(t-1,t,t+1))                                                 #6 
Ce(Eq(fpulse(spulse),fprior(spulse)+fpost(spulse)),(t-1,t,t+1))                #7 
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+"," \\cup ")

At("For example,"+Ml(Eq(fprior(srise),erise))+" and "+Ml(Eq(fpost(srise),etop))+
    " and "+Ml(Eq(fpulse(srise),prise))+", the anchor is the common element t. \\\ \ \\\ \
    The inverse function was the compliment of the signal and the overline \
    represent the inverse made.")

stopinv=var("\\overline"+str(stop))
simpulse_downinv=var("\\overline"+str(simpulse_down))

Ce(sbottom,Eq(finv(stop),stopinv));Ad()                                        #8     
Ce(simpulse_up, Eq(finv(simpulse_down),simpulse_downinv));Ad()                 #9 

   
At("The definition of pulses in terms of tri-unit of time ensured that the \
    logic state change occurred during the prior event. When there was no\
    change in prior event but a change occurred in post event, the pulse \
    was said to be delayed. The presence of the dot before the symbol indicated \
    the delay.\\\ \ \\\ ")
   
At("The top unit pulse was a sequence of the rise event followed by fall event. \
    It was a sequence of pulses, ["+Ml(srise)+","+Ml(sdelay_fall)+". ") 
Ce(Eq(stop_unit_pulse,(0,1,1,0)),(srise,sdelay_fall));Ad()                     #10                                              
At("In like manner bottom unit pulse,")               
Ce(Eq(finv(stop_unit_pulse),(1,0,0,1)),(sfall,sdelay_rise));Ad()               #11
At("The positive impulse was an intersection of rise pulse "+Ml(srise)+
   " and delayed fall "+ Ml(sdelay_fall)+".")                                                              
Ae(latex(simpulse_up)+" = "+latex(srise)+" \\cap " +latex( sdelay_fall))       #12
At("The negative impulse was a union of "+Ml(sfall)+" and "+ 
   Ml(sdelay_rise)+".")
Ae(latex(simpulse_down)+" = "+latex(sfall)+" \\cup " +latex(sdelay_rise))      #13 
At("The transition pulses were changes in logic state either 0 to 1 or 1 to 0 \
    at prior event. The change at post event without change at prior event was \
    a delayed transition.")
Ae(latex(stransition)+" = ("+latex(srise)+", "+latex(sfall)+", "+
   latex(simpulse_up)+","+latex(simpulse_down)+")")                            #14    

At("The plots for the eigth categories of pulses were illustrated in Figure 3.")


print("Processing Figure 3")
figure(num=3,figsize=(20,8))
subplots_adjust(hspace=1)

nt=[-1, 0, 1]
tp=[ 1, 1, 1]

subplot(4,2,1)
ax=gca();cla()
ax.set_title("(a) The Stem Plot of a Pulse = "+Ml(stop))
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(nt,tp,color=[0,1,0])
stem(nt,tp,use_line_collection=True)


itp=[0, 0, 0]

subplot(4,2,2)
ax=gca();cla()
ax.set_title("(b) The Stem Plot of the Inverse Pulse = "+Ml(Eq(finv(stop),sbottom)))
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
stem(nt,itp,use_line_collection=True)
plot(nt,itp,color=[0,1,0])

rp=[ 0, 1, 1]

subplot(4,2,3)
ax=gca();cla()
ax.set_title("(c) The Stem Plot of a Rise = "+Ml(srise))
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
stem(nt, rp,use_line_collection=True)
plot(nt, rp,color=[0,1,0])

irp=[1, 0, 0]

subplot(4,2,4)
ax=gca();cla()
ax.set_title("(d) The Stem Plot of an Inverse of Rise = "+Ml(Eq(finv(srise),sfall)))
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
stem(nt,irp,use_line_collection=True)
plot(nt,irp,color=[0,1,0])

fp=[1, 0, 0]

subplot(4,2,5)
ax=gca();cla()
ax.set_title("(e) The Stem Plot of a Fall = "+Ml(sfall))
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
stem(nt,fp,use_line_collection=True)
plot(nt,fp,color=[0,1,0])

ifp=[0, 1, 1]

subplot(4,2,6)
ax=gca();cla()
ax.set_title("(f) The Stem Plot of a Inverse Fall = "+Ml(Eq(finv(sfall),srise)))
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
stem(nt, ifp,use_line_collection=True)
plot(nt, ifp,color=[0,1,0])

ip=[0, 1, 0]


subplot(4,2,7)
ax=gca();cla()
ax.set_title("(g) The Stem Plot of an Impulse = "+Ml(simpulse_up))
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
stem(nt,ip,use_line_collection=True)
plot(nt,ip,color=[0,1,0])


iip=[1, 0, 1]

subplot(4,2,8)
ax=gca();cla()
ax.set_title("(h) The Stem Plot of an Inverse of Impulse = "+
             Ml(Eq(finv(simpulse_up),simpulse_down)))
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
stem(nt,iip,use_line_collection=True)
plot(nt,iip,color=[0,1,0])


savefig("FG003.png")

Af("FG003.png",caption="Type of Pulses Categorized by the Logic State \
of the Left and Right Adjacent Unit of time",height=.35)

#1.1 Expression

At("\\subsection{Expression}")

At("The pulse symbol could be an expression of function. The list of pulses \
    in a signal was expressed as follows.")
   
Ae(latex(fpulse(ssignal))+" = [t_{a},t_{b},t_{c},... ,t_{n-1},t_{n},t_{n+1}, \
   t_{k}, ...]")                                                               #15
At("where $t_{n-1}=1,t_{n}=1,t_{n+1}=1$ \\\ \ \\\ \
For example,")

Ae(latex(ftop(ssignal))+" = "+str(dS.top));Ad(key=stop)                        #16
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("59,","59, \\newline ") 

At("For t=35 from "+vD[stop][0][1]+", ")
Ae(latex(ftop(ssignal))+"[35] = ("+latex(ssignal)+"[34], "+
   latex(ssignal)+"[35], "+ latex(ssignal)+"[36])"+" = (1,1,1)");Ad(key=stop)  #17 

At("Another example,")
Ae(latex(frise(ssignal))+"[34] = ("+latex(ssignal)+"[33], "+
   latex(ssignal)+"[34], "+ latex(ssignal)+"[35])"+" = (0,1,1)");Ad(key=srise) #18 

At("The union of "+vD[stop][1][1]+" and "+vD[srise][0][1]+", ")

Ce(frise(fsignal(34))+ftop(fsignal(35)),{srise,stop})                          #19
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+"," \\cup ")

At("A signal could be expressed as list of symbolic pulses. Hence, given \\\ ")


At("A = \\begin{tabular}{p{6cm}}\
      [0,  \#  A[ 0]=undefined\\\ \
      \ 0,  \#  A[ 1]="+Ml(sbottom)+"\\\ \
      \ 0,  \#  A[ 2]="+Ml(sdelay_rise)+"\\\ \
      \ 1,  \#  A[ 3]="+Ml(srise)+"\\\ \
      \ 1,  \#  A[ 4]="+Ml(stop)+"\\\ \
      \ 1,  \#  A[ 5]="+Ml(sdelay_fall)+"\\\ \
      \ 0,  \#  A[ 6]="+Ml(sfall)+"\\\ \
      \ 0,  \#  A[ 7]="+Ml(sbottom)+"\\\ \
      \ 0,  \#  A[ 8]="+Ml(sdelay_rise)+"\\\ \
      \ 1,  \#  A[ 9]="+Ml(simpulse_up)+"\\\ \
      \ 0,  \#  A[10]="+Ml(sfall)+"\\\ \
      \ 0,  \#  A[11]="+Ml(sbottom)+"\\\ \
      \ 0,  \#  A[12]="+Ml(sdelay_rise)+"\\\ \
      \ 1,  \#  A[13]="+Ml(srise)+"\\\ \
      \ 1,  \#  A[14]="+Ml(sdelay_fall)+"\\\ \
      \ 0,  \#  A[15]="+Ml(simpulse_down)+"\\\ \
      \ 1,  \#  A[16]="+Ml(srise)+"\\\ \
      \ 1,  \#  A[17]="+Ml(sdelay_fall)+"\\\ \
      \ 0,  \#  A[18]="+Ml(sfall)+"\\\ \
      \ 0,  \#  A[19]="+Ml(sdelay_rise)+"\\\ \
      \ 1,  \#  A[20]="+Ml(srise)+"\\\ \
      \ 1,  \#  A[21]="+Ml(sdelay_fall)+"\\\ \
      \ 0,  \#  A[22]="+Ml(sfall)+"\\\ \
      \ 0,  \#  A[23]="+Ml(sbottom)+"\\\ \
      \ 0   \#  A[24]=undefine ]\
        \\end{tabular} \\\ \ \\\ ")

At("The sequence of pulses in A were ["+
    Ml(sbottom)+    ", "+Ml(sdelay_rise)+", "+Ml(srise)+        ", "+Ml(stop)+       ", "+
    Ml(sdelay_fall)+", "+Ml(sfall)+      ", "+Ml(sbottom)+      ", "+Ml(sdelay_rise)+", "+
    Ml(simpulse_up)+", "+Ml(sfall)+      ", "+Ml(sbottom)+      ", "+Ml(sdelay_rise)+", "+
    Ml(srise)+      ", "+Ml(sdelay_fall)+", "+Ml(simpulse_down)+", "+Ml(srise)+", "+
    Ml(sdelay_fall)+", "+Ml(sfall)+      ", "+Ml(sdelay_rise)+  ", "+Ml(srise)+", "+
    Ml(sdelay_fall)+", "+Ml(sfall)+      ", "+Ml(sbottom)+      "]   ")

#2.0 Signal Sets

At("\\section{Signal Sets}")

At("Let's examine the of signal sets behavior in both open and closed systems \
    logic circuit. The open loop system was a feed forward and without a feedback. \
    The closed system has feedback loop.")

#2.1 Combinatory Logic: an Open Loop system
At("\\subsection{Combinatory Logic: Open Loop System}")

At("A given set of signals had a combinations of a number of pulses, impulses, \
   rising and falling edges and their inverses. It could also be said that any \
   signal was a set of time points of stems. A stem represented an impulse. \
   Two consecutive stems represent a rising and a falling pulse. Three \
   consecutive stems makes a pulse. A stem was identified by its location in \
   time domain. A point in time could be classified as a pulse, a rising edge, \
   a falling edge, an impulse and their inverses depending on the changes of its \
   prior and post events. A stem was defined as logic state 1 at a point \
   in time domain.\\\ \ \\\ \
   Consider the followins signals ")


Astream=[0, 4, 8, 11, 12, 15, 20, 22, 23, 31, 34, 38, 48, 50]
cA=DiscreteSignal(Astream)
cA.PWText=cA.GenTextPiecewise()
exec("PwSignalA="+cA.PWText)
nAstems=cA.GenPiecewiseStem(PwSignalA, 55) 
ntA=linspace(0,len(nAstems)-1,len(nAstems))


Ce(fA(t),PwSignalA)                                                            #20
ltD=len(tD);a=tD[ltD-1]
tD[ltD-1]=tD[ltD-1].replace("&","& \\\ ").\
    replace("11\\right)","11\\right) \\\ \\quad \ \ ").\
    replace("22\\right)","22\\right) \\\ \\quad \ \ ").\
    replace("38\\right)","38\\right) \\\ \\quad \ \ ").\
    replace("12\\right)","12\\right) \\\ \\quad \ \ ").\
    replace("23\\right)","23\\right) \\\ \\quad \ \ ")       



tableA=SignalTable("Signal A Pulses",cA)
At(tableA)


Bstream=[1, 2, 7,  9, 18, 25, 26, 28, 30, 36,  40, 42, 43, 46,  50]
cB=DiscreteSignal(Bstream)
cB.PWText=cB.GenTextPiecewise()
exec("PwSignalB="+cB.PWText)
nBstems=cB.GenPiecewiseStem(PwSignalB, 55) 
ntB=linspace(0,len(nBstems)-1,len(nBstems))

Ce(fB(t),PwSignalB)                                                            #21
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("&","& \\\ ").\
    replace("18\\right)","18\\right) \\\ \\quad \ \ ").\
    replace("30\\right)","30\\right) \\\ \\quad \ \ ").\
    replace("43\\right)","43\\right) \\\ \\quad \ \ ").\
    replace("25\\right)","25\\right) \\\ \\quad \ \ ").\
    replace("36\\right)","36\\right) \\\ \\quad \ \ ")  
  

tableB=SignalTable("Signal B Pulses",cB)
At(tableB)


nCstems=cA.OR_Stem(cB.stems)
nCstream=cA.GenStream(nCstems)
cC=DiscreteSignal(nCstream)
ntC=linspace(0,len(nCstems)-1,len(nCstems))

#for i in range(len(nCstems)):
#    print(nCstems[i],nAstems,nBstems)


tableC=SignalTable("Signal C = A $\\cup$ B Pulses",cC)
At(tableC)


nDstems=cA.AND_Stem(cB.stems)
nDstream=cA.GenStream(nDstems)
cD=DiscreteSignal(nDstream)
ntD=linspace(0,len(nDstems)-1,len(nDstems))

tableD=SignalTable("Signal D = A $\\cap$ B Pulses",cD)
At(tableD)

#for i in range(len(nCstems)):
#    print(nDstems[i],nAstems[i],nBstems[i])


print("Processing Figure 4")

figure(num=4,figsize=(20,15))
subplots_adjust(hspace=1)


subplot(4,1,1)
ax=gca();cla()
ax.set_title("(a) Plot of Signal A")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
#stem(ntiS,niS,use_line_collection=True)
#stem(ntiS,niS)
plot(ntA,nAstems,color=[1,0,0],label="A")
legend()

subplot(4,1,2)
ax=gca();cla()
ax.set_title("(a) Plot of Signal B")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
#stem(ntiS,niS,use_line_collection=True)
#stem(ntiS,niS)
plot(ntB,nBstems,color=[0,0,1],label="B")
legend()

subplot(4,1,3)
ax=gca();cla()
ax.set_title("(b) Plot of Signals A $\\vee$ B")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
#stem(ntiS,niS,use_line_collection=True)
#stem(ntiS,niS)
plot(ntC,nCstems,color=[1,0,0],label="C")
#plot(ntB,nCstems,color=[0,0,1],label="B")
legend()

subplot(4,1,4)
ax=gca();cla()
ax.set_title("(c) Plot of Signals A $\\wedge$ B")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
#stem(ntiS,niS,use_line_collection=True)
#stem(ntiS,niS)
plot(ntD,nDstems,color=[1,0,0],label="C")
#plot(ntD,nDstems,color=[0,0,1],label="D")
legend()



savefig("FG004.png")

Af("FG004.png",caption="Signals A and B and their Union and Intersection \
   Operations",height=.35)



#2.2 Simple Latch: a Closed Loop System
At("\\subsection{Simple Latch: a Closed Loop System}")

At("A closed loop system could be illustrated by a simple latch. It was a system \
    consisting of an input and an output. Initial, the input is at zero logic \
    state and the output was likewise at zero logic state. When a pulse occured, \
    the output latched to logic state 1 and kept it latched irrespective of \
    changes in logic state at the input thereafter. See Figure 5.  Given such \
    signals operating condition, it was desired to derive the simple latch \
    circuit. Its block diagram was shown in Figure 6.\\\ \ \\\ \
    The input signal "+Ml(sIn)+" and the output signal "+Ml(sOut)+" were \
    defined in term of piecewise equation as follows")

In_stream=[0, 3, 4, 7,  9 ,10]
In=DiscreteSignal(In_stream)
exec("PwSignalIn="+In.PWText)
nIn_stems=In.GenPiecewiseStem(PwSignalIn, 10) 
ntIn=linspace(0,len(nIn_stems)-1,len(nIn_stems))

Ce(fIn(t),PwSignalIn)                                                          #22
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("&","& \\\ ").replace("\\vee","\\vee \\\ \ \ \\quad   ")

tableIn=SignalTable("Signal In Pulses",In)
At(tableIn)


Out_stream=[0, 3, 15]
Out=DiscreteSignal(Out_stream)
exec("PwSignalOut="+Out.GenTextPiecewise())
nOut_stems=dS.GenPiecewiseStem(PwSignalOut, 10) 
ntOut=linspace(0,len(nOut_stems)-1,len(nOut_stems))

print("Processing Figure 5")


Ce(fOut(t),PwSignalOut)                                                        #23
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("&","& \\\ ").replace("\\vee","\\vee \\\ \ \ \\quad   ")


tableOut=SignalTable("Signal Out Pulses",Out)
At(tableOut)

figure(num=5,figsize=(20,15))
#subplots_adjust(hspace=1)


subplot(2,1,1)
ax=gca();cla()
ax.set_title("(a) Plot of Simple Latch Signal "+Ml(fIn(t)))
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
#stem(ntE,nEstems,use_line_collection=True)
plot(ntIn,nIn_stems,color=[0,0,1],label=Ml(sIn))
legend()

subplot(2,1,2)
ax=gca();cla()
ax.set_title("(b) Plot of Simple Latch Signal "+Ml(fOut(t)))
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
#stem(ntE,nEstems,use_line_collection=True)
plot(ntOut,nOut_stems,color=[1,0,0],label=Ml(sOut))
legend()


savefig("FG005.png")
Af("FG005.png",caption="Simple Latch",height=.15)


foutfb= Function("In_{fb}")
soutfb= symbols("In_{fb}")



print("Processing Figure 6")


At("\
\\begin{figure}[H]                                                     \n\
   \\centering                                                        \n\
	\\tikzstyle{block} = [draw, fill=white, rectangle,                 \n\
	minimum height=1cm, minimum width=2cm]                             \n\
	\\tikzstyle{input} = [coordinate]                                  \n\
	\\tikzstyle{output} = [coordinate]                                 \n\
	\\tikzstyle{pinstyle} = [pin edge={to-,thin,black}]                \n\
	\\begin{tikzpicture}[auto, node distance=2cm,>=latex']             \n\
	\\node [input, name=input] {};                                     \n\
	\\node [block, right of=input] (Latch) {$Latch$};                  \n\
	\\node [output, right of=Latch] (out) {};                          \n\
	\\draw [draw,->] (-.5,0) node {$In(t)$} (input) -- (Latch);        \n\
	\\draw [draw,->] (Latch) --  (out)  node {};                       \n\
	\\draw (4.75,0) node {$Out(t)$};                                   \n\
    \\end{tikzpicture}                                                 \n\
\\caption{Block Diagram of Simple Latch}                               \n\
\\label{fig:Figure 6}                                                  \n\
\\end{figure}")





At("By observation of Tables VII, VIII and Figure 5, the following relationships \
    were noted.")


Ae(latex(fIntop(t))+" \\subset "+latex(fOuttop(t)),c="constant pulses")        #24
Ad(key=sIntop)        

Ae(latex(fIntransition(t))+" \\supset "+latex(fOuttransition(t)),
   c="changing pulses");Ad(key=sIntransition)                                 #25


At("The circuit could be derived from observed behavior of the relation "+
    vD[sIntop][0][1]+". Since relation had no equivalent real world circuit, \
    it was necessary to determine its equivalent equation as follows.")

Ae(latex(fOut(t))+" = "+latex(fOut(t))+" \\cup "+latex(fIn(t)));Ad(key=fOut)   #26


At("The equation "+vD[fOut][0][1]+" was expressed in terms of set theory. The \
    implementation in hardware circuit of $\\cup$ set operation was the \
    Boolean equation for OR gate. The circuit diagram was shown in Figure 7")

print("Processing Figure 7")

At("\
\\begin{figure}[H]                                                             \n\
    \\centering                                                                \n\
	\\tikzstyle{block} = [draw, fill=white, rectangle,                         \n\
	minimum height=.5cm, minimum width=1cm]                                    \n\
	\\tikzstyle{input} = [coordinate]                                          \n\
	\\tikzstyle{output} = [coordinate]                                         \n\
	\\tikzstyle{pinstyle} = [pin edge={to-,thin,black}]                        \n\
\\begin{circuitikz}                                                            \n\
\\ctikzset{tripoles/american or port/input height=.5}                          \n\
\\node[input,name=P1] {$S$};                                                   \n\
\\begin{scope}                                                                 \n\
\\ctikzset{tripoles/american or port/height=1}                                 \n\
\\draw (-.5,0) node {$"+latex(fIn(t))+"$} (P1) -- (0.5,0)                      \n\
  node[american or port, anchor=in 1] (B) {};                                  \n\
\\end{scope}                                                                   \n\
\\node[output, right of=B, node distance=1cm] (Q) {};                          \n\
\\draw (B) -- (Q) (3.5,-.4) node {$"+latex(fOut(t))+"$};                       \n\
\\node[input, below of =B, node distance=1cm] (fb) {};                         \n\
%\\draw (B.out) |- (fb);                                                       \n\
%\\draw (fb) -| (B.in 2);                                                      \n\
\\node[input,below of = P1, name=P2, node distance=.7cm] {};                   \n\
\\draw (-.7,-.7) node {$"+latex(fOut(t))+"$} (P2) -- (B.in 2);                 \n\
\\end{circuitikz}                                                              \n\
\\caption{OR Gate Circuit Diagram for Simple Latch Equation $"+
          vD[fOut][0][2]+"$}                                                   \n\
\\label{fig:Figure 7}                                                          \n\
\\end{figure}")





At("Since the "+Ml(fOut(t))+" at input terminal of the OR gate was the same "
   +Ml(fOut(t))+" at its output terminal, then the two terminal must be \
   connected as shown in Figure 8. Let the "+Ml(sOut)+" at the input terminal \
   be tag as "+Ml(soutfb)+" keeping in mind "+Ml(Eq(sOut,soutfb))+". Hence, \
   the existing of feed back loop made this circuit closed loop system. The \
   subset relation ($"+vD[sIntop][0][2]+"$) that depicted a feedback \
   equation was indicative of memrory feature. In the sequence of "+
   Ml(fpulse(sIn))+" pulses, the latch happened at "+Ml(fpulse(sOut))+" when \
   a change in "+Ml(fpulse(sIn))+" occurred as shown in Figure 8.")


print("Processing Figure 8")

At("\
\\begin{figure}[H]                                                             \n\
    \\centering                                                                \n\
	\\tikzstyle{block} = [draw, fill=white, rectangle,                         \n\
	minimum height=1.5cm, minimum width=3cm]                                   \n\
	\\tikzstyle{input} = [coordinate]                                          \n\
	\\tikzstyle{output} = [coordinate]                                         \n\
	\\tikzstyle{pinstyle} = [pin edge={to-,thin,black}]                        \n\
\\begin{circuitikz}                                                            \n\
\\ctikzset{tripoles/american or port/input height=.5}                          \n\
\\node[input,name=P1] {$S$};                                                   \n\
\\begin{scope}                                                                 \n\
\\ctikzset{tripoles/american or port/height=1}                                 \n\
\\draw (-.4,0) node {$"+latex(sIn)+" $} (P1) -- (0.5,0)                        \n\
  node[american or port, scale=.75, anchor=in 1] (B) {};                       \n\
\\end{scope}                                                                   \n\
\\node[output, right of=B, node distance=.5cm] (Q) {};                         \n\
\\draw (B.out) -- (Q);                                                         \n\
\\draw (2.4cm,-.3cm) node {$"+latex(sOut)+" $};                                \n\
\\node [input, below of =B, node distance=1cm] (fb) {};                        \n\
\\draw (B.out) |- (fb);                                                        \n\
\\draw  (fb) -| (B.in 2);                                                      \n\
\\node[input,below of = P1, name=P2, node distance=.53cm] {};                  \n\
\\draw (-.4cm,-.55cm) node {$"+latex(soutfb)+"$} (P2) -- (B.in 2);             \n\
\\end{circuitikz}                                                              \n\
\\caption{OR Gate Circuit for Simple Latch Equation ($"+vD[sIntop][0][2]+"$)}  \n\
\\label{fig:Figure 8}                                                          \n\
\\end{figure}")


At("Note that $"+latex(sbottom)+"\\subset"+latex(sbottom)+"$, \
   $"+latex(simpulse_up)+"\\subset"+latex(srise)+"$, \
   $"+latex(sbottom)+"\\subset"+latex(stop)+"$.\
   The events of "+Ml(sIn)+", "+Ml(soutfb)+", and "+Ml(sOut)+" were tabulated in \
   IX. The operating equations were tabulated in Table X. There were a sequence \
   of eigth pulses in the events. For each event, there were a set of five \
   equations. The first was the initial prior event condition of "+Ml(soutfb)+".  \
   the second equation was the prior event. The third equation was the \
   setting of the initial post condition of "+Ml(soutfb)+". This was the \
   feedback action. The fourth equation was the initial post event condition of \
   "+Ml(soutfb)+". The fifth equation is the whole event equation.")


#[0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
#[0, 0, 0, 1, 1, 1, 1, 1, 1, 1]


At("\
\\begin{table}[H] \\caption{Simple Latch Event}\
\\centering\
\\begin{tabular}{|p{.3cm}|p{.6cm}|p{6.424cm}|}\
\\hline Item&Signals &Stems \\\ \
\\end{tabular} \\\ \
\\begin{tabular}{|p{.3cm}|p{.6cm}|p{.25cm}|p{.25cm}|p{.25cm}|p{.25cm}|p{.25cm}\
                                 |p{.25cm}|p{.25cm}|p{.25cm}|p{.25cm}|p{.25cm}|}\
\\hline 00&"+Ml(sIn) +"&0&0&0&1&0&0&1&1&1&0 \\\ \
\\hline 01&Pulses& &"+Ml(sbottom)+"&"+Ml(sdelay_rise)+"&"+Ml(simpulse_up)+
                  "&"+Ml(sfall)+"&"+Ml(sdelay_rise)+"&"+Ml(srise)+"&"+Ml(stop)+
                  "&"+Ml(sdelay_fall)+"& \\\ \
\\hline 02&Priors& &"+Ml(ebottom)+"&"+Ml(ebottom)+"&"+Ml(erise)+
                  "&"+Ml(efall)+"&"+Ml(ebottom)+"&"+Ml(erise)+"&"+Ml(etop)+
                  "&"+Ml(etop)+"& \\\ \
\\hline 03&Now   & &"+Ml(pbottom)+"&"+Ml(pdelay_rise)+"&"+Ml(pimpulse_up)+
                  "&"+Ml(pfall)+"&"+Ml(pdelay_rise)+"&"+Ml(ptop)+"&"+Ml(ptop)+
                  "&"+Ml(pdelay_fall)+"& \\\ \
\\hline 04&Posts& &"+Ml(ebottom)+"&"+Ml(erise)+"&"+Ml(efall)+
                  "&"+Ml(ebottom)+"&"+Ml(erise)+"&"+Ml(erise)+"&"+Ml(etop)+
                  "&"+Ml(efall)+"& \\\ \
\\hline 05&"+Ml(soutfb)+"&0&0&0&0&1&1&1&1&1&1 \\\ \
\\hline 06&Pulses& &"+Ml(sbottom)+"&"+Ml(sbottom)+"&"+Ml(sdelay_rise)+
                  "&"+Ml(srise)+"&"+Ml(stop)+"&"+Ml(stop)+"&"+Ml(stop)+
                  "&"+Ml(stop)+"& \\\ \
\\hline 07&Priors& &"+Ml(ebottom)+"&"+Ml(ebottom)+"&"+Ml(ebottom)+
                  "&"+Ml(erise)+"&"+Ml(etop)+"&"+Ml(etop)+"&"+Ml(etop)+
                  "&"+Ml(etop)+"& \\\ \
\\hline 08&Now   & &"+Ml(pbottom)+"&"+Ml(pbottom)+"&"+Ml(pdelay_rise)+
                  "&"+Ml(prise)+"&"+Ml(ptop)+"&"+Ml(ptop)+"&"+Ml(ptop)+
                  "&"+Ml(ptop)+"& \\\ \
\\hline 09&Posts& &"+Ml(ebottom)+"&"+Ml(ebottom)+"&"+Ml(erise)+
                  "&"+Ml(etop)+"&"+Ml(etop)+"&"+Ml(etop)+"&"+Ml(etop)+
                  "&"+Ml(etop)+"& \\\ \
\\hline 10&"+Ml(sOut)+"&0&0&0&1&1&1&1&1&1&1 \\\ \
\\hline 11&Pulses& &"+Ml(sbottom)+"&"+Ml(sdelay_rise)+"&"+Ml(srise)+
                  "&"+Ml(stop)+"&"+Ml(stop)+"&"+Ml(stop)+"&"+Ml(stop)+
                  "&"+Ml(stop)+"& \\\ \
\\hline 12&Priors& &"+Ml(ebottom)+"&"+Ml(ebottom)+"&"+Ml(erise)+
                  "&"+Ml(etop)+"&"+Ml(etop)+"&"+Ml(etop)+"&"+Ml(etop)+
                  "&"+Ml(etop)+"& \\\ \
\\hline 13&Now   & &"+Ml(pbottom)+"&"+Ml(pdelay_rise)+"&"+Ml(prise)+
                  "&"+Ml(ptop)+"&"+Ml(ptop)+"&"+Ml(ptop)+"&"+Ml(ptop)+
                  "&"+Ml(ptop)+"& \\\ \
\\hline 14&Posts& &"+Ml(ebottom)+"&"+Ml(erise)+"&"+Ml(etop)+
                  "&"+Ml(etop)+"&"+Ml(etop)+"&"+Ml(etop)+"&"+Ml(etop)+
                  "&"+Ml(etop)+"& \\\ \
\\hline \\end{tabular} \\end{table} ")      




At("\
\\begin{table}[H] \\caption{Simple Latch Equation Event}\
\\centering\
\\begin{tabular}{|p{.05cm}|p{6.22cm}|p{1.4cm}|}\
\\hline n&Equations & Stems \\\ \
\\hline  1  &\\scriptsize "+Ml(fprior(foutfb(sbottom)))+" = "+Ml(fpost(foutfb(sbottom)))+
           "&\\scriptsize "+Ml(ebottom)+" = "+Ml(ebottom)+"\\\ \
            &\\scriptsize "+Ml(fprior(fIn(sbottom)))+" $\\cup$ "+Ml(fprior(foutfb(sbottom)))+
            " = "+Ml(fprior(fOut(sbottom)))+
           "&\\scriptsize "+Ml(ebottom)+" $\\cup$ "+Ml(ebottom)+" = "+Ml(ebottom)+" \\\ \
            &\\scriptsize  "+Ml(fpost(foutfb(sbottom)))+" = "+Ml(fprior(fOut(sbottom)))+
           "&\\scriptsize  "+Ml(ebottom)+" = "+Ml(ebottom)+" \\\ \
            &\\scriptsize  "+ Ml(fpost(fIn(sbottom)))+" $\\cup$ "+Ml(fpost(foutfb(sbottom))) +
              " = "+Ml(fpost(fOut(sbottom)))+
           "&\\scriptsize  "+Ml(ebottom)+" $\\cup$ "+Ml(ebottom)+" = "+Ml(ebottom)+" \\\ \
            &\\scriptsize  "+ Ml(fIn(sbottom))+" $\\cup$ "+Ml(foutfb(sbottom)) +
              " = "+Ml(fOut(sbottom))+
           "&\\scriptsize  "+Ml(pbottom)+" $\\cup$ "+Ml(pbottom)+" = "+Ml(pbottom)+" \\\ \
\\hline  2  &\\scriptsize "+Ml(fprior(foutfb(sbottom)))+" = "+Ml(fpost(foutfb(sbottom)))+
           "&\\scriptsize "+Ml(ebottom)+" = "+Ml(ebottom)+"\\\ \
            &\\scriptsize "+Ml(fprior(fIn(sdelay_rise)))+" $\\cup$ "+Ml(fprior(foutfb(sbottom)))+
            " = "+Ml(fprior(fOut(sdelay_rise)))+
           "&\\scriptsize "+Ml(ebottom)+" $\\cup$ "+Ml(ebottom)+" = "+Ml(ebottom)+" \\\ \
            &\\scriptsize  "+Ml(fpost(foutfb(sbottom)))+" = "+Ml(fprior(fOut(sbottom)))+
           "&\\scriptsize  "+Ml(ebottom)+" = "+Ml(ebottom)+" \\\ \
            &\\scriptsize  "+ Ml(fpost(fIn(sdelay_rise)))+" $\\cup$ "+Ml(fpost(foutfb(sbottom))) +
              " = "+Ml(fpost(fOut(sdelay_rise)))+
           "&\\scriptsize  "+Ml(erise)+" $\\cup$ "+Ml(ebottom)+" = "+Ml(erise)+" \\\ \
            &\\scriptsize  "+ Ml(fIn(sdelay_rise))+" $\\cup$ "+Ml(foutfb(sbottom)) +
              " = "+Ml(fOut(sdelay_rise))+
           "&\\scriptsize  "+Ml(pdelay_rise)+" $\\cup$ "+Ml(pbottom)+" = "+Ml(pdelay_rise)+" \\\ \
\\hline  3  &\\scriptsize "+Ml(fprior(foutfb(sbottom)))+" = "+Ml(fpost(foutfb(sbottom)))+
           "&\\scriptsize "+Ml(ebottom)+" = "+Ml(ebottom)+"\\\ \
            &\\scriptsize "+Ml(fprior(fIn(simpulse_up)))+" $\\cup$ "+Ml(fprior(foutfb(sbottom)))+
            " = "+Ml(fprior(fOut(simpulse_up)))+
           "&\\scriptsize "+Ml(erise)+" $\\cup$ "+Ml(ebottom)+" = "+Ml(erise)+" \\\ \
            &\\scriptsize  "+Ml(fpost(foutfb(sdelay_rise)))+" = "+Ml(fprior(fOut(simpulse_up)))+
           "&\\scriptsize  "+Ml(erise)+" = "+Ml(erise)+" \\\ \
            &\\scriptsize  "+ Ml(fpost(fIn(simpulse_up)))+" $\\cup$ "+Ml(fpost(foutfb(sdelay_rise))) +
              " = "+Ml(fpost(fOut(srise)))+
           "&\\scriptsize  "+Ml(efall)+" $\\cup$ "+Ml(erise)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fIn(simpulse_up))+" $\\cup$ "+Ml(foutfb(sdelay_rise)) +
              " = "+Ml(fOut(srise))+
           "&\\scriptsize  "+Ml(pimpulse_up)+" $\\cup$ "+Ml(pdelay_rise)+" = "+Ml(prise)+" \\\ \
\\hline  4  &\\scriptsize "+Ml(fprior(foutfb(srise)))+" = "+Ml(fpost(foutfb(sdelay_rise)))+
           "&\\scriptsize "+Ml(erise)+" = "+Ml(erise)+"\\\ \
            &\\scriptsize "+Ml(fprior(fIn(sfall)))+" $\\cup$ "+Ml(fprior(foutfb(srise)))+
            " = "+Ml(fprior(fOut(stop)))+
           "&\\scriptsize "+Ml(efall)+" $\\cup$ "+Ml(erise)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+Ml(fpost(foutfb(srise)))+" = "+Ml(fprior(fOut(stop)))+
           "&\\scriptsize  "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fpost(fIn(sfall)))+" $\\cup$ "+Ml(fpost(foutfb(srise))) +
              " = "+Ml(fpost(fOut(srise)))+
           "&\\scriptsize  "+Ml(ebottom)+" $\\cup$ "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fIn(sfall))+" $\\cup$ "+Ml(foutfb(srise)) +
              " = "+Ml(fOut(stop))+
           "&\\scriptsize  "+Ml(pfall)+" $\\cup$ "+Ml(prise)+" = "+Ml(ptop)+" \\\ \
\\hline  5  &\\scriptsize "+Ml(fprior(foutfb(stop)))+" = "+Ml(fpost(foutfb(srise)))+
           "&\\scriptsize "+Ml(etop)+" = "+Ml(etop)+"\\\ \
            &\\scriptsize "+Ml(fprior(fIn(sdelay_rise)))+" $\\cup$ "+Ml(fprior(foutfb(stop)))+
            " = "+Ml(fprior(fOut(stop)))+
           "&\\scriptsize "+Ml(ebottom)+" $\\cup$ "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+Ml(fpost(foutfb(stop)))+" = "+Ml(fprior(fOut(stop)))+
           "&\\scriptsize  "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fpost(fIn(sdelay_rise)))+" $\\cup$ "+Ml(fpost(foutfb(stop))) +
              " = "+Ml(fpost(fOut(stop)))+
           "&\\scriptsize  "+Ml(ebottom)+" $\\cup$ "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fIn(sdelay_rise))+" $\\cup$ "+Ml(foutfb(stop)) +
              " = "+Ml(fOut(stop))+
           "&\\scriptsize  "+Ml(pdelay_rise)+" $\\cup$ "+Ml(ptop)+" = "+Ml(ptop)+" \\\ \
\\hline  6  &\\scriptsize "+Ml(fprior(foutfb(stop)))+" = "+Ml(fpost(foutfb(srise)))+
           "&\\scriptsize "+Ml(etop)+" = "+Ml(etop)+"\\\ \
            &\\scriptsize "+Ml(fprior(fIn(srise)))+" $\\cup$ "+Ml(fprior(foutfb(stop)))+
            " = "+Ml(fprior(fOut(stop)))+
           "&\\scriptsize "+Ml(erise)+" $\\cup$ "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+Ml(fpost(foutfb(stop)))+" = "+Ml(fprior(fOut(stop)))+
           "&\\scriptsize  "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fpost(fIn(srise)))+" $\\cup$ "+Ml(fpost(foutfb(stop))) +
              " = "+Ml(fpost(fOut(stop)))+
           "&\\scriptsize  "+Ml(erise)+" $\\cup$ "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fIn(srise))+" $\\cup$ "+Ml(foutfb(stop)) +
              " = "+Ml(fOut(stop))+
           "&\\scriptsize  "+Ml(prise)+" $\\cup$ "+Ml(ptop)+" = "+Ml(ptop)+" \\\ \
\\hline  7  &\\scriptsize "+Ml(fprior(foutfb(stop)))+" = "+Ml(fpost(foutfb(srise)))+
           "&\\scriptsize "+Ml(etop)+" = "+Ml(etop)+"\\\ \
            &\\scriptsize "+Ml(fprior(fIn(stop)))+" $\\cup$ "+Ml(fprior(foutfb(stop)))+
            " = "+Ml(fprior(fOut(stop)))+
           "&\\scriptsize "+Ml(etop)+" $\\cup$ "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+Ml(fpost(foutfb(stop)))+" = "+Ml(fprior(fOut(stop)))+
           "&  "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fpost(fIn(stop)))+" $\\cup$ "+Ml(fpost(foutfb(stop))) +
              " = "+Ml(fpost(fOut(stop)))+
           "&\\scriptsize  "+Ml(etop)+" $\\cup$ "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fIn(srise))+" $\\cup$ "+Ml(foutfb(stop)) +
              " = "+Ml(fOut(stop))+
           "&\\scriptsize  "+Ml(ptop)+" $\\cup$ "+Ml(ptop)+" = "+Ml(ptop)+" \\\ \
\\hline  8  &\\scriptsize "+Ml(fprior(foutfb(stop)))+" = "+Ml(fpost(foutfb(srise)))+
           "& "+Ml(etop)+" = "+Ml(etop)+"\\\ \
            &\\scriptsize "+Ml(fprior(fIn(sdelay_fall)))+" $\\cup$ "+Ml(fprior(foutfb(stop)))+
            " = "+Ml(fprior(fOut(stop)))+
           "&\\scriptsize "+Ml(etop)+" $\\cup$ "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+Ml(fpost(foutfb(sdelay_fall)))+" = "+Ml(fprior(fOut(stop)))+
           "&\\scriptsize  "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fpost(fIn(stop)))+" $\\cup$ "+Ml(fpost(foutfb(stop))) +
              " = "+Ml(fpost(fOut(stop)))+
           "&\\scriptsize  "+Ml(etop)+" $\\cup$ "+Ml(etop)+" = "+Ml(etop)+" \\\ \
            &\\scriptsize  "+ Ml(fIn(srise))+" $\\cup$ "+Ml(foutfb(stop)) +
              " = "+Ml(fOut(stop))+
           "&\\scriptsize  "+Ml(pdelay_fall)+" $\\cup$ "+Ml(ptop)+" = "+Ml(ptop)+" \\\ \
\\hline \\end{tabular} \\end{table} ")      

At("Let's consider the event n=3 where the "+Ml(fIn(simpulse_up))+" event occured.")
Ce(Eq(fprior(foutfb(sbottom)),fpost(foutfb(sbottom))),
   Eq(ebottom,ebottom,evaluate=False))                                         #27
At("The current prior event of "+Ml(foutfb)+" was its previous post event. The \
    prior event equation was the feed forward of this feed back system.") 
Ce(fprior(fIn(simpulse_up))+fprior(foutfb(sbottom)),fprior(fOut(simpulse_up)),
   c=" = "+Ml(erise)+" $\\cup$ "+Ml(ebottom)+" = "+Ml(erise));Ad(key=sIn)      #28
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("+"," \\cup ")


At("The "+Ml(Eq(fprior(foutfb(sbottom)),ebottom))+" could not be changed by the "+
    Ml(Eq(fprior(fOut(simpulse_up)),erise))+" feedback since it already happened. \
    However, the "+ Ml(Eq(fprior(fOut(simpulse_up)),erise))+" could define \
    the "+Ml(fpost(soutfb))+" as feed back for next event. Thus, it was \
    set as follows.")
    
Ce(Eq(fpost(foutfb(sdelay_rise)),fprior(fOut(simpulse_up))),
   Eq(erise,erise,evaluate=False))
Ad(key=soutfb)                                                                 #29  


At("Hence, having determine the "+Ml(fpost(foutfb(sdelay_rise)))+" and given "+
   Ml(fpost(fIn(simpulse_up)))+" the "+Ml(fpost(sOut))+" was determined as follows.")

Ce(fpost(fIn(simpulse_up))+fpost(foutfb(sdelay_rise)),fpost(fOut(srise)),
   c=" = "+Ml(efall)+" $\\cup$ "+Ml(erise)+" = "+Ml(etop));Ad(key=sIn)         #30      
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("+"," \\cup ")

At("Taking the union of "+vD[sIn][0][1]+" and "+vD[sIn][1][1]+" we had the following.")

Ce(fIn(simpulse_up)+foutfb(sdelay_rise),fOut(srise),
   c=" = "+Ml(pimpulse_up)+" $\\cup$ "+Ml(pdelay_rise)+" = "+Ml(prise));
Ad(key=soutfb)                                                                 #31 
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("+"," \\cup ")


At("Although "+vD[soutfb][1][1]+" was consistent, the inequality "+
    Ml(Ne(foutfb(sdelay_rise),fOut(srise)))+ " appeared to contradict the \
    hardware connection in Figure 8 that asserted "+ Ml(Eq(soutfb,sOut))+". \
    However, the system was a feed back system whereby the output affect the \
    inputs. The assertion of equality was equation "+vD[soutfb][0][1]+".\
    Going to n=4, the "+Ml(fpost(foutfb(sdelay_rise)))+" became "+ 
    Ml(fprior(foutfb(srise)))+". In like manner, with the falling edge of  "+
    Ml(fIn(sfall))+" and the stored memory of  "+Ml(foutfb(srise))+", the \
    latch, "+Ml(fOut(stop))+" begun at this stage. The latch remained till \
    n=8, at different variation of "+Ml(sIn)+". The events n=2, 3,and 4 could be \
    said the transient response of the system. \\\ \ \\\
    The space state diagram of simple latch was shown in Figure 9.")

print("Processing Figure 9")

At("\
\\begin{figure}[H]                                                             \n\
\\centering                                                                    \n\
\\begin{tikzpicture}                                                           \n\
\\ctikzset{->, .=stealth',tripoles/american or port/input height=.5,           \n\
           node distance=3cm, initial text=$In("+latex(sbottom)+")$ }          \n\
\\node[state, initial, scale=.75] (q1) {$ Out("+latex(sbottom)+")$};           \n\
\\node[state, accepting, right of=q1, scale=.75] (q2) {$Out("+latex(stop)+")$};\n\
\\draw (q1) edge[loop above] node{"+Ml(sbottom)+"} (q1)                        \n\
(q1) edge[above] node{In("+Ml(stransition)+")} (q2)                            \n\
(q2) edge[loop above] node{"+Ml(stop)+"} (q2);                                 \n\
\\end{tikzpicture}                                                             \n\
\\caption{Space State Diagram for OR Gate Circuit for Simple Latch Equation    \n\
($"+vD[sIntop][0][2]+"$)}                                                      \n\
\\label{fig:Figure 9}                                                          \n\
\\end{figure}")

At("The simple latch could be expressed as follows.")

Ae(latex(sOut)+"=\\begin{cases} \
   "+latex(sbottom)+" & \\\ \\text{for}\\: "+latex(sIn)+" \\cup "+latex(sOut)+
   " = "+latex(sbottom)+" \\\ \ \\\ \
   "+latex(stop)+   " & \\\ \\: otherwise \\end{cases}")                       #32    


At("\\section{SR Flipflop}")


At("Let the signals S and R be generated such that they are disjoint. Let S \
    input set the latched signal QS and let R input reset the latched signal \
    QS. Let the QR be the inverse of QS. Given these condition, the circuit \
    was derived as follows.")


Sstream = [0, 6, 9, 13, 17, 18, 24, 28, 30, 60, 64, 67, 70, 71,  74, 78, 85, 88 ]

Rstream = [0, 36, 39, 42, 45, 46, 49, 52,54, 90, 92, 99, 100, 101, 102, 104, 107]

Sds=DiscreteSignal(Sstream)
exec("Spw="+Sds.GenTextPiecewise())
nSstems=Sds.GenPiecewiseStem(Spw, 110) 
nSt=linspace(0,len(nSstems)-1,len(nSstems))




Ce(sS,Spw);Ad()                                                                #33               
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("&","& \\\ ").\
    replace("13\\right)","13\\right) \\\ \\quad \ \ ").\
    replace("28\\right)","28\\right) \\\ \\quad \ \ ").\
    replace("67\\right)","67\\right) \\\ \\quad \ \ ").\
    replace("78\\right)","78\\right) \\\ \\quad \ \ ").\
    replace("17\\right)","17\\right) \\\ \\quad \ \ ").\
    replace("30\\right)","30\\right) \\\ \\quad \ \ ").\
    replace("70\\right)","70\\right) \\\ \\quad \ \ ").\
    replace("85\\right)","85\\right) \\\ \\quad \ \ ")  
  
tableS=SignalTable("Signal S Pulses",Sds)
At(tableS)


Rds=DiscreteSignal(Rstream)
exec("Rpw="+Rds.GenTextPiecewise())
nRstems=Rds.GenPiecewiseStem(Rpw, 110) 
nRt=linspace(0,len(nRstems)-1,len(nRstems))


Ce(sR,Rpw);Ad()                                                                #34 
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("&","& \\\ ").\
    replace("42\\right)","42\\right) \\\ \\quad \ \ ").\
    replace("52\\right)","52\\right) \\\ \\quad \ \ ").\
    replace("99\\right)","99\\right) \\\ \\quad \ \ ").\
    replace("45\\right)","45\\right) \\\ \\quad \ \ ").\
    replace("54\\right)","54\\right) \\\ \\quad \ \ ").\
    replace("100\\right)","100\\right) \\\ \\quad \ \ ")  

tableR=SignalTable("Signal R Pulses",Rds)
At(tableR)



At("The output signal QS and QR were constructed as follows.")

print("\nProcessing Figure 10")  



nQSstems,  nQRstems =Sds.SR_FF_Stems(nSstems,nRstems)

nQSstream=Sds.GenStream(nQSstems)
QSds=DiscreteSignal(nQSstream)
exec("QSpw="+QSds.GenTextPiecewise())
nQSt=linspace(0,len(nQSstems)-1,len(nQSstems))
nQSstems1=QSds.GenStem(nQSstream)
nQSstems2=QSds.GenPiecewiseStem(QSpw, 110)

Ce(sQS,QSpw)                                                                   #35  
tableQS=SignalTable("Signal QS Pulses",QSds)
At(tableQS)


nQRstream=Rds.GenStream(nQRstems)
QRds=DiscreteSignal(nQRstream)
exec("QRpw="+QRds.GenTextPiecewise())
nQRt=linspace(0,len(nQRstems)-1,len(nQRstems))
nQRstems1=QRds.GenStem(nQRstream)
nQRstems2=QRds.GenPiecewiseStem(QRpw, 110)
nQRtop=QRds.top
nQRtransition=set(QSds.transition)

Ce(sQR,QRpw)                                                                   #36  
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("&","& \\\ ").\
    replace("61\\right)","61\\right) \\\ \\quad \ \ ").\
    replace("100\\right)","100\\right) \\\ \\quad \ \ ")  


tableQR=SignalTable("Signal QR Pulses",QRds)
At(tableQR)




    
figure(num=10)
subplots_adjust(hspace=2.5)
subplot(4,1,1)
ax=gca();cla()
#axis([0,nSignal,-.1,1.5])
ax.set_title("Input S Signal")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(nSt,nSstems,"b")

subplot(4,1,2)
ax=gca();cla()
#axis([0,nSignal,-.1,1.5])
ax.set_title("Input R Signal")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(nRt,nRstems,"b")


subplot(4,1,3)
ax=gca();cla()
#axis([0,nSignal,-.1,1.5])
ax.set_title("Output QS Signal")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(nSt,nQSstems,"b")

subplot(4,1,4)
ax=gca();cla()
#axis([0,nSignal,-.1,1.5])
ax.set_title("Output QR Signal")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(nRt,nQRstems,"b")



At("The signals S, R, QS and QR were plotted in Figure 10.")

savefig("FG010.png")
Af("FG010.png",caption="SR Flipflop Timing Diagram",height=.35)


At("\\subsection{SR Model}")

At("By inspection of S and QS in Figure 10, the following was observed.")
Ae(latex(sStop)+" \\subset "+latex(sQStop));Ad(key=sStop)                      #37

At("Transforming "+vD[sStop][0][1]+" into an equation,")

Ce(sQStop,sQStop+sStop);Ad()                                                   #38 
ltD=len(tD)-1                                                   
tD[ltD]=tD[ltD].replace("+"," \\cup ")


At("Likewise inspecting R and QR, ")

Ae(latex(sRtop)+" \\subset "+latex(sQRtop));Ad(key=sRtop)                      #39 

At("Transforming "+vD[sRtop][0][1]+" into an equation,")

Ce(sQRtop,sQRtop+sRtop);Ad()                                                   #40  
ltD=len(tD)-1                                                
tD[ltD]=tD[ltD].replace("+"," \\cup ")


At("The relationship of QS and QR was established as follows.")

isQRtop, isQStop = symbols("\\overline{"+str(sQRtop)+"} \\overline{"+str(sQStop)+"}")


Ce(finv(sQStop),Eq(sQRtop,isQStop));Ad()                                       #41 

Ce(finv(sQRtop),Eq(sQStop,isQRtop));Ad()                                       #42 


At("Substituting "+vD[finv(sQRtop)][0][1]+" in the right hand side of "+
   vD[sQStop][0][1]+ " and  "+vD[finv(sQStop)][0][1]+" in the right hand side of "+
   vD[sQRtop][0][1]+",  ")



print("Processing Figure 11")

Ce(sQStop,isQRtop+sStop);Ad()                                                  #43
ltD=len(tD)-1                                                      
tD[ltD]=tD[ltD].replace("+"," \\cup ")
Ce(sQRtop,isQStop+sRtop);Ad()                                                  #44
ltD=len(tD)-1                                                      
tD[ltD]=tD[ltD].replace("+"," \\cup ")

At("\\subsection{SR Flipflop Circuit}")

At("The equations "+vD[sQStop][1][1]+" and "+vD[sQRtop][1][1]+" were realized \
    through the circuit diagram in Figure 11. The OR gate was the union \
    operation in set theory, the equivalent addition (+) operation in Boolean \
    algebra.")
 
At("\
\\begin{figure}[H]                                                             \n\
    \\centering                                                                \n\
	\\tikzstyle{block} = [draw, fill=white, rectangle,                         \n\
	minimum height=1.5cm, minimum width=3cm]                                   \n\
	\\tikzstyle{input} = [coordinate]                                          \n\
	\\tikzstyle{output} = [coordinate]                                         \n\
	\\tikzstyle{pinstyle} = [pin edge={to-,thin,black}]                        \n\
\\begin{circuitikz}                                                            \n\
\\ctikzset{tripoles/american or port/input height=.5}                          \n\
\\node[input,name=S] {$S$};                                                    \n\
\\node[input,below of =S, name=R, node distance=3.5cm] {$R$};                  \n\
\\node[american or port,right of = S,anchor=in 1,node distance=1cm] (ORs) {};  \n\
\\node[american or port,right of = R,anchor=in 2,node distance=1cm] (ORr) {};  \n\
\\node[american not port,below of=ORs,rotate=180,scale=.5,node distance=1cm](Is){};\n\
\\node[american not port,above of=ORr,rotate=180,scale=.5,node distance=1cm](Ir){};\n\
\\node[output, left of = Is, node distance=1cm] (fs){};                        \n\
\\node[output, left of = Ir, node distance=1cm] (fr){};                        \n\
\\node[output, right of=ORs, node distance=.5cm] (Qs) {$QS$}; \n\
\\node[output, right of=ORr, node distance=.5cm] (Qr) {$QR$}; \n\
\\draw (ORs.out) -- (Qs) node{$\\quad\\quad "+latex(sQStop)+"$} -|  (Is.in); \n\
\\draw (ORr.out) -- (Qr) node{$\\quad\\quad "+latex(sQRtop)+"$} -| (Ir.in); \n\
\\draw (Is.out) -- (fs)  -- (ORr.in 1) node {$"+latex(isQStop)+"\\quad\\quad\\quad$}; \n\
\\draw (Ir.out) -- (fr) -- (ORs.in 2) node {$"+latex(isQRtop)+"\\quad\\quad\\quad$}; \n\
\\draw  (S) node {$"+latex(sStop)+"\\quad\\quad$}-- (ORs.in 1); \n\
\\draw  (R) node {$"+latex(sRtop)+"\\quad\\quad$}-- (ORr.in 2); \n\
\\end{circuitikz} \n\
\\caption{OR Gate Circuit for SR Flipflop} \n\
\\label{fig:Figure 11}                                                 \n\
\\end{figure}")




print("Processing Figure 12")

At("Note that intersecting "+vD[sStop][0][1]+" with "+vD[sRtop][0][1]+", ")

Ae(latex(sStop)+" \\wedge "+latex(sRtop)+" \\subset "+latex(sQStop)+" \\wedge "+
   latex(sQRtop)+" = null = \\phi")                                            #45   


At("Therefore, the disjoint feature of S and R must be maintained to keep the \
    SR Flipflop operating in latching function. However, S and R may not be \
    kept disjoint for practical reasonss. \\\ \ \\\ ")

At("Hence, the set equation of SR flipflop was expressed as follows.")


SR=Matrix([sS, sR ])
QSRinv=Matrix([sQRinv, sQSinv])
QSR=Matrix([sQS, sQR]) 
QSRpulses=Matrix([[stop,simpulse_up,srise],[stop,simpulse_up,srise]])     
SRpulses=Matrix([stop,simpulse_up,srise]).transpose()
QSRundefined=Matrix([[simpulse_down,simpulse_up,simpulse_down, simpulse_up, dots],
                     [simpulse_down,simpulse_up,simpulse_down, simpulse_up, dots]])
SRundefined=Matrix([sfall,sbottom,sbottom,sbottom,dots]).transpose()

var("sQSR")

Ae(latex(QSR)+"=\\begin{cases} "+latex(SR)+" \\cup "+latex(QSRinv)+
   " & \\text{for}\\: "+latex(sS)+" \\cap "+latex(sR)+" = \\phi \\\ \ \\\ "+
   latex(QSR)+" & \\text{for}\\: "+latex(sS)+" \\cup "+latex(sR)+
   " = \\phi \\end{cases}");Ad(key=sQSR)                                        #46


At("\\subsection{Model of Cross Coupled OR Gate SR Flipflop}")

At("The cross coupled OR Gate SR Flipflop behaved differently when  \
    the non-disjoint signals S and R were inputted. Let's consider the following \
    non-disjoint signals.")

s1stream=[1,10,20,23,24,28,65,66,88,89,100,102,105,106,115,116,125,130,131,141,142,160]

s1ds=DiscreteSignal(s1stream)
exec("s1pw="+s1ds.GenTextPiecewise())
s1stems=s1ds.GenPiecewiseStem(s1pw, 160) 
s1t=linspace(0,len(s1stems)-1,len(s1stems))

Ce(sS,s1pw);Ad()                                              #47               
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("&","& \\\ ").\
    replace(" 23\\right)","23 \\right) \\\ \\quad \ \ ").\
    replace(" 66\\right)","66 \\right) \\\ \\quad \ \ ").\
    replace("102\\right)","102\\right) \\\ \\quad \ \ ").\
    replace("116\\right)","116\\right) \\\ \\quad \ \ ").\
    replace("141\\right)","141\\right) \\\ \\quad \ \ ")
  

tables1=SignalTable("Signal S Pulses",s1ds)
At(tables1)


r1stream=[1,10,35,36,50,53,54,58,75,78,80,83,88,89,115,116,125,130,131,150,151,160]

r1ds=DiscreteSignal(r1stream)
exec("r1pw="+r1ds.GenTextPiecewise())
r1stems=r1ds.GenPiecewiseStem(r1pw, 160) 
r1t=linspace(0,len(r1stems)-1,len(r1stems))


Ce(sR,r1pw);Ad()                                              #48               
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("&","& \\\ ").\
    replace(" 36\\right)","36 \\right) \\\ \\quad \ \ ").\
    replace(" 58\\right)","58 \\right) \\\ \\quad \ \ ").\
    replace(" 83\\right)","83\\right) \\\ \\quad \ \ ").\
    replace("116\\right)","116\\right) \\\ \\quad \ \ ").\
    replace("150\\right)","150\\right) \\\ \\quad \ \ ")
  
tabler1=SignalTable("Signal R Pulses",r1ds)
At(tabler1)


QS1stems,  QR1stems =s1ds.SR_FF_Stems(s1stems,r1stems)

QS1stream=Sds.GenStream(QS1stems)
QS1ds=DiscreteSignal(QS1stream)
exec("QS1pw="+QS1ds.GenTextPiecewise())
QS1t=linspace(0,len(QS1stems)-1,len(QS1stems))


Ce(sQS,QS1pw);Ad()                                            #49               
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("&","& \\\ ").\
    replace(" 12\\right)"," 12 \\right) \\\ \\quad \ \ ").\
    replace(" 16\\right)"," 16 \\right) \\\ \\quad \ \ ").\
    replace(" 36\\right)"," 36\\right) \\\ \\quad \ \ ").\
    replace(" 40\\right)"," 40\\right) \\\ \\quad \ \ ").\
    replace(" 44\\right)"," 44\\right) \\\ \\quad \ \ ").\
    replace(" 48\\right)"," 48\\right) \\\ \\quad \ \ ").\
    replace(" 66\\right)"," 66 \\right) \\\ \\quad \ \ ").\
    replace(" 70\\right)"," 70\\right) \\\ \\quad \ \ ").\
    replace(" 74\\right)"," 74\\right) \\\ \\quad \ \ ").\
    replace(" 89\\right)"," 89 \\right) \\\ \\quad \ \ ").\
    replace(" 93\\right)"," 93\\right) \\\ \\quad \ \ ").\
    replace(" 97\\right)"," 97\\right) \\\ \\quad \ \ ").\
    replace("116\\right)","116\\right) \\\ \\quad \ \ ").\
    replace("120\\right)","120 \\right) \\\ \\quad \ \ ").\
    replace("124\\right)","124\\right) \\\ \\quad \ \ ").\
    replace("141\\right)","141\\right) \\\ \\quad \ \ ")
  

tableQS1=SignalTable("Signal QS Pulses",QS1ds)
At(tableQS1)


QR1stream=Sds.GenStream(QR1stems)
QR1ds=DiscreteSignal(QR1stream)
exec("QR1pw="+QR1ds.GenTextPiecewise())
QR1t=linspace(0,len(QR1stems)-1,len(QR1stems))



Ce(sQR,QR1pw);Ad()                                            #50              
ltD=len(tD)
tD[ltD-1]=tD[ltD-1].replace("&","& \\\ ").\
    replace(" 12\\right)"," 12 \\right) \\\ \\quad \ \ ").\
    replace(" 16\\right)"," 16 \\right) \\\ \\quad \ \ ").\
    replace(" 20\\right)"," 20\\right) \\\ \\quad \ \ ").\
    replace(" 38\\right)"," 38\\right) \\\ \\quad \ \ ").\
    replace(" 42\\right)"," 42\\right) \\\ \\quad \ \ ").\
    replace(" 46\\right)"," 46\\right) \\\ \\quad \ \ ").\
    replace(" 66\\right)"," 66 \\right) \\\ \\quad \ \ ").\
    replace(" 70\\right)"," 70\\right) \\\ \\quad \ \ ").\
    replace(" 74\\right)"," 74\\right) \\\ \\quad \ \ ").\
    replace(" 91\\right)"," 91 \\right) \\\ \\quad \ \ ").\
    replace(" 95\\right)"," 95\\right) \\\ \\quad \ \ ").\
    replace(" 99\\right)"," 99\\right) \\\ \\quad \ \ ").\
    replace("116\\right)","116\\right) \\\ \\quad \ \ ").\
    replace("120\\right)","120 \\right) \\\ \\quad \ \ ").\
    replace("124\\right)","124\\right) \\\ \\quad \ \ ").\
    replace("150\\right)","150\\right) \\\ \\quad \ \ ")
  


tableQR1=SignalTable("Signal QR Pulses",QR1ds)
At(tableQR1)



At("Applying the signals from "+vD[sS][1][1]+" and "+vD[sR][1][1]+" to OR Gated \
   SR flipflop, the timing diagram behavior was generated as shown in Figure 12. \
   The space state diagram for Figure 12 timing diagram was depicted in Figure 13.")






figure(num=12)
subplots_adjust(hspace=2.5)
subplot(4,1,1)
ax=gca();cla()
#axis([0,nSignal,-.1,1.5])
ax.set_title("Input S Signal")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(s1t,s1stems,"b")

subplot(4,1,2)
ax=gca();cla()
#axis([0,nSignal,-.1,1.5])
ax.set_title("Input R Signal")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(s1t,r1stems,"b")


subplot(4,1,3)
ax=gca();cla()
#axis([0,nSignal,-.1,1.5])
ax.set_title("Output QS Signal")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(QS1t,QS1stems,"b")

subplot(4,1,4)
ax=gca();cla()
#axis([0,nSignal,-.1,1.5])
ax.set_title("Output QR Signal")
ax.set_ylabel("Logic State")
ax.set_xlabel("units of time")
plot(QR1t,QR1stems,"b")


savefig("FG012.png")
Af("FG012.png",caption="Non-disjoint S and R Signals SR Flipflop Timing Diagram",
    height=.35)


At("\
\\begin{figure}[H]                                                                \n\
\\centering                                                                       \n\
\\begin{tikzpicture}                                                              \n\
\\ctikzset{->,.=stealth',tripoles/american or port/input height=.5,               \n\
           node distance=2cm, initial text=$$ }                                   \n\
\\node[state,                scale=.75,  node distance=5cm](q1){$Q1(0,1)$};       \n\
\\node[state, right of = q1, scale=.75,  node distance=5cm](q2){$Q2(1,0)$};       \n\
\\node[state, below of = q1, scale=.75,  node distance=5cm](q3){$Q3(1,1)$};       \n\
\\node[state, right of = q3, scale=.75,  node distance=5cm](q0){$Q0(0,0)$};       \n\
\\draw (q0) edge[bend left,  below] node{"+Ml(sSbottom)+", "+Ml(sRbottom)+"} (q3);\n\
\\draw (q1) edge[loop        above] node{"+Ml(sSbottom)+", "+Ml(sRbottom)+"}      \n\
(q1) edge[bend left,         above] node{"+Ml(sSrise)+", "  +Ml(sRbottom)+"} (q2) \n\
(q1) edge[bend right,        above] node{"+Ml(sSup)+", "    +Ml(sRbottom)+"} (q3) \n\
(q1) edge[bend right,        below] node{"+Ml(sSrise)+", "  +Ml(sRrise)  +"} (q3);\n\
\\draw (q2) edge[loop        above] node{"+Ml(sSbottom)+", "+Ml(sRbottom)+"}      \n\
(q2) edge[bend left,         above] node{"+Ml(sSbottom)+", "+Ml(sRrise)  +"} (q1) \n\
(q2) edge[bend left,         below] node{"+Ml(sSrise)+", "  +Ml(sRrise)  +"} (q3) \n\
(q2) edge[bend left,         above] node{"+Ml(sSbottom)+", "   +Ml(sRup) +"} (q3);\n\
\\draw (q3) edge[loop        below] node{"+Ml(sStop)+", "+Ml(sRtop)+"}            \n\
(q3) edge[bend left,         below] node{"+Ml(sSfall)+", "  +Ml(sRfall)  +"} (q0) \n\
(q3) edge[bend right,        above] node{$oscillation$}                      (q0) \n\
(q3) edge[bend right,        below] node{"+Ml(sSfall)+","+Ml(sRtop)      +"} (q1) \n\
(q3) edge[bend left,         below] node{"+Ml(sStop)+", "+Ml(sRfall)     +"} (q2);\n\
\\end{tikzpicture}                                                                \n\
\\caption{Space State Diagram SR Flipflop Operation in Figure 12 }                \n\
\\label{fig:Figure 13}                                                            \n\
\\end{figure}")

At("\\subsection{Symbolic Pulses Features}")

At("The symbolic pulses were related as follows.  ")

Ae(latex(stop)+"\\supset {"+latex(srise)+"\\cup"+latex(sdelay_rise)+"\\cup"+
   latex(sfall)+"\\cup"+latex(sdelay_fall)+"\\cup"+latex(simpulse_up)+"\\cup"+
   latex(simpulse_down)+"\\cup"+latex(stransition)+"\\cup"+latex(sbottom)+"}") #51
Ad(key=stop)

At("Given a set of 5-stem sequence, it could be represented by a sequence of \
   the symbolic pulses as shown in Table 1.")


At("\
\\begin{table}[H] \\caption{Combination of a Three of Pulses in Four Time Points}\
\\centering\
\\begin{tabular}{|p{.5cm}|p{1.5cm}|p{3.85cm}|}\
\\hline Items&Stems     &Pulses at Time Points \\\ \
\\end{tabular} \\\ \n\
\\begin{tabular}{|p{.5cm}|p{1.5cm}|p{1cm} p{1cm} p{1cm}|}\
&0,1,2,3,4 &1 &2 &3 \\\ \
\\hline 00&0,0,0,0,0 &"+Ml(sbottom)      +",&"+Ml(sbottom)      +",&"+Ml(sbottom)      +" \\\ \
\\hline 01&1,0,0,0,0 &"+Ml(sfall)        +",&"+Ml(sbottom)      +",&"+Ml(sbottom)      +" \\\ \
\\hline 02&0,1,0,0,0 &"+Ml(simpulse_up)  +",&"+Ml(sfall)        +",&"+Ml(sbottom)      +" \\\ \
\\hline 03&1,1,0,0,0 &"+Ml(sdelay_fall)  +",&"+Ml(sfall)        +",&"+Ml(sbottom)      +" \\\ \
\\hline 04&0,0,1,0,0 &"+Ml(sdelay_rise)  +",&"+Ml(simpulse_up)  +",&"+Ml(sfall)        +" \\\ \
\\hline 05&1,0,1,0,0 &"+Ml(simpulse_down)+",&"+Ml(simpulse_up)  +",&"+Ml(sfall)        +" \\\ \
\\hline 06&0,1,1,0,0 &"+Ml(srise)        +",&"+Ml(sdelay_fall)  +",&"+Ml(sfall)        +" \\\ \
\\hline 07&1,1,1,0,0 &"+Ml(stop)         +",&"+Ml(sdelay_fall)  +",&"+Ml(sfall)        +" \\\ \
\\hline 08&0,0,0,1,0 &"+Ml(sbottom)      +",&"+Ml(sdelay_rise)  +",&"+Ml(simpulse_up)  +" \\\ \
\\hline 09&1,0,0,1,0 &"+Ml(sfall)        +",&"+Ml(sdelay_rise)  +",&"+Ml(simpulse_up)  +" \\\ \
\\hline 10&0,1,0,1,0 &"+Ml(simpulse_up)  +",&"+Ml(simpulse_down)+",&"+Ml(simpulse_up)  +" \\\ \
\\hline 11&1,1,0,1,0 &"+Ml(sdelay_fall)  +",&"+Ml(simpulse_down)+",&"+Ml(simpulse_up)  +" \\\ \
\\hline 12&0,0,1,1,0 &"+Ml(sdelay_rise)  +",&"+Ml(srise)        +",&"+Ml(sdelay_fall)  +" \\\ \
\\hline 13&1,0,1,1,0 &"+Ml(simpulse_down)+",&"+Ml(srise)        +",&"+Ml(sdelay_fall)  +" \\\ \
\\hline 14&0,1,1,1,0 &"+Ml(srise)        +",&"+Ml(stop)         +",&"+Ml(sdelay_fall)  +" \\\ \
\\hline 15&1,1,1,1,0 &"+Ml(stop)         +",&"+Ml(stop)         +",&"+Ml(sdelay_fall)  +" \\\ \
\\hline 16&0,0,0,0,1 &"+Ml(sbottom)      +",&"+Ml(sbottom)      +",&"+Ml(sdelay_rise)  +" \\\ \
\\hline 17&1,0,0,0,1 &"+Ml(sfall)        +",&"+Ml(sbottom)      +",&"+Ml(sdelay_rise)  +" \\\ \
\\hline 18&0,1,0,0,1 &"+Ml(simpulse_up)  +",&"+Ml(sfall)        +",&"+Ml(sdelay_rise)  +" \\\ \
\\hline 19&1,1,0,0,1 &"+Ml(sdelay_fall)  +",&"+Ml(sfall)        +",&"+Ml(sdelay_rise)  +" \\\ \
\\hline 20&0,0,1,0,1 &"+Ml(sdelay_rise)  +",&"+Ml(simpulse_up)  +",&"+Ml(simpulse_down)+" \\\ \
\\hline 21&1,0,1,0,1 &"+Ml(simpulse_down)+",&"+Ml(simpulse_up)  +",&"+Ml(simpulse_down)+" \\\ \
\\hline 22&0,1,1,0,1 &"+Ml(srise)        +",&"+Ml(sdelay_fall)  +",&"+Ml(simpulse_down)+" \\\ \
\\hline 23&1,1,1,0,1 &"+Ml(stop)         +",&"+Ml(sdelay_fall)  +",&"+Ml(simpulse_down)+" \\\ \
\\hline 24&0,0,0,1,1 &"+Ml(sbottom)      +",&"+Ml(sdelay_rise)  +",&"+Ml(srise)        +" \\\ \
\\hline 25&1,0,0,1,1 &"+Ml(sfall)        +",&"+Ml(sdelay_rise)  +",&"+Ml(srise)        +" \\\ \
\\hline 26&0,1,0,1,1 &"+Ml(simpulse_up)  +",&"+Ml(simpulse_down)+",&"+Ml(srise)        +" \\\ \
\\hline 27&1,1,0,1,1 &"+Ml(sdelay_fall)  +",&"+Ml(simpulse_down)+",&"+Ml(srise)        +" \\\ \
\\hline 28&0,0,1,1,1 &"+Ml(sdelay_rise)  +",&"+Ml(srise)        +",&"+Ml(stop)         +" \\\ \
\\hline 28&1,0,1,1,1 &"+Ml(simpulse_down)+",&"+Ml(srise)        +",&"+Ml(stop)         +" \\\ \
\\hline 30&0,1,1,1,1 &"+Ml(srise)        +",&"+Ml(stop)         +",&"+Ml(stop)         +" \\\ \
\\hline 31&1,1,1,1,1 &"+Ml(stop)         +",&"+Ml(stop)         +",&"+Ml(stop)         +" \\\ \
\\hline \\end{tabular} \\end{table} ")



At("\
\\begin{table}[H] \\caption{SR Flipflop in Oscillation Operation}\
\\centering\
\\begin{tabular}{|p{.3cm}|p{1.5cm}|p{5.5cm}|}\
\\hline Item&Signals &Stems \\\ \
\\end{tabular} \\\ \
\\begin{tabular}{|p{.3cm}|p{1.5cm}|p{.1cm}|p{.1cm}|p{.3cm}|p{.47cm}|p{.1cm}\
                                  |p{.1cm}|p{.1cm}|p{.1cm}|p{.1cm}|p{.1cm}|}\
\\hline 00&"+Ml(sS)+" &1&1&1&0&0&0&0&0&0&0 \\\ \
   & & &"+Ml(stop)   +"&"+Ml(sdelay_fall)+"&"+Ml(sfall)  +"&"+Ml(sbottom)+
      "&"+Ml(sbottom)+"&"+Ml(sbottom)    +"&"+Ml(sbottom)+"&"+Ml(sbottom)+
      "& \\\ \
\\hline 01&"+Ml(sQRinv)+" &0&0&0&0&1&0&1&0&1&0 \\\ \
   & & &"+Ml(sbottom)   +"&"+Ml(sbottom)+"&"+Ml(sdelay_rise)  +"&"+Ml(simpulse_up)+
      "&"+Ml(simpulse_down)+"&"+Ml(simpulse_up)    +"&"+Ml(simpulse_down)+
      "&"+Ml(simpulse_up)+"& \\\ \
\\hline 02&"+Ml(sS)+"$\\vee$"+Ml(sQRinv)+"="+Ml(sQS)+"&1&1&1&0&1&0&1&0&1&0 \\\ \
   & & &"+Ml(stop)   +"&"+Ml(sdelay_fall)+"&"+Ml(simpulse_down)  +"&"+Ml(simpulse_up)+
      "&"+Ml(simpulse_down)+"&"+Ml(simpulse_up) +"&"+Ml(simpulse_down)+
      "&"+Ml(simpulse_up)+"& \\\ \
\\hline 03&"+Ml(sR)+" &1&1&1&0&0&0&0&0&0&0 \\\ \
   & & &"+Ml(stop)   +"&"+Ml(sdelay_fall)+"&"+Ml(sfall)  +"&"+Ml(sbottom)+
      "&"+Ml(sbottom)+"&"+Ml(sbottom)    +"&"+Ml(sbottom)+"&"+Ml(sbottom)+
      "& \\\ \
\\hline 04&"+Ml(sQSinv)+" &0&0&0&0&1&0&1&0&1&0 \\\ \
   & & &"+Ml(sbottom)   +"&"+Ml(sbottom)+"&"+Ml(sdelay_rise)  +"&"+Ml(simpulse_up)+
      "&"+Ml(simpulse_down)+"&"+Ml(simpulse_up)    +"&"+Ml(simpulse_down)+
      "&"+Ml(simpulse_up)+"& \\\ \
\\hline 05&"+Ml(sR)+"$\\vee$"+Ml(sQSinv)+"="+Ml(sQR)+"&1&1&1&0&1&0&1&0&1&0 \\\ \
   & & &"+Ml(stop)   +"&"+Ml(sdelay_fall)+"&"+Ml(simpulse_down)  +"&"+Ml(simpulse_up)+
      "&"+Ml(simpulse_down)+"&"+Ml(simpulse_up) +"&"+Ml(simpulse_down)+
      "&"+Ml(simpulse_up)+"& \\\ \
\\hline \\end{tabular} \\end{table} ")      


    
At("At stead state of Q3(1,1), ")

Ce(fQS(stop),fQRinv(sbottom)+fS(stop));Ad(key=sQS)                             #52
ltD=len(tD)-1;tD[ltD]=tD[ltD].replace("+","\\cup")

Ce(fQR(stop),fQSinv(sbottom)+fR(stop));Ad(key=sQR)                             #53
ltD=len(tD)-1;tD[ltD]=tD[ltD].replace("+","\\cup")



At("\\subsection{Application of Event Property in SR Flip Flop Modeling}")

At("As illustrated previously, the pulse consisted of time units tuple \
   (t-1, t, t+1), e.g., (0,1,2). The tuple could be segmented in term of \
    events. Hence prior event was (t-1, t) and the post event (t, t+1). \
    The pulses could be categorized further by in terms of the changes in \
    prior and post events.")


At("\
\\begin{table}[H] \\caption{Symbolic Pulses Classification by Events}     \
\\centering                                                               \
\\begin{tabular}{|p{.4cm}|p{.5cm}|p{1.17cm}|p{2cm}|p{2cm}|}               \
\\hline Item&Pulse &Stems&prior Event&post Event                      \\\ \
\\end{tabular}                                                        \\\ \
\\begin{tabular}{|p{.4cm}|p{.5cm}|p{.1cm}|p{.1cm}|p{.1cm}|p{2cm}|p{2cm}|} \
\\hline 00&"+Ml(sbottom)      +" &0&0&0&No change down&No change down \\\ \
\\hline 01&"+Ml(stop)         +" &1&1&1&No change up  &No change up   \\\ \
\\hline 02&"+Ml(sfall)        +" &1&0&0&   Change down&No change down \\\ \
\\hline 03&"+Ml(srise)        +" &0&1&1&   Change up  &No change up   \\\ \
\\hline 04&"+Ml(sdelay_rise)  +" &0&0&1&No change down&   Change up   \\\ \
\\hline 05&"+Ml(sdelay_fall)  +" &1&1&0&No change up  &   Change down \\\ \
\\hline 06&"+Ml(simpulse_up)  +" &0&1&0&   Change up  &   Change down \\\ \
\\hline 07&"+Ml(simpulse_down)+" &1&0&1&   Change down&   Change up   \\\ \
\\hline \\end{tabular} \\end{table} ")      



At("Note that no change in prior events were "+Ml(sbottom)+", "+Ml(stop)+", "+
    Ml(sdelay_rise)+", and "+Ml(sdelay_fall)+". The change in prior events were "+
    Ml(srise)+", "+Ml(sfall)+", "+ Ml(simpulse_down)+", and "+Ml(simpulse_up)+
    ". The no change in post events were "+Ml(sbottom)+", "+Ml(stop)+", "+
    Ml(srise)+", and "+Ml(sfall)+". The change in post events were "+Ml(sdelay_rise)+
    ", "+Ml(sdelay_fall)+", "+ Ml(simpulse_up)+", and "+Ml(simpulse_down)+". \\\ \ \\\ \
     ")

At("\
\\begin{table}[H] \\caption{Event Equivalent}     \
\\centering                                                               \
\\begin{tabular}{|p{.1cm}|p{3cm}|p{3cm}|p{.4cm}|}               \
\\hline n&Prior Event Function&Post Event Function&Stem      \\\ \
\\hline 0&"+Ml(Eq(fprior(Eq(sbottom,pbottom)),
                   fprior(Eq(sdelay_rise,pdelay_rise))))      +" \
         &"+Ml(Eq(fpost (Eq(sbottom,pbottom)),
                   fpost (Eq(sfall,pfall)))) +"& "+Ml(ebottom)+"\\\ \
\\hline 1&"+Ml(Eq(fprior(Eq(stop,ptop)),
                  fprior(Eq(sdelay_fall,pdelay_fall))))       +" \
         &"+Ml(Eq(fpost (Eq(stop,ptop)),
                   fpost (Eq(srise,prise)))) +"& "+Ml(etop)   +"\\\ \
\\hline 2&"+Ml(Eq(fprior(Eq(srise,prise)),
                   fprior(Eq(simpulse_up,pimpulse_up))))      +" \
         &"+Ml(Eq(fpost (Eq(sdelay_rise,pdelay_rise)),
                   fpost (Eq(simpulse_down,pimpulse_down))))+"& "+Ml(erise)+"  \\\ \
\\hline 3&"+Ml(Eq(fprior(Eq(sfall,pfall)),
                   fprior(Eq(simpulse_down,pimpulse_down))))   +" \
         &"+Ml(Eq(fpost (Eq(sdelay_fall,pdelay_fall)),
                      fpost (Eq(simpulse_up,pimpulse_up))))+"& "+Ml(efall)+"  \\\ \
\\hline \\end{tabular} \\end{table} ")      


At("Let's consider the events of pulses of SR Flipflop where "+
   Ml(sSfall)+ " and "+Ml(sRfall)+" occurred simultaneously. ")

  
Ce(fS(sfall,sbottom,sbottom,sbottom,dots)+
   fQRinv(sdelay_rise,simpulse_up,simpulse_down,simpulse_up,dots),
   fQS(simpulse_down,simpulse_up,simpulse_down,simpulse_up,dots))
Ad(key=sS)                                                                     #54   
ltD=len(tD)-1;tD[ltD]=tD[ltD].replace("+","\\cup")

Ce(fR(sfall,sbottom,sbottom,sbottom,dots)+
   fQSinv(sdelay_rise,simpulse_up,simpulse_down,simpulse_up,dots),
   fQR(simpulse_down,simpulse_up,simpulse_down,simpulse_up,dots))
Ad(key=sR)                                                                     #55   
ltD=len(tD)-1;tD[ltD]=tD[ltD].replace("+","\\cup")
                              
At("Lets consider the prior event of "+Ml(sSfall)+ " and "+Ml(sRfall)+". ")

Ce(fprior(fS(sfall))+fprior(fQRinv(sbottom)),fprior(fQS(sfall)),
   c=" = "+Ml(efall)+"$\\cup$"+Ml(ebottom)+"="+Ml(efall))
Ad(key=sS)                                                                     #56 
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 
Ce(fprior(fR(sfall))+fprior(fQSinv(sbottom)),fprior(fQR(sfall)),
   c=" = "+Ml(efall)+"$\\cup$"+Ml(ebottom)+"="+Ml(efall))
Ad(key=sR)                                                                     #57  
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 

At("The changes in prior events occurred at S, R, QS, and  QR. No changes \
    took place at $\\overline{QR}$ and $\\overline{QS}$.  However, the output \
    QS and QR were inverted and fedback as $\\overline{QR}$ and $\\overline{QS}$.\
    Such inversion had prior event changes. However, the prior events of  \
    $\\overline{QR}$ and $\\overline{QS}$ happened already and could not be \
    change instantaneously. Therefore the prior events of feedbacks \
    should apply only to the post events of $\\overline{QR}$ and \
    $\\overline{QS}$. Thus,")


Ce(fpost(fQRinv(srise)),fprior(finv(fQR(sfall))),
   c="="+Ml(erise)+"$= \\overline{"+str(efall)+"}$");Ad(key=sQRinv)                #58       
Ce(fpost(fQSinv(srise)),fprior(finv(fQS(sfall))),
   c="="+Ml(erise)+"$= \\overline{"+str(efall)+"}$");Ad(key=sQSinv)                #59

At("Using "+vD[sQRinv][0][1]+" and "+vD[sQSinv][0][1]+", the post event equations \
    were formulated and solved. Therefore, the post events of SR flipflop \
    were expressed as follows.")


Ce(fpost(fS(sfall))+fpost(fQRinv(sdelay_rise)),fpost(fQS(sdelay_rise)),
   c="="+Ml(ebottom)+"$\\cup$"+Ml(erise)+"="+Ml(erise))
Ad(key=sS)                                                                     #60
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 
Ce(fpost(fR(sfall))+fpost(fQSinv(sdelay_rise)),fpost(fQR(sdelay_rise)),
   c="="+Ml(ebottom)+"$\\cup$"+Ml(erise)+"="+Ml(erise))
Ad(key=sR)                                                                     #61
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 

    
At("Taking the union of "+vD[sS][3][1]+" and "+vD[sS][4][1]+" and "+
   vD[sR][3][1]+" and "+vD[sR][4][1]+", ")

Ce(fS(sfall)+fQRinv(sdelay_rise),fQS(simpulse_down),
   c="="+Ml(pfall)+"$\\cup$"+Ml(pdelay_rise)+"="+Ml(pimpulse_down));Ad(key=sS) #62
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 
Ce(fR(sfall)+fQSinv(sdelay_rise),fQR(simpulse_down),
   c="="+Ml(pfall)+"$\\cup$"+Ml(pdelay_rise)+"="+Ml(pimpulse_down));Ad(key=sR) #63
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 

At("Hence the equation "+vD[sS][5][1]+" and "+vD[sR][5][1]+" satisfied  "+
    vD[sS][2][1]+" and "+vD[sR][2][1]+". \\\ \ \\\ \
    Moving on let the post event of "+vD[sS][5][1]+" and "+vD[sR][5][1]+
    " be the new prior event. The equivalent rise pulses were chosen. ")


Ce(fprior(fS(sbottom))+fprior(fQRinv(srise)),fprior(fQS(srise)),
   c="="+Ml(ebottom)+"$\\cup$"+Ml(erise)+"="+Ml(erise))
Ad(key=sS)                                                                     #64
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 
Ce(fprior(fR(sbottom))+fprior(fQSinv(srise)),fprior(fQR(srise)),
   c="="+Ml(ebottom)+"$\\cup$"+Ml(erise)+"="+Ml(erise))
Ad(key=sR)                                                                     #65
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 

At("Thereafter, the feedback inversion were established as follows.")

Ce(fpost(fQRinv(sdelay_fall)),fprior(finv(fQR(srise))),
   c="="+Ml(efall)+"$=\\overline{"+str(erise)+"}$");Ad(key=sQRinv)               #66       
Ce(fpost(fQSinv(sdelay_fall)),fprior(finv(fQS(srise))),
   c="="+Ml(efall)+"$=\\overline{"+str(erise)+"}$");Ad(key=sQSinv)               #67

At("Using "+vD[sQRinv][1][1]+" and "+vD[sQSinv][1][1]+", the post event equations \
    were formulated as follows.")


Ce(fpost(fS(sbottom))+fpost(fQRinv(sdelay_fall)),fpost(fQS(sdelay_fall)),
   c="="+Ml(ebottom)+"$\\cup$"+Ml(efall)+"="+Ml(efall))
Ad(key=sS)                                                                     #68
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 
Ce(fpost(fR(sbottom))+fpost(fQSinv(sdelay_fall)),fpost(fQR(sdelay_fall)),
   c="="+Ml(ebottom)+"$\\cup$"+Ml(efall)+"="+Ml(efall))
Ad(key=sR)                                                                     #69
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 

    
At("Taking the union of "+vD[sS][6][1]+" and "+vD[sS][7][1]+" and "+
   vD[sR][6][1]+" and "+vD[sR][7][1]+", ")


Ce(fS(sbottom)+fQRinv(simpulse_up),fQS(simpulse_up),
   c="="+Ml(pbottom)+"$\\cup$"+Ml(pimpulse_up)+"="+Ml(pimpulse_up));Ad(key=sS)                #70
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 
Ce(fR(sbottom)+fQSinv(simpulse_up),fQR(simpulse_up),
   c="="+Ml(pbottom)+"$\\cup$"+Ml(pimpulse_up)+"="+Ml(pimpulse_up));Ad(key=sR)                #71
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 

At("Hence the equation "+vD[sS][8][1]+" and "+vD[sR][8][1]+" satisfied  "+
    vD[sS][2][1]+" and "+vD[sR][2][1]+ "The above computations were illustrated \
    in Table XXI. the prior event equations was initially given and solve for \
    the output prior event. The output prior event was inverted and fed back as post event feedback input. \
    Thereafter the post event equation was completed and solved for the \
    output post event. The union of prior and post equations establisthed the \
    now event equation. For the next event, the previous post event was made \
    the new prior event. Thereafter the process was repeated for the next now \
    event. The event computational method for SR flip flop was tabulated in \
    Table XXIII")



At("\
\\begin{table}[H] \\caption{The Event Computational Method for SR Flip Flop}     \
\\centering                                                               \
\\begin{tabular}{|p{.4cm}|p{5.75cm}|p{1.4cm}|}               \
\\hline Item&Event Equation  &Stem     \\\ \
\\hline 00&\\scriptsize$ "+
 str(fprior(fQRinv(sbottom)))+" = "+str(fpost(fQRinv(sbottom)))+"\\newline "+
 str(fprior(fQSinv(sbottom)))+" = "+str(fpost(fQSinv(sbottom)))+
 "$&\\scriptsize$"+
 str(ebottom)+"="+str(ebottom)+"\\newline  "+
 str(ebottom)+"="+str(ebottom)+"$   \\\ \
\\hline 01&\\scriptsize$ "+
 str(fprior(fS(sfall)))+" \\cup "+str(fprior(fQRinv(sbottom)))+
 " = "+str(fprior(fQS(sfall)))+"\\newline "+
 str(fprior(fR(sfall)))+" \\cup "+str(fprior(fQSinv(sbottom)))+
 " = "+str(fprior(fQR(sfall)))+
 "$&\\scriptsize$"+
 str(efall)+"\\cup"+str(ebottom)+"="+str(efall)+"\\newline "+
 str(efall)+"\\cup"+str(ebottom)+"="+str(efall)+"$  \\\ \
\\hline 02&\\scriptsize$ "+
 str(fpost(fQRinv(sdelay_rise)))+" = "+str(fprior(finv(fQR(sfall))))+"\\newline "+
 str(fpost(fQSinv(sdelay_rise)))+" = "+str(fprior(finv(fQS(sfall))))+
 "$&\\scriptsize$"+
 str(erise)+"=\\overline{"+str(efall)+"}\\newline "+
 str(erise)+"=\\overline{"+str(efall)+"}$  \\\ \
\\hline 03&\\scriptsize$ "+
 str(fpost(fS(sbottom)))+" \\cup "+str(fpost(fQRinv(sdelay_rise)))+
 " = "+str(fpost(fQS(srise)))+"\\newline "+
 str(fpost(fR(sbottom)))+" \\cup "+str(fpost(fQSinv(sdelay_rise)))+
 " = "+str(fpost(fQR(srise)))+
 "$&\\scriptsize$"+
 str(ebottom)+"\\cup"+str(erise)+"="+str(erise)+"\\newline "+
 str(ebottom)+"\\cup"+str(erise)+"="+str(erise)+"$  \\\ \
\\hline 04&\\scriptsize$ "+
 str(fS(sfall))+" \\cup "+str(fQRinv(sdelay_rise))+
 " = "+str(fQS(simpulse_down))+"\\newline "+
 str(fR(sfall))+" \\cup "+str(fQSinv(sdelay_rise))+
 " = "+str(fQR(simpulse_down))+
 "$&\\scriptsize$"+
 str(pfall)+"\\cup"+str(pdelay_rise)+"="+str(pimpulse_down)+"\\newline "+
 str(pfall)+"\\cup"+str(pdelay_rise)+"="+str(pimpulse_down)+"$  \\\ \
\\hline 05&\\scriptsize$ "+
 str(fprior(fQRinv(srise)))+" = "+str(fpost(fQRinv(sdelay_rise)))+"\\newline "+
 str(fprior(fQSinv(srise)))+" = "+str(fpost(fQSinv(sdelay_rise)))+
 "$&\\scriptsize$"+
 str(erise)+"= "+str(erise)+"\\newline "+
 str(erise)+"= "+str(erise)+"$  \\\ \
 \\hline 06&\\scriptsize$ "+
 str(fprior(fS(sbottom)))+" \\cup "+str(fprior(fQRinv(srise)))+
 " = "+str(fprior(fQS(srise)))+"\\newline "+
 str(fprior(fR(sbottom)))+" \\cup "+str(fprior(fQSinv(srise)))+
 " = "+str(fprior(fQR(srise)))+
 "$&\\scriptsize$"+
 str(ebottom)+"\\cup"+str(erise)+"="+str(erise)+"\\newline "+
 str(ebottom)+"\\cup"+str(erise)+"="+str(erise)+"$  \\\ \
\\hline 07&\\scriptsize$ "+
 str(fpost(fQRinv(sdelay_fall)))+" = "+str(fprior(finv(fQR(srise))))+"\\newline "+
 str(fpost(fQSinv(sdelay_fall)))+" = "+str(fprior(finv(fQS(srise))))+
 "$&\\scriptsize$"+
 str(efall)+"=\\overline{"+str(erise)+"}\\newline "+
 str(efall)+"=\\overline{"+str(erise)+"}$  \\\ \
\\hline 08&\\scriptsize$ "+
 str(fpost(fS(sbottom)))+" \\cup "+str(fpost(fQRinv(sdelay_fall)))+
 " = "+str(fpost(fQS(sdelay_fall)))+"\\newline "+
 str(fpost(fR(sbottom)))+" \\cup "+str(fpost(fQSinv(sdelay_fall)))+
 " = "+str(fpost(fQR(sdelay_fall)))+
 "$&\\scriptsize$"+
 str(ebottom)+"\\cup"+str(efall)+"="+str(efall)+"\\newline"+
 str(ebottom)+"\\cup"+str(efall)+"="+str(efall)+"$  \\\ \
\\hline 09&\\scriptsize$ "+
 str(fS(sbottom))+" \\cup "+str(fQRinv(simpulse_up))+
 " = "+str(fQS(simpulse_up))+"\\newline "+
 str(fR(sbottom))+" \\cup "+str(fQSinv(simpulse_up))+
 " = "+str(fQR(simpulse_up))+
 "$&\\scriptsize$"+
 str(pbottom)+"\\cup"+str(pimpulse_up)+"="+str(pimpulse_up)+"\\newline "+
 str(pbottom)+"\\cup"+str(pimpulse_up)+"="+str(pimpulse_up)+"$  \\\ \
\\hline 10&\\scriptsize$ "+
 str(fprior(fQRinv(sfall)))+" = "+str(fpost(fQRinv(sdelay_fall)))+"\\newline "+
 str(fprior(fQSinv(sfall)))+" = "+str(fpost(fQSinv(sdelay_fall)))+
 "$&\\scriptsize$"+
 str(efall)+"= "+str(efall)+"\\newline "+
 str(efall)+"= "+str(efall)+"$  \\\ \
\\hline 11&\\scriptsize$ "+
 str(fprior(fS(sbottom)))+" \\cup "+str(fprior(fQRinv(sfall)))+
 " = "+str(fprior(fQS(sfall)))+"\\newline "+
 str(fprior(fR(sbottom)))+" \\cup "+str(fprior(fQSinv(sfall)))+
 " = "+str(fprior(fQR(sfall)))+
 "$&\\scriptsize$"+
 str(ebottom)+"\\cup"+str(efall)+"="+str(efall)+"\\newline "+
 str(ebottom)+"\\cup"+str(efall)+"="+str(efall)+"$  \\\ \
\\hline 12&\\scriptsize$ "+
 str(fpost(fQRinv(sdelay_rise)))+" = "+str(fprior(finv(fQR(sfall))))+"\\newline "+
 str(fpost(fQSinv(sdelay_rise)))+" = "+str(fprior(finv(fQS(sfall))))+
 "$&\\scriptsize$"+
 str(erise)+"=\\overline{"+str(efall)+"}\\newline "+
 str(erise)+"=\\overline{"+str(efall)+"}$  \\\ \
\\hline 13&\\scriptsize$ "+
 str(fpost(fS(sbottom)))+" \\cup "+str(fpost(fQRinv(sdelay_rise)))+
 " = "+str(fpost(fQS(sdelay_rise)))+"\\newline "+
 str(fpost(fR(sbottom)))+" \\cup "+str(fpost(fQSinv(sdelay_rise)))+
 " = "+str(fpost(fQR(sdelay_rise)))+
 "$&\\scriptsize$"+str(ebottom)+"\\cup"+str(erise)+"="+str(erise)+"\\newline "+
 str(ebottom)+"\\cup"+str(erise)+"="+str(erise)+"$  \\\ \
\\hline 14&\\scriptsize$ "+
 str(fS(sbottom))+" \\cup "+str(fQRinv(simpulse_down))+
 " = "+str(fQS(simpulse_down))+"\\newline "+
 str(fR(sbottom))+" \\cup "+str(fQSinv(simpulse_down))+
 " = "+str(fQR(simpulse_down))+
 "$&\\scriptsize$"+
 str(pbottom)+"\\cup"+str(pimpulse_down)+"="+str(pimpulse_down)+"\\newline "+
 str(pbottom)+"\\cup"+str(pimpulse_down)+"="+str(pimpulse_down)+"$  \\\ \
\\hline \\end{tabular} \\end{table} ")      


At("The initial equation of SR flip flop was illustrate in "+vD[sQSR][0][1]+
   "with restriction that S and R were disjoint sets. Lets consider a \
    disjoint set case as follows.")

Ce(Eq(sR,finv(sS)),sSinv);Ad(key=sR)                                           #72   

At("Then")
Ae(latex(sS)+" \\subset "+ latex(sQS));Ad(key=sS)                              #74 
Ae(latex(sR)+" \\subset "+ latex(sQR));Ad(key=sR)                              #74 
Ce(Eq(sQR,finv(sQS)),sQSinv);Ad(key=sQR)                                       #75   

At("Substituting, "+vD[sR][9][1]+" and "+vD[sQR][2][1]+" in "+vD[sR][10][1]+", ")

Ae(latex(sSinv)+" \\subset " + latex(sQSinv));Ad(key=sS)                       #76


At("From "+vD[sS][9][1]+" and "+vD[sS][10][1]+", the following were determined. ")
Ce(sQS,sS)                                                                     #77  
Ce(sQR,sSinv)                                                                  #78 

At("For ")

phi = symbols("\\phi")

Ce(sS+sR,phi)                                                                  #79
ltD=len(tD)-1
tD[ltD]=tD[ltD].replace("+","\\cup") 

At("Then, ")
Ae(latex(phi)+" \\subset "+ latex(sQS)+"="+latex(sQS));Ad(key=sQS)             #80
Ae(latex(phi)+" \\subset "+ latex(sQR)+"="+latex(sQR));Ad(key=sQR)             #81

At("For "+Ml(sS)+"$\\cap$"+Ml(sR)+"="+Ml(stop)+", ")

Ce(Eq(sQS,sQR),stop)                                                           #82


At("Finally, the SR flipflop model was completed as follows.")

S=Matrix([sS,sSinv])
SR=Matrix([sS, sR ])
QSRinv=Matrix([sQRinv, sQSinv])
QSR=Matrix([sQS, sQR]) 
QSRpulses=Matrix([[stop,simpulse_up,srise],[stop,simpulse_up,srise]])     
SRpulses=Matrix([stop,simpulse_up,srise]).transpose()
QSRundefined=Matrix([[simpulse_down,simpulse_up,simpulse_down, simpulse_up, dots],
                     [simpulse_down,simpulse_up,simpulse_down, simpulse_up, dots]])
SRundefined=Matrix([sfall,sbottom,sbottom,sbottom,dots]).transpose()

Ae(latex(QSR)+"=\\begin{cases} "+latex(SR)+" \\cup "+latex(QSRinv)+
   " & \\\ \\text{for}\\: "+latex(sS)+" \\cap "+latex(sR)+" = \\phi \\\ \ \\\ "+
   latex(QSR)+
   " & \\\ \\text{for}\\: "+latex(sS)+" \\cup "+latex(sR)+" = \\phi \\\ \ \\\ "+
   latex(S)+
   " & \\\ \\text{for}\\: "+latex(sR)+" = "+latex(sSinv)+"  \\\ \ \\\ "+
   latex(Matrix([stop,stop]))+
   " & \\\ \\text{for}\\: "+latex(sS)+" \\cap "+latex(sR)+" = "+
   latex(stop) + "\\\ \ \\\ "+
   latex(QSRundefined)+
   " & \\\ \\text{for}\\: "+latex(sS)+" \\cap "+latex(sR)+" = "+
   latex(SRundefined) + "\\end{cases}")                                        #83

ltD=len(tD)
tD[ltD-1]=tD[ltD-1]

At("\\section{Conclusion}")


At("The set theory could be used to model the SR Flipflop. The classification of \
    pulses were designed to facilitate the formulation of prior and post event \
    functions. The basic set element was the stem and the dot at a point in time. \
    The stem was present if the logic state was 1 and the dot appeared if if the \
    logic state was 0.  A pulse was designed to consist of a set of tri-tuple \
    {t-1,t,t+1}. The number of combination of $2^3=8$ was exhausted that yielded \
    8 categories of pulses. The prior (t-1,t) and post (t,t+1) events were \
    realized from the tri-tuple perspective anchored in t. The classification of \
    pulses were based on the observaton made on the behavior of prior and post \
    events over the 8 combinations of tri-tuple. The delayed category was \
    specifically applied for no change in prior event but with change in post \
    events.\\\ \ \\\ \
    The concept was tested through a process of derivation of circuits for \
    simple latch and SR flipflop. After a number of thought experiments and \
    simulations, the method of calculation was established. The prior function \
    became the front end for handling input to output operation. The post function \
    became the backend for handling output to input feedback operation.  \
    The prior event of the output was the post event feedback to the input. \
    The union of the prior and post events led to the the now event equation. \
    \\\ \ \\\ \
    Finally, the thorough model of SR flipflop was formulated under different \
    input conditions in piecewise form. The undefine behavour was included and \
    fully articulated. The memory and the buffer feature were expressed. \\\ \ \\\ \
    ")


At("\\begin{thebibliography}{00} \n\
\\bibitem{b1} Patric Suppes, \"Axiomatic Set Theory\" Copyright @ 1972 \
    Dover Publication, Inc., New York\
\\bibitem{b2} Rossum, Guido van,\"Python 3.6.5\",Python Software Foundation. \
    \\url{https://www.python.org/}, 2018 \
\\bibitem{b3} Sympy Development Team,\"SymPy 1.3\",Github. \
    \\url{https=//github.com/sympy/sympy},2018 \
\\bibitem{b4} Thomas Feuerstack,\"proTeXt - MiKTeX-based distribution for Windows \",\
    TUG home page; \\url{https://www.tug.org/protext/}, 2019, proTeXt's creator \
    and principal maintainer is Thomas Feuerstack, while MiKTeX was created \
    and continues to be maintained by Christian Schenk. Many thanks to both. \
\\bibitem{b5} Anaconda,\"Anaconda 5.3 For Windows Installer \" \
    Anaconda, Inc. All Rights Reserved, \\url{https://www.anaconda.com/download/},\
    2018 \
\\bibitem{b6} IEEE, \"Manuscript Templates for conference Proceedings\"\
    \\url{https://www.ieee.org/conferences/publishing/templates.html} \
\\bibitem{b7} Benito van der Zander, Jan Sundermeyer, Daniel Braun, \
        Tim Hoffmann (TeXstudio), Pascal Brachet (Texmaker), \
        Luc Buant (QCodeEdit), Joel Amblard (html conversion),\
        \"TeXStudio 2.12.10 \",Source Forge, \\href{https://www.texstudio.org/} {TexStudio} ,\
        2018, download from \\url{https://sourceforge.net/projects/texstudio/} \
\\bibitem{b8} Raybaut, Pierre,\"Spyder 3.2.8, The Scientific Python Development \
    Environment\", The Spyder Project Contributors, Licensed under the terms of \
    the MIT License, 2018, Download from \\url{https://github.com/spyder-ide/spyder}\
\\end{thebibliography} \n")

"""
\\bibitem{b9} Altshuller, Genrich, H. Altove, Lev Shulyak,  \
    \\href{https://books.google.com.sg/books?id=s7Qk_6WELWUC&printsec=frontcover&source=gbs_ge_summary_r&cad=0#v=onepage&q&f=false}\
     {And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving}\
\\bibitem{b10} Innovation-TRIZ, \\textcolor{blue}{\\href{https://www.innovation-triz.com/TRIZ40/}\
     {TRIZ Matrix}}\
\\bibitem{b11} Litvin, Simon, Vladimir Petrov, Mikhail Rubin, TRIZ Body of Knowledge, \
     International TRIZ Association (MA TRIZ) and \\\ \
     Frey, Victor, Altshuller Institute for TRIZ studies, \
     \\url{https://www.aitriz.org/triz/triz-body-of-knowledge}\
\\bibitem{b12} Lerner, Leonid, Genrich, Altshuller:Father of TRIZ, \
     \\url{https://www.aitriz.org/altshuller/116-altshuller/775-genrich-altshuller}, \
     accessed 2020\
\\bibitem{b12} Altshuller, Genrich, Altshuller Institute for TRIZ studies, \
     \\url{https://www.aitriz.org/triz}, accessed 2020\
\\bibitem{b13} 40 Inventive Principles, The TRIZ Journal , \
     \\url{https://triz-journal.com/40-inventive-principles-examples/}, 2020\

"""

#9.0 About the Author
At("\\section*{About the Authors} ")


#Begin to be filled by user

ABT=[
     {'ID'     :'cco.png',
      'Author' :'Celso Bation Co',
      'Account':'He earned his diploma as Electronic Technician from International \
       Correspondence Schools of University of Pennsylvania in 1972. He obtained \
       his degree of Bachelor of Science in Electronics and Communication \
       Engineering (ECE) from the University of Sto Tomas in 1977, Master  \
       and Doctoral degrees in ECE from De La Salle University in 1996 and \
       2007 respectively. He is currently the guest lecturer at Batangas \
       State University. He advocates strong linkages among academes, industries \
       and government.'},
      ]

def AbtItem(var):
    l=len(var)
    About=""
    for i in range(l):
        temp="\\begin{IEEEbiography}[{\\includegraphics[width=2.5cm,height=2.5cm,clip, \
              keepaspectratio]{"+var[i]['ID']+"}}]{"+var[i]['Author']+"} "+\
              var[i]['Account']+"\\end{IEEEbiography} "
        About+=temp
    About+="\n"
    return About

At(AbtItem(ABT))

show()


Pb(Filename="Signals.tex")
