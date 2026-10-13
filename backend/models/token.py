from dataclasses import dataclass

@dataclass
class TokenSession():
    access_token: str
    token_type: str
    username: str