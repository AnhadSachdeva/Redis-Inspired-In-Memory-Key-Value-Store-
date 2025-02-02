# Redis-Inspired In-Memory Key-Value Store

A lightweight, multi-threaded in-memory key-value store inspired by Redis, implemented in C++.

## Features

- In-memory key-value storage
- TTL (Time To Live) support
- Sorted Sets (ZSET) implementation

## Building

```bash
g++ -std=c++11 -pthread -o redis_server server.cpp avl.cpp hashtable.cpp heap.cpp thread_pool.cpp zset.cpp
```

```bash
./redis_server
```

# Test the server using the Python script (recommended):
```bash
python redis_test.py
```

### Manual Testing
```bash
./redis_cli.py
```

### Basic Operations
```bash                  # List all keys in database
GET key                 # Get value of key
SET key value          # Set key to value
DEL key               # Delete key
```

### TTL Commands:
```bash
PEXPIRE key ms         # Set key to expire in milliseconds
PTTL key               # Get remaining time to live in milliseconds
```

### ZSET Commands:
```bash
ZADD leaderboard 100 "player1"    # Add player1 with score 100
ZADD leaderboard 200 "player2"    # Add player2 with score 200
ZSCORE leaderboard "player1"      # Get player1's score (returns 100)
ZREM leaderboard "player1"        # Remove player1
ZQUERY leaderboard 0 "" 0 10       # Get top 10 players
```

# Note: Direct connection with nc is not supported due to binary protocol requirements instead use the python script