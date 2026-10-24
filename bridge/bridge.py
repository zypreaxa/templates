"""Bridge pattern: notifications (abstraction) and delivery channels (implementation).

This module has no GUI dependencies, so it is easy to test independently.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DeliveryResult:
    channel: str
    destination: str
    rendered_message: str
    delivered_at: str


class DeliveryChannel(ABC):  # IMPLEMENTOR
    name: str

    @abstractmethod
    def deliver(self, destination: str, subject: str, body: str) -> DeliveryResult:
        """Simulate sending a message through this channel."""

    def _result(self, destination: str, content: str) -> DeliveryResult:
        return DeliveryResult(self.name, destination, content,
                              datetime.now().strftime('%H:%M:%S'))


class EmailChannel(DeliveryChannel):  # CONCRETE IMPLEMENTOR
    name = 'Email'

    def deliver(self, destination: str, subject: str, body: str) -> DeliveryResult:
        return self._result(destination, f'To: {destination}\nSubject: {subject}\n\n{body}')


class SMSChannel(DeliveryChannel):  # CONCRETE IMPLEMENTOR
    name = 'SMS'

    def deliver(self, destination: str, subject: str, body: str) -> DeliveryResult:
        # Character limit is presented as a simulation, not actual SMS delivery.
        text = f'{subject}: {body}'.replace('\n', ' ')
        if len(text) > 160:
            text = text[:157] + '...'
        return self._result(destination, f'To: {destination}\n{text}\n\n({len(text)}/160 chars)')


class PushChannel(DeliveryChannel):  # CONCRETE IMPLEMENTOR
    name = 'Push'

    def deliver(self, destination: str, subject: str, body: str) -> DeliveryResult:
        return self._result(destination, f'Device: {destination}\n[{subject}]\n{body}')


class Notification(ABC):  # ABSTRACTION
    def __init__(self, channel: DeliveryChannel):
        self.channel = channel  # BRIDGE: composition; not inheritance!

    @abstractmethod
    def prepare(self, subject: str, body: str) -> tuple[str, str]:
        """Define formatting independent of the delivery technology."""

    def send(self, destination: str, subject: str, body: str) -> DeliveryResult:
        subject, body = self.prepare(subject, body)
        return self.channel.deliver(destination, subject, body)


class StandardNotification(Notification):  # REFINED ABSTRACTION
    name = 'Standard'

    def prepare(self, subject: str, body: str) -> tuple[str, str]:
        return subject, body


class UrgentNotification(Notification):  # REFINED ABSTRACTION
    name = 'Urgent'

    def prepare(self, subject: str, body: str) -> tuple[str, str]:
        return f'URGENT — {subject}', f'⚠ IMMEDIATE ATTENTION REQUIRED\n\n{body}'


class SystemNotification(Notification):  # REFINED ABSTRACTION
    name = 'System'

    def prepare(self, subject: str, body: str) -> tuple[str, str]:
        return f'SYSTEM · {subject}', f'[Automated system notification]\n\n{body}\n\n— Notification Studio'


CHANNELS = {'Email': EmailChannel, 'SMS': SMSChannel, 'Push': PushChannel}
NOTIFICATIONS = {'Standard': StandardNotification, 'Urgent': UrgentNotification,
                 'System': SystemNotification}


def dispatch(kind: str, channel: str, destination: str, subject: str, body: str) -> DeliveryResult:
    """Factory convenience for the demonstration UI; not the Bridge itself."""
    alert = NOTIFICATIONS[kind](CHANNELS[channel]())
    return alert.send(destination, subject, body)
