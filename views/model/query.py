import logging
import sys
import traceback

import graphene

from services.local_pay_co_data_service import RecordNotFoundError
from views.model.customer_schema import CustomerSchema

_logger = logging.getLogger(__name__)


class Query(graphene.ObjectType):
    customer = graphene.Field(CustomerSchema, customerId=graphene.Int())

    def resolve_customer(self, info, customerId):
        try:
            service = info.context.pay_co_data_service
            data = service.process_usage(customerId)
            if not data:
                return None
            return data
        except RecordNotFoundError:
            _logger.error(traceback.format_exception(*sys.exc_info()))
            raise
