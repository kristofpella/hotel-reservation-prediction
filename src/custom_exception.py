import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message: str, error_detail: Exception):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message: str, error_detail: Exception):
        try:
            # Get the traceback from the exception
            exc_type, exc_obj, exc_tb = sys.exc_info()
            if exc_tb is None:
                # If no traceback in sys.exc_info(), try to get it from the exception
                tb = error_detail.__traceback__
                if tb is not None:
                    file_name = tb.tb_frame.f_code.co_filename
                    line_number = tb.tb_lineno
                else:
                    # Fallback if no traceback available
                    return f"Error: {error_message}"
            else:
                file_name = exc_tb.tb_frame.f_code.co_filename
                line_number = exc_tb.tb_lineno
            
            return f"Error in {file_name} at line number {line_number} error message: {error_message}"
        except Exception:
            # Fallback if traceback extraction fails
            return f"Error: {error_message}"
    
    def __str__(self):
        return self.error_message
