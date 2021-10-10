from django.db import models
from django.utils.translation import gettext_lazy as _


class LegoSet(models.Model):
    name = models.CharField(unique=True, max_length=32, help_text='Name of Lego Set')
    description = models.TextField(max_length=256, blank=True, help_text='Lego Set description')
    is_complete_set = models.BooleanField(default=False, help_text='Data-structure is a Complete Lego Set')

    def __str__(self) -> str:
        return f'Name: {self.name}, Completed Set: {self.is_complete_set}, Description: {self.description}'


class LegoPieces(models.Model):
    lego_set = models.ForeignKey('LegoSet', on_delete=models.CASCADE, related_name='LegoPieces')
    lego_piece = models.ForeignKey('LegoPiece', on_delete=models.CASCADE, related_name='LegoPiece')
    hex_color = models.PositiveIntegerField(help_text='Hex color code of Lego pieces')
    quantity = models.PositiveSmallIntegerField(help_text='Number of Lego pieces')

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

    part_number = models.PositiveSmallIntegerField(unique=True, help_text='Lego piece Part Number')
    name = models.CharField(unique=True, max_length=64, help_text='Lego piece name')
    category = models.CharField(max_length=2, choices=LegoPieceCategory.choices,
                                default=LegoPieceCategory.OTHER, help_text='Lego piece category')
    description = models.TextField(max_length=256, blank=True, help_text='Lego piece Description')

    def __str__(self) -> str:
        return f'Piece: {self.name}, Number: {self.part_number}'
