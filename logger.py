import sys, os, signal
import time
from datetime import datetime

class _Logger:
    """ Overall class for logging events"""
    f = None
    
        

    def _write(self, text, level="5"):
        """Write a log event
            0 "Emergency"
            1 "Alert"
            2 "Critical"
            3 "Error"
            4 "Warning"
            5 "Notice"
            6 "Info"
            7 "Debug"
            8 "Trace"
        """
        if self.f is None:
            # lazily open log to get the app a chance to init
            self.f = self.open_log()

        if self.f is None:
            print(text)  # write to console if there is no file
        else:
            ts = self.get_ts()
            # print(ts)
            text = f"{ts} {level} {str(text)}\n"  # + " " + str(text) + "\n"

            try:
                self.f.write(text)
            except OSError as error:
                # reconnect to file
                self._handle_stale_file_error()

                # wait a second in case there is a network blip
                time.sleep(1)

                # try to write again. If we get another exception we want that to be thrown and to kill the job
                self.f.write(text)

            # also write to console
            print(text)

   
    def notice(self, text):
        self._write(text=text, level="5")

    def info(self, text):
        self._write(text=text, level="6")

    def debug(self, text):
        self._write(text=text, level="7")

    def error(self, text):
        self._write(text=text, level="3")

    def warning(self, text):
        self._write(text=text, level="4")

    
