# Written by Bram Cohen
# see LICENSE.txt for license information

from time import time
from cStringIO import StringIO
from sys import stdout
true = 1
false = 0

def kify(n):
    return str(long((n / (2 ** 10)) * 10) / 10.0)

class PublisherFeedback:
    def __init__(self, choker, add_task, port, ip, max_pause):
        self.choker = choker
        self.add_task = add_task
        self.port = port
        self.ip = ip
        self.max_pause = max_pause
        self.start = time()
        self.add_task(self.display, 1)

    def display(self):
        self.add_task(self.display, 1)
        t = time()
        s = StringIO()
        s.write('\n\n\n\n')
        for c in self.choker.connections:
            u = c.get_upload()
            if u.lastout < t - self.max_pause:
                u.update_rate(0)
            s.write('%15s ' % c.get_ip())
            if u.is_choked():
                s.write('c')
            else:
                s.write(' ')
            if u.is_interested():
                s.write('i')
            else:
                s.write(' ')
            s.write(' %6s\n' % kify(u.rate))
        s.write('\nat %s:%s' % (self.ip,str(self.port)))
        print s.getvalue()
        stdout.flush()
