
# gr-receive muter
This oot module contains two blocks that can be used to mute a receive chan while the transmitter is transmitting. The muting is done based on signal level detection.
This allows full duplex devices, such as Ettus USRP devices to be operated in simplex, and avoid feedback from the transmitter into the receiver side signal processing.

To gain the best results, pre- and post- pad the transmits with low power white noise.

The mute function can either attenuate, replace with white noise or replace with zeros.


## Installation
```bash
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
```


## Running the example
Start `receive_mute_example`. Then run `send_test_sig.py` to inject a signal.

