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
KEYS                    # List all keys in database
GET key                 # Get value of key
SET key value          # Set key to value
DEL key 

# TTL Commands:
PEXPIRE key ms         # Set key to expire in milliseconds
PTTL key               # Get remaining time to live in milliseconds

# ZSET Commands:
ZADD leaderboard 100 "player1"    # Add player1 with score 100
ZADD leaderboard 200 "player2"    # Add player2 with score 200
ZSCORE leaderboard "player1"      # Get player1's score (returns 100)
ZREM leaderboard "player1"        # Remove player1
ZQUERY leaderboard 0 "" 0 10       # Get top 10 players