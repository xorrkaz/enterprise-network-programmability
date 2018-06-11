## DO NOT modify this file. Use _LabEnv.py

# Replace YOUR-NAME-HERE in the line below
LAB_USER = 'YOUR-NAME-HERE'

# Get your Cisco Spark access token from developer.ciscospark.com
# 1) Login
# 2) Copy the Access Token from top-right corner portrait icon
# 3) replace YOUR-ACCESS-TOKEN-HERE in the line below
LAB_USER_SPARK_TOKEN = 'YOUR-ACCESS-TOKEN-HERE'

LAB_SESSION = 'dCloud DNA Network Programmability Lab v1.4'

SPARK_ROOM_NAME = 'LTRNMS-3602: Enterprise SDN: Advanced Network Programming Hands-On Lab'


# temporary change for backwards compatibility

import os  # noqa
if os.path.isfile(os.path.join(os.path.dirname(__file__), '_LabEnv.py')):
    import _LabEnv
    LAB_USER = _LabEnv.LAB_USER
    LAB_USER_SPARK_TOKEN = _LabEnv.LAB_USER_SPARK_TOKEN
