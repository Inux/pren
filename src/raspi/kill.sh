#Kill Raspi Applications

#find all applications by ports (defined in server.py and zmq_socket.py)
lsof -t -i :2828 | xargs kill -9
lsof -t -i :28281 | xargs kill -9
lsof -t -i :28282 | xargs kill -9
lsof -t -i :28283 | xargs kill -9
lsof -t -i :28284 | xargs kill -9
lsof -t -i :28285 | xargs kill -9
lsof -t -i :28286 | xargs kill -9
