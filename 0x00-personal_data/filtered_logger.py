#!/usr/bin/env python3
"""
This module contains the function filter_datum which returns the log message
obfuscated
"""
import re
import logging
from typing import List, Tuple


PII_FIELDS: Tuple = ("email", "ssn", "password", "ip", "phone")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated

    Args:
        fields (List[str]): fields to obfuscate
        redaction (str): string to replace the field
        message (str): log to obfuscate
        separator (str): separator of fields

    Returns:
        str: log obfuscated
    """
    for field in fields:
        message = re.sub(r"{}=[^{}]+".format(field, separator),
                         r"{}={}".format(field, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filter values in incoming log records using filter_datum.
        """
        if not record:
            return ""

        record.msg = filter_datum(self.fields,
                                  self.REDACTION,
                                  record.msg,
                                  self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object
    """
    logger_obj: logging.Logger = logging.getLogger(name="user_data")
    logger_obj.setLevel(logging.INFO)
    logger_obj.propagate = False
    # formatter: RedactingFormatter = RedactingFormatter(list(PII_FIELDS))
    handler: logging.StreamHandler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger_obj.addHandler(handler)
    return logger_obj
