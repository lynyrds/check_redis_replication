# check_redis_replication
This script is creating a key with values from 1 to 100 on the source Redis DB.
Then it waits for the key to be replicated to the target, reads it and prints it reversed.

Please run the script without arguments to print help.
