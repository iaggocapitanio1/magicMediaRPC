import random
import grpc
import logging
from locust import User, task, between
from services import vacancy_service_pb2
from services import vacancy_service_pb2_grpc, rpc_create_vacancy_pb2, rpc_update_vacancy_pb2
from utils.users import User as UserData
from utils.utilitis import retrieve_credentials

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

grpc_host = "vacancies.cyrextech.net"
grpc_port = 7823

# Pre-defined users
users = [
    UserData(name='iaggo01', email='iaggocapitanio01@guerrillamail.info', password='password'),
    UserData(name='iaggo02', email='iaggocapitanio02@guerrillamail.info', password='password'),
    UserData(name='iaggo03', email='iaggocapitanio03@guerrillamail.info', password='password')
]

class VacancyUser(User):
    wait_time = between(1, 2)
    tokens = []

    def on_start(self):
        for user in users:
            try:
                user.sign_up()
                logger.info(f"User {user.email} signed up successfully.")
            except Exception as e:
                logger.error(f"Error signing up user {user.email}: {e}")
        for user in users:
            self.tokens.append(retrieve_credentials(user.email)[0])
        logger.info("Users signed up and tokens retrieved")

    @task
    def create_and_manage_vacancy(self):
        token = random.choice(self.tokens)
        channel = grpc.insecure_channel(f"{grpc_host}:{grpc_port}")
        stub = vacancy_service_pb2_grpc.VacancyServiceStub(channel)

        try:
            # Create Vacancy
            create_request = rpc_create_vacancy_pb2.CreateVacancyRequest(
                Title=f"Engineer {random.randint(1, 1000)}",
                Description="Job description",
                Division=1,
                Country="USA"
            )
            create_response = stub.CreateVacancy(create_request, metadata=[('authorization', f'Bearer {token}')])
            logger.info(f"Created Vacancy: {create_response}")
            vacancy_id = create_response.vacancy.Id

            # Update Vacancy
            update_request = rpc_update_vacancy_pb2.UpdateVacancyRequest(
                Id=vacancy_id,
                Title=f"Senior Engineer {random.randint(1, 1000)}",
                Description="Updated job description",
                Views=random.randint(1, 1000),
            )
            update_response = stub.UpdateVacancy(update_request, metadata=[('authorization', f'Bearer {token}')])
            logger.info(f"Updated Vacancy: {update_response}")

            # Fetch Vacancy
            fetch_request = vacancy_service_pb2.VacancyRequest(Id=vacancy_id)
            fetch_response = stub.GetVacancy(fetch_request, metadata=[('authorization', f'Bearer {token}')])
            logger.info(f"Fetched Vacancy: {fetch_response}")

            # Delete Vacancy
            delete_request = vacancy_service_pb2.VacancyRequest(Id=vacancy_id)
            delete_response = stub.DeleteVacancy(delete_request, metadata=[('authorization', f'Bearer {token}')])
            logger.info(f"Deleted Vacancy: {delete_response}")
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {e.details()}")
        finally:
            channel.close()

    @task
    def fetch_all_vacancies(self):
        token = random.choice(self.tokens)
        channel = grpc.insecure_channel(f"{grpc_host}:{grpc_port}")
        stub = vacancy_service_pb2_grpc.VacancyServiceStub(channel)

        try:
            # Fetch All Vacancies
            fetch_all_request = vacancy_service_pb2.GetVacanciesRequest(page=1, limit=100)
            fetch_all_response = stub.GetVacancies(fetch_all_request, metadata=[('authorization', f'Bearer {token}')])
            logger.info(f"Fetched all vacancies: {fetch_all_response}")
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {e.details()}")
        finally:
            channel.close()

    def on_stop(self):
        # Clean up if necessary when the user stops
        pass

# To run this locust script, execute `locust` in your terminal with this file.
# e.g., `locust -f locustfile.py
