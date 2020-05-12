import numpy as np
from datetime import datetime
from mpi4py import MPI


comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

# init cores with sieve
if comm_rank == 0:
    n = int(input("n: "))
    start = datetime.now()
    sieve = np.ones(n + 1)
else:
    n = None
    sieve = None
n = comm.bcast(n, root=0)
sieve = comm.bcast(sieve, root=0)

# distribute sieve
if comm_rank == comm_size-1:
    sub_size = int(n/comm_size)
    begin = sub_size * comm_rank
    sieve = sieve[begin:]
else:
    sub_size = int(n/comm_size)
    begin = sub_size * comm_rank
    end = sub_size * (comm_rank+1)
    sieve = sieve[begin:end]

# apply sieve algorithm
start_index = comm_rank * sub_size
k = 2

while not k**2 >= start_index+len(sieve):
    index_counter = start_index
    while index_counter < len(sieve)+start_index:
        if (index_counter % k) == 0 and index_counter > k:
            sieve[index_counter-start_index] = 0
        index_counter += 1
    k += 1

# reduce sum sieve
sieve = np.sum(sieve)
sieve_sum = comm.reduce(sieve, op=MPI.SUM, root=0)
if comm_rank == 0:
    sieve_sum -= 2
    print(int(sieve_sum))
    print(datetime.now() - start)

