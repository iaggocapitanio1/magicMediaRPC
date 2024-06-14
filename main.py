# 1. Create 3 users on the server (SignUpUser)
# 2. Verify the email of the users (VerifyEmail)
# 3. Store the credentials somewhere for later use


# To accomplish this, I use the gRPC client to interact with the server and create the users. Subsequently, we need
# a method to receive the verification codes. For this, we will utilize a temporary email service to receive the emails
# and extract the verification codes from them.

# User 1
# Name: iaggo01
# Email: iaggocapitanio01@guerrillamail.info
# Password: password

# User 2
# Name: iaggo02
# Email: iaggocapitanio02@guerrillamail.info
# Password: password

# User 3
# Name: iaggo03
# Email: iaggocapitanio03@guerrillamail.info
# Password: password

from utils.users import User

users = [User(name='iaggo01', email='iaggocapitanio01@guerrillamail.info', password='password'),
         User(name='iaggo02', email='iaggocapitanio02@guerrillamail.info', password='password'),
         User(name='iaggo03', email='iaggocapitanio03@guerrillamail.info', password='password')]

verify_codes = [
    'STfoAOPKIIpu0Pz2Oy2P',
    'iF7PFfpdg28BNr61OaTL',
    'JkVOMfDeNubinWXxrof3',

]


def create_users():
    for user in users:
        user.sign_up()


def verify_emails():
    for user, code in zip(users, verify_codes):
        user.verify_email(code)


def sign_in():
    for user in users:
        user.sign_in()


if __name__ == '__main__':
    # create_users()
    # verify_emails()
    sign_in()
