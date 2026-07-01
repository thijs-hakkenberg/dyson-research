# CMakeLists.txt — NS-3 scratch scenario for TDMA swarm cluster validation
#
# Usage (from NS-3 top-level directory):
#   cp -r <this-directory> scratch/tdma-swarm-cluster
#   ./ns3 build scratch/tdma-swarm-cluster
#   ./ns3 run scratch/tdma-swarm-cluster -- --clusterSize=100 --phyRateBps=30000
#
# Or build in-tree by adding this directory to scratch/ in the NS-3 source tree.

set(name tdma-swarm-cluster)

set(source_files
    tdma-swarm-cluster.cc
    tdma-net-device.cc
    tdma-scheduler.cc
    ge-channel-model.cc
)

set(header_files
    tdma-net-device.h
    tdma-scheduler.h
    ge-channel-model.h
)

build_lib_example(
    NAME ${name}
    SOURCE_FILES ${source_files}
    LIBRARIES_TO_LINK
        ${libcore}
        ${libnetwork}
        ${libinternet}
        ${libpoint-to-point}
        ${libflow-monitor}
        ${libapplications}
)
