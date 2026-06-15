from dataclasses import dataclass


@dataclass
class Tenant:
    name: str        # 사용자 지정 표시명
    host: str        # https://xxxxx.cfapps.hana.ondemand.com
    clientid: str
    clientsecret: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "host": self.host,
            "clientid": self.clientid,
            "clientsecret": self.clientsecret,
        }

    @staticmethod
    def from_dict(data: dict) -> "Tenant":
        return Tenant(
            name=data["name"],
            host=data["host"].rstrip("/"),
            clientid=data["clientid"],
            clientsecret=data["clientsecret"],
        )
