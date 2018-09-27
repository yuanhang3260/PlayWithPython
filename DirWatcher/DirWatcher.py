import datetime
import sys
import subprocess
import threading
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher(object):
  def __init__(self, directory):
    self.dir_to_watch = directory
    print "monitoring " + self.dir_to_watch
    self.observer = Observer()

  def run(self):
    self.observer.schedule(Handler(), self.dir_to_watch, recursive=False)
    self.observer.start()
    try:
      while True:
        time.sleep(100)
    except:
      self.observer.stop()
      print "Error"

    self.observer.join()


command = ""

class Handler(FileSystemEventHandler):
  @staticmethod
  def on_any_event(event):
    if event.is_directory:
      return
    elif event.event_type == 'modified':
      out = Command(command).run()
      if out:
        print "[" + str(datetime.datetime.now()) + "] " + command + ":"
        for line in out:
          print line


class Command(object):
  def __init__(self, cmd):
    self.cmd = cmd
    self.process = None
    self.out = None

  def run_command(self, capture=True):
    if not capture:
      self.process = subprocess.Popen(self.cmd, shell=True)
      self.process.communicate()
      return

    # capturing the outputs of shell commands
    self.process = subprocess.Popen(self.cmd, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
    out, err = self.process.communicate()
    if len(out) > 0:
      self.out = out.splitlines()
    else:
      self.out = None

  # set default timeout to 10s.
  def run(self, capture=True, timeout=10):
    thread = threading.Thread(target=self.run_command, args=(capture,))
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
      print 'Command timeout, kill it: ' + self.cmd
      self.process.terminate()
      thread.join()

    return self.out


if __name__ == '__main__':
  if len(sys.argv) != 3:
    print "Usage: python DirWatcher.py [directory] cmd"
    sys.exit(-1)

  command = sys.argv[2]

  w = Watcher(sys.argv[1])
  w.run()

