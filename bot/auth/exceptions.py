class AuthError(Exception):
    pass


class TokenExpired(Exception):
    pass


UNAVAILABLE = "Service is unavailable, please try again later."
