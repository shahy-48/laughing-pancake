import sys

def error_message_detail(error, error_detail:sys):
    """Return error message with line number and file name."""
    _,_,exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error: {str(error)} at line {exc_tb.tb_lineno} in {filename}"
    return error_message

class CustomException(Exception):
    def __init__(self, error_message:str, error_detail:sys):
        # Get the error message with line number and file name
        self.error_message = error_message_detail(error_message, error_detail)
        # Call the parent class constructor
        super().__init__(self.error_message)
    def __str__(self) -> str:
        # Return the error message
        return self.error_message