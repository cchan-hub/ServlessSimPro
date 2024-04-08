### This is the control layer of simulator, consisting of:
* Container Migration &rarr; ContainerConsolidation.py
* Container Deployment &rarr; ContainerPlacement.py
* Queuing and Concurrency Control &rarr; PopQueue.py
* Resource Allocation &rarr; RequestAllocation.py

Each *.py file contains some related algorithms. Users can choose suitable algorithms to use or write their own algorithms.

### How to choose suitable algorithms?
Just by changing the algorithm name in [simulator.py](../simulator.py).
```
ContainerPlacementStrategy = ConPlaceAlgo.FIRST_FIT
RequestAllocationStrategy = ReqAllocAlgo.EARLIEST_KILLED
ContainerConsolidationStrategy = ConConsAlgo.MIN_PM_NUM
PopQueueStrategy = PopQueueAlgo.FCFS
```

The algorithm names are listed in [enumClass.py](../enumClass/enumClass.py).

### How to write your own algorithms?
1. Add your algorithm function in one of the *.py(ContainerConsolidation, ContainerPlacement, PopQueue, RequestAllocation) file.
2. Add your algorithm name in [enumClass.py](../enumClass/enumClass.py).
3. Change the algorithm name to your algorithm name in [simulator.py](../simulator.py).
 ```
ContainerPlacementStrategy = ConPlaceAlgo.FIRST_FIT
RequestAllocationStrategy = ReqAllocAlgo.EARLIEST_KILLED
ContainerConsolidationStrategy = ConConsAlgo.MIN_PM_NUM
PopQueueStrategy = PopQueueAlgo.FCFS
```