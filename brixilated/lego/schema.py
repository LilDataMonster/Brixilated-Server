import graphene
from graphene_django import DjangoObjectType
from lego.models import LegoSet, LegoPiece


class LegoSetType(DjangoObjectType):
    class Meta:
        model = LegoSet
        fields = '__all__'


class LegoPieceType(DjangoObjectType):
    class Meta:
        model = LegoPiece
        fields = '__all__'


class Query(graphene.ObjectType):
    lego_sets = graphene.List(LegoSetType)
    lego_piece = graphene.List(LegoPieceType)

    @staticmethod
    def resolve_lego_sets(self, info):
        return LegoSet.objects.all()

    @staticmethod
    def resolve_lego_piece(self, info):
        return LegoPiece.objects.all()

    # category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    #
    # def resolve_category_by_name(root, info, name):
    #     try:
    #         return Category.objects.get(name=name)
    #     except Category.DoesNotExist:
    #         return None


schema = graphene.Schema(query=Query)
