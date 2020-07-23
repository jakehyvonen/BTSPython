# BTSPython

A collection of Python code for usage with a custom LED Batch Test System (BTS).

The file ActiveDevBatchControl.py is set to run whenever the Raspberry Pi is booted. It interacts with a Marlin CNC controller and solenoid actuators to move LED samples into and out of a test socket. It receives commands and sends image files via TCP.
