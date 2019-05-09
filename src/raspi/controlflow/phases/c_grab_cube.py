import time

count = 0
limit = 5

def method(middleware_data):
    global count
    if count < limit:
        count = count + 1
        time.sleep(1)
        return "'" + str(count) + "' < '" + str(limit) + "'"

    count = 0
    return ""
