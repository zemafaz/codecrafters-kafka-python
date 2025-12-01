import socket  # noqa: F401

MESSAGE_SIZE_SIZE = 4
REQ_API_KEY_SIZE = 2
REQ_API_VERSION_SIZE = 2
REQ_CORRELATION_ID_SIZE = 4


def parse_response(correlation_id: bytes) -> bytes:
    message_size = bytes(len(correlation_id))

    return message_size + correlation_id


def parse_correlation_id(request: bytes) -> bytes:
    start = MESSAGE_SIZE_SIZE + REQ_API_KEY_SIZE + REQ_API_VERSION_SIZE
    end = start + REQ_CORRELATION_ID_SIZE
    return request[start:end]


def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    connection, _ = server.accept()  # wait for client
    request = connection.recv(1024)

    correlation_id = parse_correlation_id(request)

    response = parse_response(correlation_id)
    connection.sendall(response)
    connection.close()


if __name__ == "__main__":
    main()
