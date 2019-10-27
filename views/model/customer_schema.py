import graphene


class UsageDetails(graphene.ObjectType):
    apiCalls = graphene.String(required=True)
    storage = graphene.String(required=True)
    requestSize = graphene.String(required=True)


class UsageData:
    subscriptionStartsAt = graphene.Int(required=True)
    subscriptionEndsAt = graphene.Int(required=True)
    status = graphene.String(required=True)
    allowsApiOverage = graphene.Boolean(required=True)
    details = graphene.Field(UsageDetails, required=True)


class CustomerSchema(graphene.ObjectType, UsageData):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
