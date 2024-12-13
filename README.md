# EITP40_Final_Project
The current model is used to recognize numbers. The tester first draws numbers in the air with the board, and the model is used to classify and recognize which number is drawn (0-9, a total of ten categories). You can directly compile and upload IMU_Classifier.ino to test it. However, the method of drawing numbers requires a little trick, you can try more. If you don’t understand, you can refer to https://docs.arduino.cc/tutorials/nano-33-ble-sense/get-started-with-machine-learning/

I have completed the code for collecting data and the final classifier (most of them are open source, I just made some adjustments). But I used python to train the model, not on the board. val_accuracy can reach 95%. But the actual recognition effect is not so ideal. The main reason should be that there are too few samples. The original training data only has 11 groups of samples for each category, and 20% is used as a validation set (forgive me, these 11*10 groups of data have made my hands sore).

I think the gestures can be redesigned. Or reduce the number of categories, such as only recognizing a few specific numbers with high accuracy. This will give you more training data.

Another option is to train on Arduino, but I haven't tried it yet. It shouldn't be too complicated. You just need to set the parameters of the training set and the model. You can study it.