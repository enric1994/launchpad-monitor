# Launchpad Monitor

Reuse your Novation Launchpad to check your desk performance!

![Alt text](launchpad.jpg?raw=true)

## Information displayed
* RAM (green)
* SSD (amber)
* HDD(yellow)
* GPU usage (green)
* CPU core usage x8 (red)
* Temperature over 80 (yellow)

## Installation

1. Check your MIDI device name and add it to the outport:
`amidi -l`

2. Install the following packages:
`sudo apt-get install libjack0 libjack-dev libasound2-dev`

3. Install the following Python2.7 packages:
`sudo pip install rtmidi psutil mido python-rtmidi gpuinfo`

## More info

https://d2xhy469pqj8rc.cloudfront.net/sites/default/files/novation/downloads/4080/launchpad-programmers-reference.pdf