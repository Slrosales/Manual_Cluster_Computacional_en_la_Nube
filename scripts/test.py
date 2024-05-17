comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

hostname = MPI.Get_processor_name()

# Gather hostnames from all procesess
all_hostnames = comm.gather(hostname, root = 0)

if rank == 0:
    print("Hostnames of machines in the cluster: ")
    for i, host in enumerate(all_hostnames):
        print(f"Process {i} is running on {host}")
