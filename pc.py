# Seth Wilson
# COSC 5330
# Assignment #2
# Consumer/Producer Problem

# import needed modules.
import sys, time, random, threading

# create a class that contains the boolean semaphores.
class Semaphores:

    def __init__(self):

        self.item_available = False
        self.space_available = True
        self.buffer_available = True

# Instantiate a new semaphores object.
semaphores = Semaphores()

# create a circular buffer class.
class Buffer:

    def __init__(self, buffer_size):
        """Initialize buffer values."""
        self.queue = list()
        self.head = 0
        self.tail = 0
        self.size = 0
        self.max_size = buffer_size

    def enqueue(self):
        """Add a 1 to the buffer."""

        # Add a 1 to the existing index. If index doesn't exist, create it.
        try:
            self.queue[self.tail] = 1
        except IndexError:
            self.queue.append(1)

        # Make the buffer circular by using modulo division.
        self.tail = (self.tail + 1) % self.max_size

        # Increment the buffer size.
        self.size = self.size + 1

        # If buffer is full, toggle the buffer_available semaphore.
        if self.size == self.max_size:
            semaphores.buffer_available = False

    def dequeue(self):
        """Overwrite the head of the queue with 0, effectively dequeuing."""
        self.queue[self.head] = 0

        # Move the head of the queue up, circularly.
        self.head = (self.head + 1) % self.max_size

        # Once you dequeue items, the buffer is available again.
        semaphores.buffer_available = True

        # Decrement the buffer size.
        self.size = self.size - 1

    def show(self):
        """Display the buffer's contents, with no spaces."""
        return ''.join(str(i) for i in self.queue)

# Specify an optional buffer size as third command line argument.
try:
    buff_size = int(sys.argv[3])
# Otherwise buffer size defaults to 80.
except IndexError:
    buff_size = 80

# Instantiate a new buffer object.
buffer = Buffer(buff_size)

# Producer class.
class Producer(threading.Thread):
    def __init__(self, num_items):
        """Initialize the Producer thread."""
        super(Producer,self).__init__()

        # Set number of items to produce based on input.
        self.num_items = num_items

    def run(self):
        """Loop to run the thread."""
        while True:

            # Only produce if buffer and space semaphores are clear.
            if semaphores.buffer_available and semaphores.space_available:

                # Also make sure there's room in the buffer.
                if (buffer.max_size - buffer.size) >= self.num_items:

                    # Lock the item available semaphore.
                    semaphores.item_available = False

                    # Produce m number of items.
                    for m in range(self.num_items):
                        buffer.enqueue()
                    
                    # Release the item available semaphore.
                    semaphores.item_available = True

                    # Print the buffer.
                    print("Producer: {}".format(buffer.show()))

                    # Sleep for random amount of time to simulate real app.
                    time.sleep(random.random())
        return

# Consumer class
class Consumer(threading.Thread):
    def __init__(self, num_items):
        """Initialize the Consumer thread."""
        super(Consumer,self).__init__()

        # Set number of items to consume based on input.
        self.num_items = num_items

    def run(self):
        """Loop to run the thread."""
        while True:

            # Only consume if there are items available.
            if semaphores.item_available:

                # Make sure there are enough items in the buffer to consume.
                if buffer.size >= self.num_items:

                    # Lock the space available semaphore.
                    semaphores.space_available = False

                    # Consume n number of items.
                    for n in range(self.num_items):
                        buffer.dequeue()

                    # Release the space available semaphore.
                    semaphores.space_available = True

                    # Print the buffer.
                    print("Consumer: {}".format(buffer.show()))

                    # Sleep for random amount of time to simulate real app.
                    time.sleep(random.random())
        return

# Initialize m and n variables from command line arguments.
m = int(sys.argv[1])
n = int(sys.argv[2])

# Instantiate producer and consumer objects with command line arguments.
p = Producer(m)
c = Consumer(n)

# Start the consumer.
c.start()

# Wait two seconds and start the producer.
time.sleep(2)
p.start()