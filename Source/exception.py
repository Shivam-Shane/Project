import sys,os
import inspect


def error_message_details(error, error_detail):
    _, _, exc_tb = error_detail
    filename = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in {filename}, line {line_number}: {error}"
    return error_message                                                                 


class CustomException(Exception):
    def __init__(self, error_message, exc_info):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, exc_info)

    def __str__(self):
        return "Error Message: {}".format(self.error_message)


