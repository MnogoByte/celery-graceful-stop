# -*- coding: utf-8 -*-

from celery import bootsteps
from celery.exceptions import WorkerShutdown
from celery.apps.worker import install_worker_term_hard_handler, platforms
from celery.worker.control import Panel
from celery.utils.log import worker_logger as logger

__all__ = [
    'GracefulWorkerStop',
    'GracefulConsumerStop'
]


class GracefulWorkerStop(bootsteps.StartStopStep):
    conditional = True
    requires = (
        'celery.worker.components:Timer',
        'celery.worker.components:Pool',
        'celery.worker.components:Hub',
    )

    def __init__(self, worker, **kwargs):
        self.enabled = getattr(worker.app.conf, 'CELERY_GRACEFUL_STOP', True)

    def install_worker_term_handler(self):
        def on_next_TERM(*args):
            logger.info('worker: TERM signal received but worker is already in `stop` state. All next TERM signals will be ignored. For Cold shutdown use `INT` and `QUIT` signals')

        def _handler(*args):
            install_worker_term_hard_handler(self.worker, sig='SIGINT')
            platforms.signals['SIGTERM'] = on_next_TERM
            self.worker.graceful_stop()

        platforms.signals['SIGTERM'] = _handler

    def create(self, worker):
        self.worker = worker
        self.timer = worker.timer
        self.pool = worker.pool
        worker.graceful_stop = self.graceful_stop_handler

    def graceful_stop_handler(self):
        self.worker.blueprint.close(self.worker)
        self._wait_stop_pool()
        self.wait_stop_timer = self.timer.call_repeatedly(0.2, self._wait_stop_pool)

    def close(self, worker):
        worker.consumer.graceful_stop()

    def start(self, worker):
        super(GracefulWorkerStop, self).start(worker)

        self.install_worker_term_handler()

    def _wait_stop_pool(self):
        try:
            res = self.pool._pool._join_exited_workers()
            self.pool.shrink(len(self.pool._pool._pool))
        except ValueError: #ignore shrink error
            pass

        if not self.pool._pool._pool:
            self.timer.cancel(self.wait_stop_timer)
            raise WorkerShutdown()


class GracefulConsumerStop(bootsteps.StartStopStep):
    conditional = True
    requires = (
        'celery.worker.consumer:Connection',
        'celery.worker.consumer:Heart',
        'celery.worker.consumer:Events',
        'celery.worker.consumer:Gossip',
        'celery.worker.consumer:Mingle',
        'celery.worker.consumer:Control',
    )

    restricted_control_actions = [
        'pool_grow', 'pool_shrink', 'add_consumer', 'cancel_consumer', 'autoscale', 'pool_reload'
    ]

    def __init__(self, consumer, **kwargs):
        self.enabled = getattr(consumer.app.conf, 'CELERY_GRACEFUL_STOP', True)

    def get_restricted_control_actions(self):
        return self.restricted_control_actions

    def graceful_stop(self):
        for step in self.consumer.steps:
            if type(step) not in self.requires:
                if hasattr(step, 'stop'):
                    logger.debug('| Worker: stopping {}'.format(step))
                    step.stop(self.consumer)

        def fake_action(*args, **kwargs):
            msg = 'Worker: action is disabled while worker is in `stopping` state'
            logger.info(msg)
            raise Exception(msg)

        for action in self.get_restricted_control_actions():
            Panel.data[action] = fake_action


    def create(self, consumer):
        self.consumer = consumer
        consumer.graceful_stop = self.graceful_stop
