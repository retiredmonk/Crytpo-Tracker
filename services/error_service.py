class APIResponseError(Exception):
    pass

class APIRateLimitedError(Exception):
    pass

class NetworkError(Exception):
    pass