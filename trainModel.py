import numpy as np
from alexnet import alexnet2
from random import shuffle
import pandas as pd
import tflearn, os

# what to start at
START_NUMBER = 60

# what to end at
hm_data = 111

w = 160
h = 120

modelName = 'GTA5-TestModel-70k-data.model'
trainingDataName = 'trainingData.npy'
model = alexnet2(w, h, 6)

if os.path.isfile(modelName):
    print("File exists")
    model.load(modelName)

epochs = 10
for i in range(epochs):
    data_order = [i for i in range(START_NUMBER, hm_data + 1)]
    shuffle(data_order)

    for i in data_order:
        trainData = np.load(trainingDataName)

        df = pd.DataFrame(trainData)
        df = df.iloc[np.random.permutation(len(df))]
        trainData = df.values.tolist()

        train = trainData[:-100]
        test = trainData[-100:]

        X = np.array([i[0] for i in train]).reshape(-1, w, h, 1)
        Y = [i[1] for i in train]

        test_x = np.array([i[0] for i in test]).reshape(-1, w, h, 1)
        test_y = [i[1] for i in test]

        tflearn.init_graph(num_cores=4, gpu_memory_fraction=0.5)
        model.fit(X, Y, n_epoch=1, validation_set=(test_x, test_y),
                  shuffle=True, show_metric=True, snapshot_step=2000, run_id=modelName)

        model.save(modelName)
