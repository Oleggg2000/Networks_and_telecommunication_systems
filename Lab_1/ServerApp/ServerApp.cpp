#include "pch.h"
#include <iostream>
#pragma comment(lib, "ws2_32.lib")
#include <WinSock2.h>
#pragma warning(disable:4996)

using namespace std;
void Client_Handler(int index);

SOCKET Connections[10]; //sockets for clients
int Counter = 0; //counter of clients

int main()
{
	///Library Initialization///
	WSAData WSA_Data; //init wsock32.dll
	//WORD DLL_Version = MAKEWORD(2, 1); //get version wsock32.dll
	if (WSAStartup(0x0101, &WSA_Data) != 0) {
		cout << "Error, can't initialize WinSock: " << WSAGetLastError() << endl;
		return 1;
	}

	///Creating IP address///
	SOCKADDR_IN address;//struct for saving IP address 
	int sizeof_address = sizeof(address);//can't use sizeof(address) directly into accept(*,*,&sizeof(address)) in 4th block of code
	address.sin_addr.s_addr = inet_addr("127.0.0.1");; //IP address
	//gethostbyname(const char *name) this function gets all information about host: name, IP, etc 
	address.sin_port = htons(1337); //port of node, transfer from short int to network byte order
	address.sin_family = AF_INET; //family of protocols (AF_INET - Internet protocol)

	///Creating, listening and binding socket with IP address///
	SOCKET socket_Listen = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); //created socket for listening
	bind(socket_Listen, (SOCKADDR*)&address, sizeof(address)); //bind IP address to socket
	listen(socket_Listen, SOMAXCONN); //maximum number of socket's requests

	///Socket for connection server to client///
	SOCKET new_Connection;//socket for new client
	for (int i = 0; i < 10; i++) {
		new_Connection = accept(socket_Listen, (SOCKADDR*)&address, &sizeof_address);//setting connection with client
		if (new_Connection == INVALID_SOCKET) {
			cout << "Error, client can't connect to server: " << WSAGetLastError() << endl;
			return 1;
		}
		else {
			cout << "Client successful connection!" << endl;
			char str[256]="Welcome to my server, user!";
			send(new_Connection, str, sizeof(str), NULL);

			Connections[i] = new_Connection;
			Counter++;
			CreateThread(NULL, NULL, (LPTHREAD_START_ROUTINE)Client_Handler, (LPVOID)i, NULL, NULL);
		}
	}


	system("pause");
	closesocket(new_Connection);
	closesocket(socket_Listen);
	return 0;
}

void Client_Handler(int index) { //Client handler (for reading and sending messages to other clients)
	char str[256];
	while (true) {
		recv(Connections[index], str, sizeof(str), NULL);//receive message
		for (int i = 0; i < Counter; i++) { 
			if (i == index) continue;
			send(Connections[i], str, sizeof(str), NULL);
		}
	}
}
