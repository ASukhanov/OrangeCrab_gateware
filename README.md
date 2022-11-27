# OrangeCrab_gateware
Unofficial gateware projects for OrangeCrab development board.

## Prerequisites
OSS Cad Suite. (https://github.com/YosysHQ/oss-cad-suite-build).

Virtual environment: 

    source <extracted_location>/oss-cad-suite/environment

# Finished

- amaranth/blink.py: Simplest gateware. Blink the three LEDs in a counting pattern.

# Work in progress

## amaranth/blink_reset.py
usage: blink_reset.py [-h] [-g]

Blink the three LEDs in a counting pattern. Reset the OrangeCrab on button
press. It is amaranth implementation of a verilog project blink_reset at:
https://github.com/orangecrab-fpga/orangecrab-examples/tree/main/verilog

optional arguments:
  -h, --help  show this help message and exit
  -g, --gen   Generate gateware, simulate otherwise

To view simulated traces:
    gtkwave test.vcd

![waveform blink_reset-v002](/Waveforms/blink_reset-v002.png)
