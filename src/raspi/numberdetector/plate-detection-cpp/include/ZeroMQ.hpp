//
// Created by patrick on 28.03.19.
//

#ifndef PLATEDETECTION_ZEROMQ_HPP
#define PLATEDETECTION_ZEROMQ_HPP

#include <zmq.hpp>
#include <string>
#include <iostream>
#include <unistd.h>
#include "numberReco.pb.h"

using namespace zmq;


class ZeroMQ {

public:

    ZeroMQ(socket_t socket);

    void sendZerMQMessage(std::string message);


private:
    socket_t *localSocket;



};


#endif //PLATEDETECTION_ZEROMQ_HPP
