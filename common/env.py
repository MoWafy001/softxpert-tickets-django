import os


"""
This module provides a simple way to manage environment variables in Python.
It allows you to retrieve environment variables with optional default values,
and to enforce that certain environment variables must be set.
It also provides a method to convert the environment variable values to integers.
Usage:
    from env import Env

    # Get an environment variable with a default value
    db_host = Env.get("DB_HOST", "localhost").or_fail().to_str()
    
    # Get an environment variable and require it to be set
    db_port = Env.get("DB_PORT").required().to_int()

    # Get an environment variable and require it to be not empty
    db_user = Env.get("DB_USER").not_empty().to_str()
"""

class EnvValue:
    def __init__(self, key: str, strVal: str | None):
        """
        Initialize the EnvValue with a key and an optional default value.
        """
        self.strVal = strVal
        self.key = key
        self.required_enabled = False
        self.not_empty_enabled = False
    
    def __validate_constrains(self):
        """
        Validate the constraints set on the environment variable.
        Raise an error if the constraints are not met.
        """
        if self.required_enabled and self.strVal is None:
            raise ValueError(f"Environment variable {self.key} is required but not set.")
        if self.not_empty_enabled and (self.strVal is None or self.strVal == ""):
            raise ValueError(f"Environment variable {self.key} is not supposed to be empty.")

    def required(self):
        """
        Require the environment variable to be set. Raise an error if not set.
        """
        self.required_enabled = True
        return self

    def or_fail(self):
        """
        Alias for required() to indicate that the environment variable is required.
        """
        return self.required()

    def not_empty(self):
        """
        Require the environment variable to be not empty. Raise an error if empty.
        """
        self.not_empty_enabled = True
        return self

    def to_int(self) -> int:
        """
        Convert the string value to an integer.
        """
        self.__validate_constrains()

        # if the value is None, return None
        if self.strVal is None:
            return None;

        # check if the value is numeric
        if self.strVal.isnumeric():
            return int(self.strVal)
        else:
            raise ValueError(f"Environment variable {self.key} is not a valid integer.")

    def to_str(self) -> str:
        """
        Convert the string value to a string.
        """
        self.__validate_constrains()
        return self.strVal if self.strVal is not None else None

    def to_bool(self) -> bool:
        """
        Convert the string value to a boolean.
        """
        self.__validate_constrains()
        if self.strVal is not None:
            return self.strVal.lower() in ("true", "1", "yes")
        else:
            return False
    
    def to_float(self) -> float:
        """
        Convert the string value to a float.
        """
        self.__validate_constrains()

        # if the value is None, return None
        if self.strVal is None:
            return None;

        # check if the value is numeric
        if self.strVal.replace('.', '', 1).isdigit():
            return float(self.strVal)
        else:
            raise ValueError(f"Environment variable {self.key} is not a valid float.")

    def to_list(self, separator: str = ",") -> list:
        """
        Convert the string value to a list.
        """
        self.__validate_constrains()
        if self.strVal is not None:
            return [item.strip() for item in self.strVal.split(separator)]
        else:
            return []

    # magic methods to convert the object if needed
    def __str__(self):
        return self.to_str()
    def __int__(self):
        return self.to_int()
    def __float__(self):
        return self.to_float()
    def __bool__(self):
        return self.to_bool()
    def __list__(self):
        return self.to_list()
    def __repr__(self):
        return f"EnvValue(key={self.key}, strVal={self.strVal})"

class Env:
    @staticmethod
    def get(key: str, default: str = None) -> EnvValue:
        """
        Get the environment variable value or return the default value if not found.
        """
        return EnvValue(key, os.environ.get(key, default))