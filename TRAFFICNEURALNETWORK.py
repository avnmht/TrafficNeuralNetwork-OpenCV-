import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical
from keras.layers import Dropout,Flatten
from keras.layers.convolutional import Conv2D,MaxPooling2D
import cv2
from sklearn.model_selection import train_test_split
import pickle
import os
import pandas as pd
import random
from keras.preprocessing.image import ImageDataGenerator

path="DATA"
labelfile="labels.csv"
batch_size_val=50
steps_per_epoch_val=2000
epochs_val=20
imageDimensions=(32,32,3)
testratio=0.2
validationratio=0.2

count=0
Images=[]
Classno=[]
mylist=os.listdir(path)
print("Total Classes Detected: ",len(mylist))
noofclasses=len(mylist)
print("Importing Classes .....")
for i in range(0,len(mylist)):
    mypics=os.listdir("DATA/" + str(count))
    for y in mypics:
        current=cv2.imread(path+"/"+str(count)+"/"+ y)
        Images.append(current)
        Classno.append(count)
    print(str(count) + "/" + str(noofclasses))
    count=count+1
print(str(noofclasses)+("/")+str(noofclasses))
print(" ")
#print(Images)
#print(Classno)
Images=np.array(Images)
Classno=np.array(Classno)
print(Images.shape)
print(Classno.shape)




X_train, X_test, Y_train, Y_test = train_test_split(Images,Classno,test_size=testratio)
X_train, X_validation ,Y_train, Y_validation = train_test_split(X_train,Y_train,test_size=validationratio)

################################################
print("DATA SHAPES")
print("Train:  ")
print(X_train.shape,Y_train.shape)
print("Validation:   ")
print(X_validation.shape, Y_validation.shape)
print("Test:  ")
print(X_test.shape,Y_test.shape)

data=pd.read_csv(labelfile)
print("data_shape",data.shape,type(data))

def grayscale(img):
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return img
def equalize(img):
    img=cv2.equalizeHist(img)
    return img
def preprocessing(img):
    img=grayscale(img)
    img=equalize(img)
    img=img/255.0
    return img

X_train=np.array(list(map(preprocessing,X_train)))
X_validation=np.array(list(map(preprocessing,X_validation)))
X_test=np.array(list(map(preprocessing,X_test)))
cv2.imshow("Gray Scale Images: ", X_train[random.randint(0,len(X_train)-1)])
cv2.waitKey(0)

X_train=X_train.reshape(X_train.shape[0],X_train.shape[1],X_train.shape[2],1)
X_validation=X_validation.reshape(X_validation.shape[0],X_validation.shape[1],X_validation.shape[2],1)
X_test=X_test.reshape(X_test.shape[0],X_test.shape[1],X_test.shape[2],1)

datagen=ImageDataGenerator(width_shift_range=0.1,height_shift_range=0.1,zoom_range=0.2,shear_range=0.1,rotation_range=10)
datagen.fit(X_train)
batches=datagen.flow(X_train,Y_train,batch_size=20)
X_batch,Y_batch=next(batches)

Y_train=to_categorical(Y_train,noofclasses)
Y_validation=to_categorical(Y_validation,noofclasses)
Y_test=to_categorical(Y_test,noofclasses)

def mymodel():
    nooffilters=60
    sizeoffilters=(5,5)
    sizeoffilters2=(3,3)
    sizeofpool=(2,2)
    noofnodes=500
    model=Sequential()
    model.add((Conv2D(nooffilters,sizeoffilters,input_shape=(imageDimensions[0],imageDimensions[1],1),activation='relu')))
    model.add((Conv2D(nooffilters,sizeoffilters,activation='relu')))
    model.add(MaxPooling2D(pool_size=sizeofpool))

    model.add((Conv2D(nooffilters//2,sizeoffilters2,activation='relu')))
    model.add((Conv2D(nooffilters//2,sizeoffilters2,activation='relu')))
    model.add(MaxPooling2D(pool_size=sizeofpool))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(noofnodes,activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(noofclasses,activation='softmax'))

    model.compile(Adam(lr=0.001),loss='categorical_crossentropy',metrics=['accuracy'])
    return model

###################33
model=mymodel()
history=model.fit_generator(datagen.flow(X_train,Y_train,batch_size=batch_size_val),steps_per_epoch=steps_per_epoch_val,epochs=epochs_val,validation_data=(X_validation,Y_validation),shuffle=1)
score=model.evaluate(X_test,Y_test,verbose=0)
print('Test Score: ',score[0])
print('Test Accuracy: ',score[1])

#################
pickle_out=open("model_trained_avnmht.p","wb")
pickle.dump(model.pickle_out)
pickle_out.close()
cv2.waitKey(0)

    


