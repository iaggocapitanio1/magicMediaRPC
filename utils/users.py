import grpc
from services import auth_service_pb2_grpc, rpc_signup_user_pb2, auth_service_pb2_grpc, auth_service_pb2, rpc_signin_user_pb2
from utils.utilitis import store_credentials

class User:
    def __init__(self, name, email, password):
        self._name = name
        self._email = email
        self._password = password

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @staticmethod
    def _create_channel():
        """
        Create a gRPC channel to connect to the authentication service.
        """
        return grpc.insecure_channel('vacancies.cyrextech.net:7823')

    def sign_up(self):
        """
        Sign up a user in the CyrexTech server.
        """
        # Create a gRPC channel
        print("Creating a gRPC channel.")
        channel = self._create_channel()

        try:
            # Create a stub (client)
            auth_stub = auth_service_pb2_grpc.AuthServiceStub(channel)

            # Create a sign-up request
            signup_request = rpc_signup_user_pb2.SignUpUserInput(
                name=self.name,
                email=self.email,
                password=self.password,
                passwordConfirm=self.password  # Assuming you need to confirm the password
            )

            # Send the sign-up request
            signup_response = auth_stub.SignUpUser(signup_request)

            # Process the response
            if signup_response:
                print("Sign-up successful!")
            else:
                print("Sign-up failed:", signup_response.error)

            return signup_response

        except grpc.RpcError as e:

            if e.code() == grpc.StatusCode.UNAVAILABLE:
                print("The server is unavailable.")
            else:
                e.code() == grpc.StatusCode.ALREADY_EXISTS
                print("The user already exists.")


        finally:
            print("Closing the gRPC channel.")
            channel.close()

    def verify_email(self, verification_code):
        """
        Verify the user's email address.
        """
        channel = grpc.insecure_channel('vacancies.cyrextech.net:7823')
        auth_stub = auth_service_pb2_grpc.AuthServiceStub(channel)

        # Use the correct module to create the VerifyEmailRequest
        try:
            verification_response = auth_stub.VerifyEmail(auth_service_pb2.VerifyEmailRequest(
                verificationCode=verification_code))
            print("Email verification successful!")
            return verification_response
        except grpc.RpcError as e:
            print("Error verifying email:", e.details())
        finally:
            print("Closing the gRPC channel.")
            channel.close()

    def sign_in(self):
        """
        Authenticate a user by signing them in to the CyrexTech server.
        """
        channel = self._create_channel()
        try:
            auth_stub = auth_service_pb2_grpc.AuthServiceStub(channel)
            signin_request = rpc_signin_user_pb2.SignInUserInput(
                email=self.email,
                password=self.password
            )
            signin_response = auth_stub.SignInUser(signin_request)
            if signin_response:
                print("Sign-in successful!")
                print(signin_response)
                store_credentials(email=self.email, access_token=signin_response.access_token, refresh_token=signin_response.refresh_token)
            else:
                print("Sign-in failed:", signin_response.error)
            return signin_response
        except grpc.RpcError as e:
            print(f"RPC Error: {e.details()} Code: {e.code()}")
        finally:
            channel.close()

