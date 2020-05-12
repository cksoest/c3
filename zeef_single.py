import numpy as np
from datetime import datetime


n = int(input("n: "))

start = datetime.now()
sieve = np.ones(n+1)

k = 2
while not k**2 > n:
    index_counter = k**2
    while index_counter <= n:
        if (index_counter % k) == 0:
            sieve[index_counter] = 0
        index_counter += 1
    for prime in sieve[k+1:]:
        k += 1
        if prime == 1:
            break

print(sum(sieve)-2)
print(datetime.now()-start)

