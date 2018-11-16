#Kill Raspi Applications

#webapp (find port 2828 and kill process...)
lsof -t -i :2828 | xargs kill -9