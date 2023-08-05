import tkinter as tk
import socket
import threading

# Replace 'YOUR_IP_ADDRESS' with the local IP address of the machine running the server
SERVER_IP = 'http://127.0.0.1:8000/'
SERVER_PORT = 5000

def receive_messages(client_socket, text_widget):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            text_widget.insert(tk.END, message + '\n')
        except OSError:
            break

def send_message(client_socket, message_entry):
    message = message_entry.get()
    client_socket.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    root = tk.Tk()
    root.title("Chat Client")

    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
    text_widget.config(state=tk.DISABLED)

    message_entry = tk.Entry(root)
    message_entry.pack(padx=10, pady=5, expand=True, fill=tk.BOTH)

    send_button = tk.Button(root, text="Send", command=lambda: send_message(client_socket, message_entry))
    send_button.pack(padx=10, pady=5)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, text_widget))
    receive_thread.start()

    root.mainloop()

    client_socket.close()

if __name__ == "__main__":
    start_client()
