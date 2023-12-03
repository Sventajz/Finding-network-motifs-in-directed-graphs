#!/usr/bin/env python3
from mpi4py import MPI

name = MPI.Get_processor_name()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print("Pozdrav sa domaćina", name, "od procesa ranga", rank, "od ukupno", size, "procesa")

if rank == 0:
    vendor = MPI.get_vendor()
    print("Podaci o implementaciji MPI-a koja se koristi:", vendor[0], vendor[1])
