
from abc import ABCMeta, abstractmethod

from app.core.schema.mail import MailBase


class MailRepository(metaclass=ABCMeta):

    @abstractmethod
    def send_mail(self, data: MailBase):
        raise NotImplementedError
