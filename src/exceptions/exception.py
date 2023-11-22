def error_message_detail(error, error_detail):
    _, _, exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    lineno = exc_tb.tb_lineno
    error_message = "Error occured in script [{0}] at line number [{1}] with error message [{2}]".format(
        filename, lineno, error
    )
    return error_message


class SensorException(Exception):
    def __init__(self, error_message: str, error_detail) -> None:
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self) -> str:
        return self.error_message
