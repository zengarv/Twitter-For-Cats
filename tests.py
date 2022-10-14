import pandas as pd
import random

# t = pd.read_csv('tweets.csv', delimiter='`')
# print(t.sample())

usernames = pd.read_csv('rngusernames.csv')
u = (usernames.sample(n=1))
for _ in range(10): print(usernames.at[random.randint(0, len(usernames.index)-1), 'Adj'])


