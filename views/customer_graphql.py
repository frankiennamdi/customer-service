from flask_graphql import GraphQLView


class CustomerGraphQl(GraphQLView):

    def __init__(self, pay_co_data_service, **kwargs):
        super(CustomerGraphQl, self).__init__(**kwargs)
        self._pay_co_data_service = pay_co_data_service

    def get_context(self):
        context = super().get_context()
        context.pay_co_data_service = self._pay_co_data_service
        return context
