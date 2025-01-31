# Redis-Inspired-In-Memory-Key-Value-Store-

# How to run the code:

g++ -std=c++11 -pthread -o redis_server server.cpp avl.cpp hashtable.cpp heap.cpp thread_pool.cpp zset.cpp

./redis_server

# Test the server using the Python script (recommended):
python redis_test.py

# Note: Direct connection with nc is not supported due to binary protocol requirements instead use the python script


### Testing
./redis_cli.py


# Commands:
set key value
get key
del key
