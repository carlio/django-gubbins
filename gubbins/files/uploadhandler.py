
import time
from django.core.files.uploadhandler import FileUploadHandler

class SlowFileUploadHandler(FileUploadHandler):
    """
    This is an implementation of the Django file upload handler which will
    sleep between processing chunks in order to simulate a slow upload. This
    is intended for development when creating features such as an AJAXy
    file upload progress bar, as uploading to a local process is often too
    quick.
    """
    def receive_data_chunk(self, raw_data, start):
        time.sleep(2);
        return raw_data
    
    def file_complete(self, file_size):
        return None
