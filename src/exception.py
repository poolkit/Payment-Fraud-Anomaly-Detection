import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    error_message = f"Script: [{exc_tb.tb_frame.f_code.co_filename}], Line: [{exc_tb.tb_lineno}], Message: [{str(error)}]"
    return error_message
    
class CustomException(Exception):
    def __init__(self,error_message,error_detail=sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
    
if __name__=="__main__":
    try:
        x = 5/0
    except Exception as e:
        logging.error(CustomException(e))
        raise e