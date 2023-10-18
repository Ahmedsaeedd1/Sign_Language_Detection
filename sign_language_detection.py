# -*- coding: utf-8 -*-
"""Sign Language Detection

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fCSWR2jjN3nnwMS9oSnvmViIIWk-kkrq

*importing the needed libraries*
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import os
import keras
from keras.models import Sequential
from keras.layers import Dense , Flatten ,MaxPool2D , Dropout , Conv2D
import warnings
warnings.filterwarnings("ignore")

for dirname, _, filenames in os.walk("input"):
    for filename in filenames:
      print (os.path.join(dirname,filename))

"""# load the dataset"""

train_data= pd.read_csv("/content/sign_mnist_train.csv")
test_data= pd.read_csv("/content/sign_mnist_test.csv")

train_data.shape

train_data.head()

test_data.shape

test_data.head()

test_data.describe()

train_data.describe()

"""# Data preprocessing"""

train_lb =train_data['label']
train_lb.head()

train_set= train_data.drop(['label'], axis=1)
train_set.head()

X_train = train_set.values
X_train = train_set.values.reshape(-1,28,28,1)
print (X_train.shape)

test_label=test_data['label']
X_test=test_data.drop('label',axis=1)
X_test.shape

X_test.head()

from sklearn.preprocessing import LabelBinarizer
lb=LabelBinarizer()
y_train=lb.fit_transform(train_lb)
y_test=lb.fit_transform(test_label )

X_test = X_test.values.reshape(-1,28,28,1)

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=0,
    height_shift_range=0.2,
    width_shift_range=0.2,
    shear_range=0,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

X_test = X_test / 255

"""# Data visualiztion"""

fig , axe= plt.subplots(2,2)
fig.suptitle('perview of the dataset')
axe[0,0].imshow(X_train[0].reshape(28,28),cmap='gray')
axe[0,0].set_title('label: 3   letter :  C ')
axe[0,1].imshow(X_train[1].reshape(28,28),cmap='gray')
axe[0,1].set_title('label: 6   letter :  F')
axe[1,0].imshow(X_train[2].reshape(28,28),cmap='gray')
axe[1,0].set_title('label: 2   letter :  B')
axe[1,1].imshow(X_train[4].reshape(28,28),cmap='gray')
axe[1,1].set_title('label: 13   letter : M ')

"""# CNN model"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten
model = Sequential()
model.add(Conv2D(128, kernel_size=(5, 5), strides=1, padding='same', activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(3, 3), strides=2, padding='same'))
model.add(Conv2D(64, kernel_size=(2, 2), strides=1, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=2, padding='same'))
model.add(Conv2D(32, kernel_size=(2, 2), strides=1, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=2, padding='same'))

model.add(Flatten())

model.add(Dense(units=512,activation='relu'))
model.add(Dropout(rate=0.25))
model.add(Dense(units=24,activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(train_datagen.flow(X_train,y_train,batch_size=200),
                    epochs= 35, validation_data= (X_test ,y_test ),
                    shuffle= 1)

"""# Model Evaluation"""

history_df = pd.DataFrame(history.history)
history_df.loc[:, ['loss', 'val_loss']].plot()
history_df.loc[:, ['accuracy', 'val_accuracy']].plot()
plt.show()

(ls,acc)= model.evaluate(x=X_test,y=y_test)
print('The accuracy of the model  is {}%'.format(acc*100))

