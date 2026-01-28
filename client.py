# 底层 TCP 客户端
import socket

SERVER_HOST = "192.168.12.14"   # 服务器IP
SERVER_PORT = 9000          # 服务器端口

def tcp_client():
    # 创建 TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 建立连接
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to server")

        while True:
            # 发送数据
            message = input("Send to server: ")
            if message.lower() == "exit":
                break

            client_socket.sendall(message.encode("utf-8"))

            # 接收数据
            data = client_socket.recv(1024)
            print("Received:", data.decode("utf-8"))

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()
        print("Connection closed")


if __name__ == "__main__":
    tcp_client()

