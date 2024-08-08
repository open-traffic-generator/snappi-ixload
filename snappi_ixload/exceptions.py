#import errors as err
import sys
import traceback
sys.path.insert(0, "c:\\Users\\waseebai\\Documents\\project\\snappi_l47\\snappi\\artifacts\\snappi")
import snappi

class Snappil47Exception(Exception): 
    def __init__(self, *args):
        super(Snappil47Exception, self).__init__(*args)
        self._args = args
        self._message = None
        self._status_code = None
        self._url = None
        self.process_exception()

    @property
    def args(self):
        return (
            self._status_code,
            (
                [self._message]
                if not isinstance(self._message, list)
                else self._message
            ),
            self._url
        )

    @property
    def message(self):
        return self._message.args[0]
    
    @property
    def url(self):
        return self._url

    @property
    def status_code(self):
        return self._status_code
    
    def process_exception(self):
        import pdb;pdb.set_trace()
        if isinstance(self._args[0].args, tuple) and len(self._args[0].args) == 1:
            if "Max retries exceeded" in str(self._args[0].args[0]):
                self._status_code= 500
                self._message = self._args[0]
                return (self._message, self._status_code)
            if isinstance(self._args[0].args[0], (str, list)):
                self._status_code = (
                    400 if self._status_code is None else self._status_code
                )
                self._message = self._args[0].args[0]
                return (self._message, self._status_code) 
            if isinstance(self._args[0], (NameError, TypeError, ValueError, KeyError, AttributeError)):
                self._status_code= 400
                self._message= self._args[0].args
                return (self._status_code, self._message)
            if isinstance(
                self._args[0], (ImportError, RuntimeError)
            ):
                self._status_code= 400
                self._message = self._args[0]
                return (self._status_code, self._message)
            else:
                self._status_code= 400
                self._message = self._args
                return (self._status_code, self._message)
        else:
            self._message = self._args
        return