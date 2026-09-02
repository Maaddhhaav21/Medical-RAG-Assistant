import sys

class CustomException(Exception):
    """Custom exception with file and line information."""

    def __init__(self, message: str, error_detail=None):
        super().__init__(message)

        self.message = message
        self.error_detail = error_detail

        _, _, exc_tb = sys.exc_info()

        if exc_tb:
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.line_number = exc_tb.tb_lineno
        else:
            self.file_name = "Unknown"
            self.line_number = "Unknown"

    def __str__(self):
        if self.error_detail:
            return (
                f"{self.message} | "
                f"Error: {self.error_detail} | "
                f"File: {self.file_name} | "
                f"Line: {self.line_number}"
            )

        return (
            f"{self.message} | "
            f"File: {self.file_name} | "
            f"Line: {self.line_number}"
        )