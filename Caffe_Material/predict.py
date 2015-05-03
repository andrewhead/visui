'''
Given a whole bunch of numpy arrays as a result of the classify.py script, actually predict these
and plot the results!

(c) May 2015 by Daniel Seita

Call this in the caffe/CS280_FinalProject directory! It must have results/ in it where that
directory contains all the numpy prediction arrays.
'''

import numpy as np
import matplotlib.pyplot as plt
import re
import os

total_test = 1000
accuracy_results = {} # Goes from (iter#) -> (accuracy)
for filename in os.listdir("results"):
    predicted_classes = np.argmax(np.loadtxt("results/" + filename),axis=1)
    correct = 0
    for i in range(len(predicted_classes)):
        if (i % 4 == 0 and predicted_classes[i] == 0):
            correct += 1
        elif (i % 4 == 1 and predicted_classes[i] == 1):
            correct += 1
        elif (i % 4 == 2 and predicted_classes[i] == 2):
            correct += 1
        elif (i % 4 == 3 and predicted_classes[i] == 3):
            correct += 1
    iteration_number = int(re.findall('\d+', filename)[0])
    accuracy_results[iteration_number] = float(correct)/total_test
print accuracy_results

x_axis = []
y_axis = []
for key_num in accuracy_results:
    x_axis.append(int(key_num))
    y_axis.append(float(accuracy_results[key_num]))
plt.figure()
plt.xlabel("Iteration Number")
plt.ylabel("Test Set Accuracy")
plt.plot(x_axis, y_axis)
plt.show()
