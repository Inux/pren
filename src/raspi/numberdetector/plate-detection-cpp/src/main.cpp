#include <iostream>
#include "PlateDetec.hpp"
#include "numberReco.pb.h"
#include <zmq.hpp>
#include <unistd.h>

int main(int argc, char *argv[]) {
    PlateDetec plateDetec;
    plateDetec.enableWindow();
    plateDetec.showImage();

}