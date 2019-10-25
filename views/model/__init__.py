import graphene

from views.model.query import Query

schema = graphene.Schema(query=Query)
