//  shared memory interface to the supercollider server
//  Copyright (C) 2011 Tim Blechmann
//  Copyright (C) 2011 Jakob Leben
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation; either version 2 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program; see the file COPYING.  If not, write to
//  the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
//  Boston, MA 02111-1307, USA.

#pragma once

#include <boost/foreach.hpp>
#include <boost/version.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/interprocess/containers/vector.hpp>
#include <boost/interprocess/managed_shared_memory.hpp>
#include <boost/interprocess/offset_ptr.hpp>

namespace detail_server_shm {

using std::pair;
using std::string;

namespace bi = boost::interprocess;
using bi::managed_shared_memory;
using bi::offset_ptr;

static inline string make_shmem_name(unsigned int port_number) {
    return string("SuperColliderServer_") + boost::lexical_cast<string>(port_number);
}

class server_shared_memory {
public:
    typedef offset_ptr<float> sh_float_ptr;

    server_shared_memory(managed_shared_memory& segment, int control_busses) {
        control_busses_ = (float*)segment.allocate(control_busses * sizeof(float));
        std::fill(control_busses_.get(), control_busses_.get() + control_busses, 0.f);
    }

    void destroy(managed_shared_memory& segment) {
        segment.deallocate(control_busses_.get());
    }

    void set_control_bus(int bus, float value) {
        // TODO: we need to set the control busses via a work queue
    }

    float* get_control_busses(void) { return control_busses_.get(); }

private:
    string shmem_name;
    sh_float_ptr control_busses_; // control busses
};


class server_shared_memory_client {
public:
    server_shared_memory_client(unsigned int port_number):
        shmem_name(detail_server_shm::make_shmem_name(port_number)),
        segment(bi::open_only, shmem_name.c_str()) {
        pair<server_shared_memory*, size_t> res = segment.find<server_shared_memory>(shmem_name.c_str());
        if (res.second != 1)
            throw std::runtime_error("Cannot connect to shared memory");
        shm = res.first;
    }

    float* get_control_busses(void) { return shm->get_control_busses(); }

private:
    string shmem_name;
    managed_shared_memory segment;
    server_shared_memory* shm;
};

}

using detail_server_shm::server_shared_memory_client;
