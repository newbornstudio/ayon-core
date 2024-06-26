# -*- coding: utf-8 -*-
import os
import sys

# this might happen in some 3dsmax version where PYTHONPATH isn't added
# to sys.path automatically
for path in os.environ["PYTHONPATH"].split(os.pathsep):
    if path and path not in sys.path:
        sys.path.append(path)

from ayon_core.hosts.max.api import MaxHost
from ayon_core.pipeline import install_host

host = MaxHost()
install_host(host)
