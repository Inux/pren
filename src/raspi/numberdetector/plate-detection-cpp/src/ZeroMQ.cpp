//
// Created by patrick on 28.03.19.
//

#include "ZeroMQ.hpp"



ZeroMQ::ZeroMQ(socket_t socket) {
    socket.connect("tcp:://localhost:6666");
    localSocket = &socket;
}

void ZeroMQ::sendZerMQMessage(std::string message) {
    message_t m(5);
    memcpy(m.data(),"Hallo",5);
    localSocket->send(m);
}
