#!/bin/bash

find $1 -name '*.png' | xargs -I % ./main %