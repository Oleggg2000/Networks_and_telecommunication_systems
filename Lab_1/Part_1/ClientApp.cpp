#include "pch.h"
#include <iostream>
#pragma comment(lib, "ws2_32.lib")
#include <WinSock2.h>
#pragma warning(disable:4996)

using namespace std;
void Get_message_from_server();
SOCKET Connection;

int main()
{
	///Library Initialization///
	WSAData WSA_Data; 
	//WORD DLL_Version = MAKEWORD(2, 1); //get version wsock32.dll
	if (WSAStartup(0x0101, &WSA_Data) != 0) {
		cout << "Error, can't initialize WinSock: " << GetLastError() << endl;
		return 1;
	}

	///Creating IP address///
	SOCKADDR_IN address;
	int sizeof_address = sizeof(address);
	address.sin_addr.s_addr = inet_addr("127.0.0.1");
	//gethostbyname(const char *name) this function gets all information about host: name, IP, etc 
	address.sin_port = htons(1337);
	address.sin_family = AF_INET;

	///Creating, listening and binding socket with IP address///
	SOCKET socket_Listen = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	bind(socket_Listen, (SOCKADDR*)&address, sizeof(address));
	listen(socket_Listen, SOMAXCONN);

	///Connection to the server///
	Connection= socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (connect(Connection, (SOCKADDR*)&address, sizeof(address)) != 0) {
		cout << "Error, can't be connected to server: " << WSAGetLastError() << endl;
		return 1;
	}
	else cout << "Connected!!" << endl;
	
	///Sending and getting user's messages///
	char msg[256];
	CreateThread(NULL, NULL, (LPTHREAD_START_ROUTINE)Get_message_from_server, NULL, NULL, NULL);
	while (true) { //Endless cycle
		cin.getline(msg, sizeof(msg));
		send(Connection, msg, sizeof(msg), NULL);
	}

	system("pause");
	closesocket(Connection);
	closesocket(socket_Listen);
	return 0;
}

void Get_message_from_server() { //Stream for getting messages from the server
	char str[256];
	while (true) { //Endless cycle
		recv(Connection, str, sizeof(str), NULL);
		cout << str << endl;
	}
}