# ServlessSimPro
A Comprehensive Serverless Simulation Platform in a Cloud Environment.

Reference article: The related article is currently under review.

### Download and Run
When downloading the code, please use Git. 

After `git clone`, make sure you already download /Trace/AzureFunctionsInvocationTraceForTwoWeeksJan2021.txt. This is the default dataset of our simulator.

It is recommended to use Python 3.9 as the Python interpreter version. 

You can start the simulation by running `simulator.py`.

### Parameter Adjustment

You can adjust the simulation parameter in [simulator.py](simulator.py):
```python
from resource.container import Container
from resource.pm import PM, CPU
from resource.app import App, APP_NUM
import resource.req
import resource.app
from schedulingInterface.ContainerPlacement import FirstFit, MinVectorDist
from schedulingInterface.RequestAllocation import EarliestKilled, LatestKilled, RandomSelection
from schedulingInterface.ContainerConsolidation import MinPmNum
from schedulingInterface.PopQueue import FCFS, SJF, HRRN
from enumClass.enumClass import ReqAllocAlgo, ConPlaceAlgo, ConConsAlgo, PopQueueAlgo, Task, ContainerState

# ####################### Simulation Parameters(Adjustable) #######################
req_num = 1000
P_idle = 92.61
P_max = 259.67
P_mid = 94.8
cs_factor = 0.52

reuseTimeWindow = 600

USE_CONSOLIDATION = True
CONSOLIDATION_TIME_INTERVAL = 300
CONSOLIDATION_THRESHOLD = 0.38

LOG_TIME_INTERVAL = 50

APP_CONF_RANDOM = False

USE_QUEUE = True
QUEUE_THRESHOLD = [50] * APP_NUM
MAX_QUEUE_LENGTH = [20] * APP_NUM

# ####################### Strategies(Adjustable) #######################

ContainerPlacementStrategy = ConPlaceAlgo.FIRST_FIT
RequestAllocationStrategy = ReqAllocAlgo.EARLIEST_KILLED
ContainerConsolidationStrategy = ConConsAlgo.MIN_PM_NUM
PopQueueStrategy = PopQueueAlgo.FCFS
```
For `Simulation Parameters(Adjustable)`:
* `req_num` is the number of arrival requests.
* `P_idle, P_max, P_mid, cs_factor` are related to power of the physical machine.
* `reuseTimeWindow` is the reuse time of the container.
* `USE_CONSOLIDATION, CONSOLIDATION_TIME_INTERVAL, CONSOLIDATION_THRESHOLD` are related to container consolidation strategies.
* `LOG_TIME_INTERVAL` is the time interval of logging.
* `APP_CONF_RANDOM` is whether to use random application configuration.
* `USE_QUEUE, QUEUE_THRESHOLD, MAX_QUEUE_LENGTH` are related to queuing strategies.

For `Strategies(Adjustable)`: refer to [Strategies Readme](./schedulingInterface/README.md)

Noted: `Global Variables` are simulation variables, their values change during simulation.

### Simulation Results
#### Metrics
We provide some metrics such as:
```
Total Energy Consumption
Total Latency
Cold Start Count
Rejection Count
Average CPU Allocation Rate
Average memory Allocation Rate
Average Maximum Concurrency
Average Cold Start State Count
Average Running State Count
Average Idle State Count
Average Dead State Count
Average Active Physical Machine Count
```
These results can be found in [logMetrics.py](./logs/logMetrics)
#### Plot Figs
...
### Contact Information
If you have any questions, please contact 220222036@seu.edu.cn.
