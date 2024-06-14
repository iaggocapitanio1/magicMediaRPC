def store_credentials(email: str, access_token: str, refresh_token: str):
    """
    Store access and refresh tokens for a given email in a file.
    """
    with open(f'{email}.txt', 'w') as file:
        file.write(f'access:{access_token}\nrefresh:{refresh_token}')


def retrieve_credentials(email: str) -> tuple:
    """
    Retrieve access and refresh tokens for a given email from a file.
    return: Tuple containing access and refresh tokens.
    example: ('access', 'refresh')
    """
    filename = f"{email}.txt"
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            access_token = lines[0].strip().split(':')[1]
            refresh_token = lines[1].strip().split(':')[1]
            return access_token, refresh_token
    except FileNotFoundError:
        print(f"No credentials found for {email}.")
        return None, None
    except IndexError:
        print("File format is incorrect.")
        return None, None
