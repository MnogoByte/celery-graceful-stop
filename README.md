# celery-graceful-stop

[Celery](http://celeryproject.org) plugin provides ability of graceful worker stopping.

# Problem
Production deployment of long running tasks require worker to be stopped gracefully. Unfortunately celery got different behaviour:

1. Receiving `SIGTERM` signal by `celery` results starting **Warm shutdown** procedure. Due this procedure, `inspect` and `control` commands become unavailable.
2. More than that, all tasks are terminated forcely by the second `SIGTERM` with the **Cold shutdown** procedure.

This module provides more consistent approach to this problem, it

1. overrides `SIGTERM` receiver to prevent default **Warm shutdown** and **Cold shutdown** worker behaviour,
2. forces `inspect` and `control` commands to be working even after `SIGTERM` signal received.

# Installation & Setup

```
pip install git+https://github.com/MnogoByte/celery-graceful-stop.git
```

Append your `proj/celery.py` file containg `app` instance with the following lines.

```python
import celery_graceful_stop
celery_graceful_stop.register(app)
```

# Settings 

- `CELERY_GRACEFUL_STOP` (boolean). Controls graceful stop function. (`True` by default)

# Using with systemd

1. Define 1 service per each worker you got (systemd require only one master `pid` for restart).
2. Provide `/etc/conf.d/celery_<service_name>` configuration file for each worker.
3. Add [celery@.service](systemd/celery@.service) file into your system.
4. Register your service with `systemctl enable celery@<service_name>`.

# Limitations

- This module disables `pool_shrink`, `pool_grow`, `autoscale`, `pool_reload`, `add_consumer`, `cancel_consumer` control commands after receiving `SIGTERM` signal. Actually, you'll does not need to call them when the worker is shutting down, because worker will not starts new tasks.
- This module has been tested only with celery 3.1 with pool=prefork.

# Author

[Antonov Mikhail](https://github.com/atin65536)

# License

BSD - 3
