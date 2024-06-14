from locust import User, task, between, events
import grpc
import services.auth_service_pb2_grpc as auth_service
import services.vacancy_service_pb2_grpc as vacancy_service
import services.rpc_signup_user_pb2 as rpc_signup_user
import services.rpc_signin_user_pb2 as rpc_signin_user
import services.rpc_create_vacancy_pb2 as rpc_create_vacancy
import services.rpc_update_vacancy_pb2 as rpc_update_vacancy
import random
import services.auth_service_pb2 as auth_service_defs
import services.auth_service_pb2_grpc as auth_service_grpc

# Global variable to hold user tokens
user_tokens = []


class VacancyUser(User):
    wait_time = between(1, 2)  # Time between tasks



    def on_start(self):
        # Simulate user sign-up, verification, and login
        self.signup_verify_and_login()


    @classmethod
    def login(cls, email, password):
        channel = grpc.insecure_channel('vacancies.cyrextech.net:7823')
        auth_stub = auth_service.AuthServiceStub(channel)
        signin_response = auth_stub.SignInUser(rpc_signin_user.SignInUserInput(
            email=email, password=password))

        return signin_response



    @task
    def create_and_manage_vacancy(self):
        if not user_tokens:
            return  # Skip this task if no users are logged in

        token = random.choice(user_tokens)  # Choose a token at random

        # Create and manage vacancies using the same channel
        channel = grpc.insecure_channel('vacancies.cyrextech.net:7823')
        create_stub = vacancy_service.VacancyServiceStub(channel)

        # Create a vacancy with the given token
        create_response = create_stub.CreateVacancy(rpc_create_vacancy.CreateVacancyRequest(
            Title="Engineer", Description="Job description", Division=1, Country="USA"),
            metadata=[('authorization', f'Bearer {token}')])

        # Further operations (update, get, delete) are performed as before
