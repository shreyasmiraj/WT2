
# coding: utf-8

# In[1]:

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import os
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

# In[2]:

def predictValue():

    img_width, img_height = 210, 210
    epochs = 10
    batch_size = 32

    if K.image_data_format() == 'channels_first':
        input_shape = (3, img_width, img_height)
    else:
        input_shape = (img_width, img_height, 3)


    # In[3]:



    model = Sequential()

    model.add(Conv2D(32, (3, 3), input_shape=(210,210,3)))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(5))
    model.add(Activation('softmax'))


    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.summary()

    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=False)

    # this is the augmentation configuration we will use for testing
    test_datagen = ImageDataGenerator(rescale=1. / 255)



    model.load_weights("model/Final.h5")
    model._make_predict_function()

    # In[6]:


    classList = ['corn gray leaf spot', 'corn common rust', 'corn healthy', 'peach bacterial spot', 'peach healthy']



    datagen = ImageDataGenerator(rescale=1. / 255)
    generator = datagen.flow_from_directory(
            'imagedata',
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='categorical',  # only data, no labels
            shuffle=False)  # keep data in same order as labels

    op = model.predict_generator(generator,1)
    maxprobability = max(op[0])

    for i in range(len(op[0])):
        if maxprobability == op[0][i]:
            maxprobabilityclass = i
            break
    return str(classList[maxprobabilityclass])