# celery-gracefull-stop

[Celery](http://celeryproject.org) plugin, thats adds ability to gracefull stop worker.

# Problem

1. When `celery` receives `SIGTERM` system signal, it's begin stop worker procedure called **Warm shutdown**. Due this procedure, `inspect` and `control` commands are unavailable.
2. Also, if `celery` receives yet another `SIGTERM` system signal, it's terminate all tasks by **Cold shutdown** procedure.

This module provides solution for two cases described above.
Becouse, it's important to waiting for tasks have been finished in case of long running tasks.

# Installation & Setup

```
pip install git+https://github.com/MnogoByte/celery-gracefull-stop.git
```

Then, add following lines to both of your `proj/celery.py` file contains `app` instance.

```python
import celery_gracefull_stop
celery_gracefull_stop.register(app)
```

# Settings 

- `CELERY_GRACEFULL_STOP` (boolean). Enables, or disables gracefull stop function. (`True` by default)

# Systemd users

You can use this module for gracefull reload of celery worker.
Look at [celery@.service](systemd/celery@.service) sample.
This solution works only if you starts only one worker by registered service, becouse systemd require only one master `pid` for restart. (e.g. you can register multiple services within this service file by `systemctl enable celery@<service_name>`. Also, you must have `/etc/conf.d/celery_<service_name>` configuration file).

# Limitations

This module has been tested only with celery 3.1 with pool=prefork.

# Author

[Antonov Mikhail](https://github.com/atin65536)

# License

[BSD - 3](LICENSE)
