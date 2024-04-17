#############
## Imports ##
#############

import secrets
import string

######################
## Helper Functions ##
######################


def create_short_key(length: int = 5) -> str:
    """
    Generate a random alphanumeric key of specified length.

    Args:
        length (int): The length of the key to generate. Defaults to 5.

    Returns:
        str: A randomly generated alphanumeric key.
    """

    # define characters to choose from
    chars = string.ascii_letters + string.digits
    # generate the random key
    random_key = "".join(secrets.choice(chars) for _ in range(length))
    return random_key
