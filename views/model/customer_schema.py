import graphene


class UsageDetails(graphene.ObjectType):
    apiCalls = graphene.String()
    storage = graphene.String()
    requestSize = graphene.String()


class UsageData:
    subscriptionStartsAt = graphene.Int()
    subscriptionEndsAt = graphene.Int()
    status = graphene.String()
    allowsApiOverage = graphene.Boolean()
    details = graphene.Field(UsageDetails)


class CustomerSchema(graphene.ObjectType, UsageData):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
