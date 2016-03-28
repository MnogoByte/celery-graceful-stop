# -*- coding: utf-8 -*-

from celery import apps

__all__ = ['register']

def register(app):
    from .bootsteps import GracefullWorkerStop, GracefullConsumerStop

    app.steps['worker'].add(GracefullWorkerStop)
    app.steps['consumer'].add(GracefullConsumerStop)

