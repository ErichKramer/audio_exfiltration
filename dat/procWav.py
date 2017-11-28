#THIS FILE EXISTS TO SPLIT A LARGER AUDIO FILE INTO INDIVIDUAL KEYSTORKE WAVES
#DUMPS TO SUBDIR "out"
#IT IS NOT PERFECT
import pydub
import sys, os, string

def dumpSplit(filepath, tag, featLen = .2):
    if not os.path.isfile(filepath):
        return []

    parentDir = os.path.abspath(os.path.join(filepath, os.pardir))
    sound = pydub.AudioSegment.from_wav(filepath)
    chunks = pydub.silence.split_on_silence(sound, \
            min_silence_len=40, silence_thresh =-48, keep_silence=0)
    featLen = .2

    chunks = [chunk for chunk in chunks \
            if chunk.max > 1100 and chunk.duration_seconds < .8 and chunk.duration_seconds >= featLen]

    chunks = [chunk[0:featLen*1000] for chunk in chunks] #slice all files so that tehy are thee same length

    #filter too quiet sounds (not keystrokes) and too long sounds (multiple or not keystroke clips)
    #this is necessary to guarantee same size feature vectors.

    outDir = parentDir + "/out/"
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    #output each chunk as a seperate file into /out directory
    for i, chunk in enumerate(chunks):
            chunk.export(outDir + tag + str(i) + ".wav", format="wav")

    print(tag, " is ", len(chunks))

def clearOut():


if __name__ =="__main__":


    #assumes working directory contains all files needed, does nothing if file not found
    for char in string.ascii_uppercase:
        dumpSplit(char+"_100.wav", char)


    exit(0)



