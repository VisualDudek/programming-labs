class EchoProcessor:
    def process_message(self, message: bytes) -> bytes:
        return message


class UpperCaseProcessor:
    def process_message(self, message: bytes) -> bytes:
        return message.upper()


class HardcodedConfig:
    def get_host(self) -> str:
        return "localhost"

    def get_port(self) -> int:
        return 8080
