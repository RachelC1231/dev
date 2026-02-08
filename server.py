import socket

HOST = "0.0.0.0"  # 主机外面都可以访问, 127.0.0.1 只能自己访问的ip
PORT = 9000 #端口

# 1. 创建 socket（IPv4 + TCP）
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 绑定地址
server_socket.bind((HOST, PORT))

# 3. 开始监听
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

while True:
    # 4. 接受客户端连接
    client_socket, client_addr = server_socket.accept()
    print(f"Client connected: {client_addr}")

    try:
        # 5. 接收数据
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("break")
                break

            message = data.decode("utf-8")
            print("Received:", message)

            # 6. 回复数据
            response = f"Server: {message}"
            client_socket.send(response.encode("utf-8"))

    finally:
        client_socket.close()
        # 7. 关闭连接
        print("...")
        