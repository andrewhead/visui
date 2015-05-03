'''
(c) May 2015 by Daniel Seita

This script will use the caffe snapshots to classify images in our testing set. This accuracy is
ultimately one of the main things we should be reporting. We will need to iterate through lots of
different snapshots. In addition, for each snapshot, we have 8000 testing images to assess, with
2000 per class.

Some assumptions:

(1) This file should be in the CS280_FinalProject directory, which is in 
    {caffe_root}/CS280_FinalProject
and it also has a "snapshots" folder inside it, i.e., 
    {caffe_root}/CS280_FinalProject/snapshots
that will contain the snapshots that I need to provide as input to the code. Use the function
os.listdir("snapshots") to list all the snapshots, then grab those that end in ".caffemodel".

(2) This file is in the same directory as the files
    videos_v2_test_all.txt
    videos_v2_test_nonoise.txt
These will contain the testing image file names. The raw path should be specified earlier.

(3) We also need to make it clear when we are using "nonoise" or "all" data.

(4) For the mean file, it's a little more complicated; see some stuff on the documentation.
'''

# First, the boring part...
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
caffe_root = "../"
sys.path.insert(0, caffe_root + "python")
import caffe
caffe.set_mode_gpu()
image_root = "/Users/danielseita/UC_Berkeley_Material/CS_280-Computer_Vision/" \
    "FinalProject/Videos_and_Images/"
output_directory = "results/"

########
# MAIN #
########

# Important! Set false if we want to use our nonoise data.
all_data = False
if all_data:
    image_root = image_root + "Images_All/"
else:
    image_root = image_root + "Images_NoNoise/"
print "all_data is set to be " + str(all_data)

# Step 1: MODEL_FILE is the prototxt file, PRETRAINED contains the .caffe models with weights.
# EDIT: These are NOT the train/val prototxt files, but the DEPLOYMENT prototxt files!!!
MODEL_FILE = ""
if all_data:
    MODEL_FILE = "alexnet_deploy_all.prototxt"
else:
    MODEL_FILE = "alexnet_deploy_nonoise.prototxt"
PRETRAINED_FILES = [] # Note that we will need "snapshots/" prepended.
for filename in os.listdir("snapshots"):
    if "caffemodel" in filename:
        if (all_data and "all" in filename) or (not all_data and "nonoise" in filename):
            PRETRAINED_FILES.append(filename)

# Step 2: Now deal with the image files, and then load/format them for caffe.
# We have done this earlier in caffeimages_test_{all,nonoise}.gz so we can just do np.loadtxt(...)
# Note that we can use the original text for adding image roots. BUT we do know that these classes
# are arranged in 0-1-2-3 fashion in a repeated manner.
print "Now loading images (this may take a few minutes) ..."
IMAGE_FILES = []
if all_data:
    with open('videos_v2_test_all_1000.txt', 'r') as f:
        for line in f:
            IMAGE_FILES.append(caffe.io.load_image(image_root + line.split()[0]))
else:
    with open('videos_v2_test_nonoise_1000.txt', 'r') as f:
        for line in f:
            IMAGE_FILES.append(caffe.io.load_image(image_root + line.split()[0]))
print "Finished with loading images."

# Step 3: Create the mean file. I THINK this is correct...
blob = caffe.proto.caffe_pb2.BlobProto()
data = ""
if all_data:
    data = open("videos_v2_train_all_mean.binaryproto","rb").read()
else:
    data = open("videos_v2_train_nonoise_mean.binaryproto","rb").read()
blob.ParseFromString(data)
arr = np.array( caffe.io.blobproto_to_array(blob) )
numpy_mean = arr[0]
print "Finished with numpy_mean: " + str(numpy_mean)

# Step 4: Now let's get to classification. For the sake of being modular, save all this to txt
# files. Then we can plot this information. Make sure IMAGE_FILES_CAFFE is OK!
for caffemodel in PRETRAINED_FILES:
    print "Currently on caffemodel of " + str(caffemodel)
    net = caffe.Classifier(model_file = MODEL_FILE, 
                           pretrained_file = "snapshots/" + caffemodel,
                           mean = numpy_mean.mean(1).mean(1),
                           channel_swap=(2,1,0),
                           raw_scale=255, # TODO is this raw_scale and image_dim appropriate?
                           image_dims=(256, 256))
    print "Now predicting on it ..."
    predictions = net.predict(IMAGE_FILES) # Predicts on everything in this file
    np.savetxt(output_directory + caffemodel + "_preds", predictions)

