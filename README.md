# The Producer/Consumer Problem

This is my solution to the classic Producer/Consumer problem, written in Python. I've found other solutions out there, but they don't tackle the problem in a clear way. Rather than using Python's built-in semaphores, I've created my own simple boolean ones. I've also created my own buffer from scratch, forcing a list to become a circular queue.

Enjoy!

## Usage

`python pc.py <num_producers> <num_producers> [<buffer_size>]`

## TODO

Implement a keystroke to gracefully stop the loop and exit the program..