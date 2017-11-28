import numpy as np
import python_speech_features as psf
import pydub, pydub.playback 
import os, sys, string, glob
import scipy.io.wavfile
from sklearn import svm, neighbors
datPath = "./dat/out/"


#returns feature vector for each wav matching string passed in
def getFeat(string):
    #print(datPath+string)
    waves = glob.glob(datPath + string)
    #print(waves)
    data = []
    for clip in waves:
        (rate, sig) = scipy.io.wavfile.read(clip)
        sig.flatten()#make into Nx1, not sure if has effect
        #tmp = np.fft.fft(sig)
        data.append( psf.mfcc(sig, rate, nfft=1200).flatten() )
        #flatten into 1D feature vector so taht we can use as feature vector
    return data


def testSVM(model, devDat):
    total = 0
    correct = 0
    for i, charProf in enumerate(devDat):
        for inst in charProf:
            total +=1
            pred = model.predict([inst])
            #print(pred)

            if pred[0] == i:
                correct +=1

    print("Total : ", total, "Correct: ", correct)
    return correct/total

def audioSVM(features, holdout=.1):
    #features[0] = 'A', features[1] = 'B' and so on
    
    #create dev set
    dev = []
    for i,charProf in enumerate(features):
        splitIDX = int(len(charProf) *(1-holdout))
        dev.append( charProf[splitIDX:])
        features[i] = charProf[:splitIDX]
    #print(dev)
    labels = []
    for i, charProfile in enumerate(features):
        labels += [i]*len(charProfile)

    #flatten alpha into list of feature vectors
    features = [ featVect for charProf in features for featVect in charProf ]
    
    print(labels)
    state = np.random.get_state()
    np.random.shuffle(features)
    np.random.set_state(state)
    np.random.shuffle(labels)
    
    neigh = neighbors.KNeighborsClassifier(n_neighbors=3)
    neigh.fit(features, labels)

    
    clf = svm.SVC(C = 10, gamma = 1**-20)
    clf.fit(features, labels)
    
    print("Accuracy: ", testSVM(neigh, dev))



if __name__ == "__main__":

    alpha = [ np.array(getFeat(char + "*.wav")) for char in string.ascii_uppercase]
    
    profile = []
    for block in alpha:
        if len(block)>0:
            profile.append(sum(block)/len(block))
    '''
    total=correct=0
    for i, block in enumerate(alpha):
        for inst in block:
            total+=1
            dists = [ np.linalg.norm(inst - x) for x in profile ]
            if dists.index(min(dists)) == i:
                print(i)
                correct +=1

    print("Acc: ", correct/total)
    '''

    audioSVM(alpha)
    #tmp = getFeat("B*.wav")
    print(alpha[1].shape)
    print(len(alpha))
    #print(tmp)





