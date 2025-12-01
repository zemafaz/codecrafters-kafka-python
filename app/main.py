import socket  # noqa: F401
from .request import Request, RequestHeaderV2

VALID_ERROR_CODE = 0
INVALID_API_VERSION_ERROR_CODE = 35


def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    connection, _ = server.accept()  # wait for client
    request_byte = connection.recv(1024)

    request = Request(request_byte, RequestHeaderV2)

    correlation_id = request.get_correlation_id()

    api_version = request.get_api_version()

    error_code = validate_api_version(api_version)

    response = parse_response(correlation_id, error_code)

    connection.sendall(response)
    connection.close()


def validate_api_version(api_version: bytes) -> bytes:
    return (
        VALID_ERROR_CODE.to_bytes(2)
        if b"0" <= api_version <= b"4"
        else INVALID_API_VERSION_ERROR_CODE.to_bytes(2)
    )


def parse_response(correlation_id: bytes, error_code: bytes) -> bytes:
    message_size = (len(correlation_id) + len(error_code)).to_bytes(4)

    return message_size + correlation_id + error_code


if __name__ == "__main__":
    main()
