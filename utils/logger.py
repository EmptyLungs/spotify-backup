import sys
import time


def log(str):
    sys.stdout.buffer.write(
        '[{}] {}\n'.format(time.strftime('%I:%M:%S'), str). \
            encode(sys.stdout.encoding, errors='replace'))
    sys.stdout.flush()
