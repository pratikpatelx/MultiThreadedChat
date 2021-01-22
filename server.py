#!usr/bin/python
import socket
from threading import Thread
from person import Person

HOST = "localhost"
PORT = 80
address = (HOST, PORT)

class Server(object):

    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.address = (self.host, self.port)
        self.clients = []
        self.server = None

    def start_broadcasting(self, msg, name):
        """
        This method broadcasts  new messages to all clients
        :param msg:
        :param name: the name of the client
        :type name: str
        :return:
        """
        for person in self.clients:
            client = person.client
            try:
                client.send(bytes(name, "utf8") + msg)
            except Exception as e:
                print("Failed to BroadCast message", e)

    def set_up_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(address)
            self.server.listen(5)
            print("Server Set-Up Successful")
            accept_thread = Thread(target=self.start_server)
            accept_thread.start()
            accept_thread.join()
        except socket.error as e:
            print("Error....Unable to Set Up Sockets with {0}".format(e.strerror))
            self.server.close()

    def client_handler(self, person):
        client = person.client
        # get client's name
        name = client.recv(512)
        name = name.decode("utf8")
        person.set_name(name)
        message = bytes("{0} has joined the chat!".format(name), "utf8")
        self.start_broadcasting(message, "")
        while True:
            try:
                message = client.recv(512)
                result = message.decode()
                print("Received Message....{0}".format(result))
                if result == "quit":
                    client.close()
                    self.clients.remove(person)
                    self.start_broadcasting(bytes("{0} has left the chat...".format(name), "utf8"), "")
                    print("Disconnected {0} from server".format(name))
                    break
                else:
                    self.start_broadcasting(message, name + ": ")
                    print("{0}: ".format(name), message.decode("utf8"))
            except Exception as e:
                print("Error...Failed to Broadcast Message", e)

    def start_server(self):
        while True:
            try:
                print("Waiting For a Request from server...")
                (requestSocket, clientAddr) = self.server.accept()
                person = Person(clientAddr, requestSocket)
                self.clients.append(person)
                print("Got a connection request from...{0}".format(clientAddr))
                Thread(target=self.client_handler, args=(person,)).start()
            except socket.error as e:
                print("Error... Failed to send a request to the client {0}".format(e.strerror))
                break


if __name__ == '__main__':
    server = Server()
    server.set_up_server()
