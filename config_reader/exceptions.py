class ConfigTypeError(TypeError):
    def __init__(self, key, value, expected):
        fmt_dict = {"key": key, "type": type(value), "value": value, "expected": expected}
        msg = "Invalid type {type} of value {value} for configuration key {key}, expected {expected}".format(**fmt_dict)
        super(ConfigTypeError, self).__init__(msg)


class ConfigTypeCastError(TypeError):
    def __init__(self, key, value, expected):
        fmt_dict = {"key": key, "value": value, "expected": expected}
        msg = "Cannot cast value {value} of configuration key {key} to {expected}".format(**fmt_dict)
        super(ConfigTypeCastError, self).__init__(msg)


class ConfigKeyNotFoundError(KeyError):
    def __init__(self, key):
        msg = "Configuration key {key} was not found.".format(key=key)
        super(ConfigKeyNotFoundError, self).__init__(msg)


class ConfigParseError(ValueError):
    def __init__(self, filename, error):
        fmt_dict = {'filename': filename, 'error': error}
        msg = "ConfigReader could not parse file '{filename}':\n{error}".format(**fmt_dict)
        super(ConfigParseError, self).__init__(msg)
