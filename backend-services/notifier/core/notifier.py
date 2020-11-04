import logging
import os
import time
from typing import Dict
from typing import List
from typing import NoReturn

import artemis_utils.rest_util
import ujson as json
from artemis_utils import get_logger
from artemis_utils import RABBITMQ_URI
from artemis_utils.rabbitmq_util import create_exchange
from artemis_utils.rabbitmq_util import create_queue
from artemis_utils.rest_util import ControlHandler
from artemis_utils.rest_util import HealthHandler
from artemis_utils.rest_util import setup_data_task
from artemis_utils.rest_util import start_data_task
from kombu import Connection
from kombu import Consumer
from kombu.mixins import ConsumerProducerMixin
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.web import RequestHandler

log = get_logger()
hij_log = logging.getLogger("hijack_logger")
mail_log = logging.getLogger("mail_logger")
try:
    hij_log_filter = json.loads(os.getenv("HIJACK_LOG_FILTER", "[]"))
except Exception:
    log.exception("exception")
    hij_log_filter = []


class HijackLogFilter(logging.Filter):
    def filter(self, rec):
        if not hij_log_filter:
            return True
        for filter_entry in hij_log_filter:
            for filter_entry_key in filter_entry:
                if rec.__dict__[filter_entry_key] == filter_entry[filter_entry_key]:
                    return True
        return False


mail_log.addFilter(HijackLogFilter())
hij_log.addFilter(HijackLogFilter())

MODULE_NAME = "notifier"
# TODO: add the following in utils
REST_PORT = 3000


class ConfigHandler(RequestHandler):
    """
    REST request handler for configuration.
    """

    def post(self):
        """
        Configures notifier and responds with a success message.
        :return: {"success": True | False, "message": < message >}
        """
        self.write({"success": True, "message": "configured"})


class Notifier:
    """
    Notifier Service.
    """

    def __init__(self):
        self._running = False
        self.worker = None

    def is_running(self):
        return self._running

    def stop(self):
        if self.worker:
            self.worker.should_stop = True
        else:
            self._running = False

    def run(self) -> NoReturn:
        """
        Entry function for this service that runs a RabbitMQ worker through Kombu.
        """
        self._running = True
        try:
            with Connection(RABBITMQ_URI) as connection:
                self.worker = self.Worker(connection)
                self.worker.run()
        except Exception:
            log.exception("exception")
        finally:
            log.info("stopped")
            self._running = False

    class Worker(ConsumerProducerMixin):
        """
        RabbitMQ Consumer/Producer for this Service.
        """

        def __init__(self, connection: Connection) -> NoReturn:
            self.connection = connection

            # TODO: exchanges and queues

            # EXCHANGES
            self.hijack_notification_exchange = create_exchange(
                "hijack-notification", connection, declare=True
            )

            # QUEUES
            self.hij_log_queue = create_queue(
                MODULE_NAME,
                exchange=self.hijack_notification_exchange,
                routing_key="hij-log",
                priority=1,
            )
            self.mail_log_queue = create_queue(
                MODULE_NAME,
                exchange=self.hijack_notification_exchange,
                routing_key="mail-log",
                priority=1,
            )

        def get_consumers(
            self, Consumer: Consumer, channel: Connection
        ) -> List[Consumer]:
            # TODO: consumers
            return [
                Consumer(
                    queues=[self.hij_log_queue],
                    on_message=self.handle_hij_log,
                    prefetch_count=100,
                    accept=["ujson"],
                ),
                Consumer(
                    queues=[self.mail_log_queue],
                    on_message=self.handle_mail_log,
                    prefetch_count=100,
                    accept=["ujson"],
                ),
            ]

        @staticmethod
        def handle_hij_log(message: Dict) -> NoReturn:
            """
            Callback function that generates a hijack log
            """
            message.ack()
            hij_log_msg = message.payload
            hij_log.info(
                "{}".format(json.dumps(hij_log_msg)),
                extra={
                    "community_annotation": hij_log_msg.get(
                        "community_annotation", "NA"
                    )
                },
            )

        @staticmethod
        def handle_mail_log(message: Dict) -> NoReturn:
            """
            Callback function that generates a mail log
            """
            message.ack()
            mail_log_msg = message.payload
            mail_log.info(
                "{}".format(json.dumps(mail_log_msg)),
                extra={
                    "community_annotation": mail_log_msg.get(
                        "community_annotation", "NA"
                    )
                },
            )

        # TODO: encapsulate auto-ignore functionality


def make_app():
    return Application(
        [
            ("/config", ConfigHandler),
            ("/control", ControlHandler),
            ("/health", HealthHandler),
        ]
    )


if __name__ == "__main__":
    # notifier should be initiated in any case
    setup_data_task(Notifier)

    # notifier should start in any case
    start_data_task()
    while not artemis_utils.rest_util.data_task.is_running():
        time.sleep(1)

    # create REST worker
    app = make_app()
    app.listen(REST_PORT)
    log.info("Listening to port {}".format(REST_PORT))
    IOLoop.current().start()
