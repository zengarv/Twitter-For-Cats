from traceback import print_tb
import pandas as pd
import random

# t = pd.read_csv('tweets.csv', delimiter='`')
# print(t.sample())

usernames = pd.read_csv('https://raw.githubusercontent.com/zengarv/Twitter-For-Cats/master/rngusernames.csv')
u = (usernames.sample(n=1))
print(usernames.describe())
for _ in range(10): print(usernames.at[random.randint(0, len(usernames.index)-1), 'Handles'])


