from .adapters.stability_service import Stability
# from pydantic import BaseSettings


# class AuthConfig(BaseSettings):
#     API_KEY: str


# config = AuthConfig()


class Service:
    def __init__(self):
        self.stability = Stability("sk-nd1utdFyof200NOw567li1JLptzQ1vMcdXlLGPllHEhfWrL2")

def get_service():
    svc = Service()
    return svc
