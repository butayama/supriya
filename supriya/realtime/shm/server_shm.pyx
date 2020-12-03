# distutils: language = c++

from server_shm cimport server_shared_memory_client


cdef class ServerSHM:
    cdef server_shared_memory_client* client

    def __cinit__(self, int port_number):
        self.client = new server_shared_memory_client(port_number)

    def __dealloc__(self):
        del self.client

    def get_control_busses(self):
        return self.c_client.get_control_busses()
