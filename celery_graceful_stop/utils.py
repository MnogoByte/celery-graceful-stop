# -*- coding: utf-8 -*-

from celery import apps

__all__ = ['register']

def register(app):
    from .bootsteps import GracefulWorkerStop, GracefulConsumerStop

    app.steps['worker'].add(GracefulWorkerStop)
    app.steps['consumer'].add(GracefulConsumerStop)
