# Redis-Inspired-In-Memory-Key-Value-Store-

# How to run the code:

g++ -std=c++11 -pthread -o redis_server server.cpp avl.cpp hashtable.cpp heap.cpp thread_pool.cpp zset.cpp

./redis_server

# connect to server
nc localhost 1234
set key value
get key
del key

# Or use py test script
python redis_test.py