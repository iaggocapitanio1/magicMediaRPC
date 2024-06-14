import logging
import random
import time

import grpc
from grpc.experimental import gevent as grpc_gevent
from locust import task, between, events
import gevent
from services import vacancy_service_pb2
from services import vacancy_service_pb2_grpc, rpc_create_vacancy_pb2, rpc_update_vacancy_pb2
from utils.grpcUser import GrpcUser
from utils.users import User as UserData
from utils.utilitis import retrieve_credentials
from logging.handlers import RotatingFileHandler
grpc_gevent.init_gevent()
# Set up logging with file rotation
log_handler = RotatingFileHandler('locust.log', maxBytes=2 * 1024 * 1024, backupCount=5)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
grpc_host = "vacancies.cyrextech.net"
grpc_port = 7823
BACKGROUND_TASK_INTERVAL = 45
# Pre-defined users
users = [
    UserData(name='iaggo01', email='iaggocapitanio01@guerrillamail.info', password='password'),
    UserData(name='iaggo02', email='iaggocapitanio02@guerrillamail.info', password='password'),
    UserData(name='iaggo03', email='iaggocapitanio03@guerrillamail.info', password='password')
]


class VacancyUser(GrpcUser):
    wait_time = between(1, 2)
    stub_class = vacancy_service_pb2_grpc.VacancyServiceStub
    host = f"{grpc_host}:{grpc_port}"
    tokens = []

    def __init__(self, environment):
        super().__init__(environment)
        # Schedule the background task
        gevent.spawn_later(BACKGROUND_TASK_INTERVAL, self.run_background_tasks)

    def on_start(self):

        for user in users:
            try:
                user.sign_in()
                logger.info(f"User {user.email} signed up successfully.")
            except Exception as e:
                logger.error(f"Error signing up user {user.email}: {e}")
        for user in users:
            self.tokens.append(retrieve_credentials(user.email)[0])
        logger.info("Users signed up and tokens retrieved")

    @task
    def create_and_manage_vacancy(self):
        token = random.choice(self.tokens)

        try:
            # Create Vacancy
            create_request = rpc_create_vacancy_pb2.CreateVacancyRequest(
                Title=f"Engineer {random.randint(1, 1000)}",
                Description="Job description",
                Division=1,
                Country="USA"
            )
            create_response = self.stub.CreateVacancy(create_request, metadata=[('authorization', f'Bearer {token}')])
            logger.info(f"Created Vacancy: {create_response}")
            vacancy_id = create_response.vacancy.Id

            # Update Vacancy
            update_request = rpc_update_vacancy_pb2.UpdateVacancyRequest(
                Id=vacancy_id,
                Title=f"Senior Engineer {random.randint(1, 1000)}",
                Description="Updated job description",
                Views=random.randint(1, 1000),
            )
            update_response = self.stub.UpdateVacancy(update_request, metadata=[('authorization', f'Bearer {token}')])
            logger.info(f"Updated Vacancy: {update_response}")

            # Fetch Vacancy
            fetch_request = vacancy_service_pb2.VacancyRequest(Id=vacancy_id)
            fetch_response = self.stub.GetVacancy(fetch_request, metadata=[('authorization', f'Bearer {token}')])
            logger.info(f"Fetched Vacancy: {fetch_response}")

            # Delete Vacancy
            delete_request = vacancy_service_pb2.VacancyRequest(Id=vacancy_id)
            delete_response = self.stub.DeleteVacancy(delete_request, metadata=[('authorization', f'Bearer {token}')])
            logger.info(f"Deleted Vacancy: {delete_response}")
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {e.details()}")


    def fetch_all_vacancies(self):
        token = random.choice(self.tokens)

        try:
            # Fetch All Vacancies
            fetch_all_request = vacancy_service_pb2.GetVacanciesRequest(page=1, limit=100)
            fetch_all_response = self.stub.GetVacancies(fetch_all_request,
                                                        metadata=[('authorization', f'Bearer {token}')])
            logger.info(f"Fetched all vacancies: {fetch_all_response}")
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {e.details()}")

    def run_background_tasks(self):
        while True:
            self.fetch_all_vacancies()
            gevent.sleep(BACKGROUND_TASK_INTERVAL)

    def on_stop(self):
        self._channel.close()
