VEP-BCI
=======
python 2.7.6 32 bit

* (gevent 0.13.8)
* (greenlet 0.4.2)
* pycrypto 2.6
* pywinusb 0.3.3
* numpy 1.8.1
* scipy 0.14.0
* scikit-learn 0.15.0
* psychopy 1.80.06
* wxpython  2.8.12.1
* lxml 3.3.5
* pillow 2.5.0
* pyopengl 3.1.0
* pyglet 1.1.4
* pywin32 219
* emokit https://github.com/openyou/emokit/tree/master/python/emokit

Visual Studio 2008

Done:

- Install gevent with libev or libevent.
- Update example.py to see electrode reading instead of gyroscope readings.
- Perform FFT on one of the channels, plot result.
- Thesis skeleton: Introduction, contents, chapters, structure.
- Python application prototype which flashes screen with given frequency, read EPOC signal, performs FFT on each, averages and then you can compare if you can find the same frequency in the brain signal.
- Implement target identification with FFT (Fast Fourier Transform)
- Try all kinds of signal processing (filtering, windowing, linear detrending)
- Implement target identification with CCA (Canonical Correlation Analysis)
- Add linear interpolation to FFT method
- Make FFT and CCA method collaborate
- Have unexpectedly high target identification accuracy

TODO:

- Try to improve target identification time without significant loss in accuracy
- Write short summary of the thesis
- Start actually writing the thesis

Next general goals:

- Estimate how good it is for controlling a robot
- Try also c-VEP
- Try to control actual robot with it
