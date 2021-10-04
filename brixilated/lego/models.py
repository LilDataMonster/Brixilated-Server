from django.db import models
from django.utils.translation import gettext_lazy as _


class LegoSet(models.Model):
    name = models.CharField(unique=True, max_length=32)
    description = models.TextField(max_length=256, blank=True)

    def __str__(self) -> str:
        return f'Name: {self.name}, Description: {self.description}'


class LegoPieces(models.Model):
    lego_set = models.ForeignKey('LegoSet', on_delete=models.CASCADE, related_name='LegoPieces')
    lego_piece = models.ForeignKey('LegoPiece', on_delete=models.CASCADE, related_name='LegoPiece')
    hex_color = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f'Lego Set: {self.lego_set.name}, Lego Piece: {self.lego_piece.part_number}, Quantity: {self.quantity}, Color: {self.hex_color:#08x}'


class LegoPiece(models.Model):

    class LegoPieceCategory(models.TextChoices):
        BASIC = 'BA', _('Basic')
        WALL = 'WA', _('Wall')
        SNOT = 'SN', _('Snot')
        CLIP = 'CL', _('Clip')
        HINGE = 'HI', _('Hinge')
        SOCKET = 'SO', _('Socket')
        ANGLE = 'AN', _('Angle')
        CURVED = 'CU', _('Curved')
        VEHICLE = 'VE', _('Vehicle')
        MINIFIG = 'MI', _('Minifig')
        NATURE = 'NA', _('Nature')
        TECHNIC = 'TE', _('Technic')
        ELECTRONICS = 'EL', _('Electronics')
        OTHER = 'OT', _('Other')
        RETIRED = 'RE', _('Retired')

    part_number = models.PositiveSmallIntegerField()
    name = models.CharField(unique=True, max_length=16)
    category = models.CharField(max_length=2, choices=LegoPieceCategory.choices, default=LegoPieceCategory.OTHER)
    description = models.TextField(max_length=256, blank=True)

    def __str__(self) -> str:
        return f'Piece: {self.name}, Number: {self.part_number}'
