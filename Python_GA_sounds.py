import math
import time
import random
import pyaudio

#things to figure out
    #what note is chord
    #major vs minor
    #various lengths
    #groups of sequences of chors
    #play notes in chord in random order
        #- remember order randomness

#sudo apt-get install python-pyaudio
PyAudio = pyaudio.PyAudio

#See http://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 16000 #number of frames per second/frameset.

#Frequencies
A4  = 440
As4 = 466.164
B4  = 493.883
C4  = 261.626
Cs4 = 277.183
D4  = 293.665
Ds4 = 311.127
E4  = 329.628
F4  = 349.228
Fs4 = 369.994
G4  = 391.995
Gs4 = 415.305
A5  = 880
As5 = 932.328
B5  = 987.767
C5  = 523.251
D5  = 587.330

#g c d g
#g c d c
# mj = major, mn = minor
A3_mj = [A4,Cs4,E4] #0 A4 Cs4 E4
A3_mn = [A4,C4,E4]  #1 A4 C4  E4
B3_mj = [B4,Ds4,Fs4]#2 B4 Ds4 Fs4
B3_mn = [B4,D4,F4]  #3 B4 D4  F4
C3_mj = [C4,E4,G4]  #4 C4 E4  G4
C3_mn = [C4,Ds4,G4] #5 C4 Ds4 G4
D3_mj = [D4,Fs4,A5] #6 D4 Fs4 A5
D3_mn = [D4,F4,A5]  #7 D4 F4  A5
E3_mj = [E4,Gs4,B5] #8 E4 Gs4 B5
E3_mn = [E4,G4,B5]  #9 E4 G4  B5
F3_mj = [F4,A4,C5]  #10 F4 A4  C5
F3_mn = [F4,Gs4,C5] #11 F4 Gs4 C5
G3_mj = [G4,B5,D5]  #12 G4 B5  D5
G3_mn = [G4,As5,D5] #13 G4 As5 D5

#Global Chromosomes. all have 10 Alleles
P1 = [12,12,12,12,12,12] #[0,2,4,6,8,10,12] # All Major Seed
P2 = [12,12,12,12,12,12] #[13,11,9,7,5,3,1] # All Mingor Seed
C1 = [12,12,12,12,12,12] #[0,2,4,6,8,10,12] # Child 1
C2 = [12,12,12,12,12,12] #[13,11,9,7,5,3,1]# Child 2
L = .3 # length to play a sound for
    
def dlight (FREQUENCY, LENGTH):
    "plays a frequency for a length"

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = ''
    
    for x in range(NUMBEROFFRAMES):
        WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/(2*math.pi)))*127+128))    

    #fill remainder of frameset with silence
    for x in range(RESTFRAMES): 
        WAVEDATA = WAVEDATA+chr(128)

    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 2, 
                    rate = BITRATE, 
                    output = True)
    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return

def miccheck():
    "loop to find the light frequencies"
    freq = 4000; # starting frequency
    for i in range(0,40): # band to  sweep
        print ('freq = ', freq)
        dlight(freq, 5)   # see what lights get triggered
        freq = freq + 100 # increment size
    # end for loop
    return

def crossover():
    "make children"
    # since we need to change the globals
    global C1
    global C2
    size = len(P1)
    index1 = random.randint(1, size - 1)
    #print index1
    index2 = random.randint(1, size - 1)
    #print index2
    if index1 > index2:
        index1 = index2
        index2 = index1
    temp1 = P1[0:index1]
    temp2 = P2[index1:index2]
    temp3 = P1[index2:size]
    C1 = temp2 + temp1 + temp3
    temp1 = P2[0:index1]
    temp2 = P1[index1:index2]
    temp3 = P2[index2:size]
    C2 = temp2 + temp1 + temp3
    mutate_one_index(C1)
    mutate_one_index(C1)
    mutate_mult_index(C1)
    mutate_mult_index(C2)
    mutate_one_index(C2)
    return

def mutate_one_index(C):
    size = len(C)
    index = random.randrange(0,size)
    mutate_value = random.randrange(0,13)
    C1[index] = mutate_value 
    return 

def mutate_mult_index(C):
    size = len(C)
    while True:
        index1 = random.randrange(0,size)
        index2 = random.randrange(0,size)
        if (index1 != index2):
           temp  = C[index1]
           C[index1] = C[index2]
           C[index2] = temp
           break
    
    return 

def evaluate():
   "select children for crossover"
   global P1
   global P2
   P1 = P2 # get rid of oldest parent
#   ask user "first or second?"
   while 1:    
    x = int(input("Press 1 if you like chromose 1 , Press 2 if you like chromosome 2"))
    if x == 1:
        print("Chromosome 1 selected")
        P2 = C1    
        break
    elif x == 2:
        print("Chromosome 2 selected")
        P2 = C2
        break
    elif x==3:
        print("neither was adequate")
        break
    else:
        print("wrong selection, please press  1 or 2")
def play(F):
    DecodeChord(F)

def DecodeChord(F): # select elemenf of chord array
    "play sequence"
    FREQUENCY = 1
    for i in range(len(F)):
        wait = 1;
        if F[i] == 0:  
            PlayChord(A3_mj)
        elif F[i] == 1:
            PlayChord(A3_mn)
        elif F[i] == 2:
            PlayChord(B3_mj)
        elif F[i] == 3:
            PlayChord(B3_mn)
        elif F[i] == 4:
            PlayChord(C3_mj)
        elif F[i] == 5:
            PlayChord(C3_mn)
        elif F[i] == 6:
            PlayChord(D3_mj)
        elif F[i] == 7:
            PlayChord(D3_mn)
        elif F[i] == 8:
            PlayChord(E3_mj)
        elif F[i] == 9:
            PlayChord(E3_mn)
        elif F[i] == 10:
            PlayChord(F3_mj)
        elif F[i] == 11:
            PlayChord(F3_mn)
        elif F[i] == 12:
            PlayChord(G3_mj)
        elif F[i] == 13:
            PlayChord(G3_mn)
        #    wait = 0
        #if wait == 1:
        
        #elif wait == 0:
        #    time.sleep(L)
def PlayChord(S): # iteratively play frequencies in chord
    for i in range(len(S)):
        dlight (S[i], L)

def main():
    #first children
    gen = 0 # generation counter
    again = 1
   # miccheck()
    while(again):
        print('playing sequence one')
        play(C1)
        time.sleep(1)
        print('playing sequence two')
        play(C2)
        evaluate()
        crossover()
        gen = gen + 1
        print ('generation ', gen)
        again = input(' again? 1 yes 0 no: ')
    #end while loop

if __name__=="__main__":
    main()
