from django.db import models
from django.utils.translation import gettext_lazy as _


class LegoSet(models.Model):
    name = models.CharField(unique=True, max_length=32, help_text='Name of Lego Set')
    description = models.TextField(max_length=256, blank=True, help_text='Lego Set description')
    is_complete_set = models.BooleanField(default=False, help_text='Data-structure is a Complete Lego Set')

    def __str__(self) -> str:
        return f'Name: {self.name}, Completed Set: {self.is_complete_set}, Description: {self.description}'

    class Meta:
        verbose_name = 'Lego Set'
        verbose_name_plural = 'Lego Sets'


class LegoPieces(models.Model):
    lego_set = models.ForeignKey('LegoSet', on_delete=models.CASCADE, related_name='LegoPieces')
    lego_piece = models.ForeignKey('LegoPiece', on_delete=models.CASCADE, related_name='LegoPiece')
    lego_color = models.ForeignKey('LegoColor', on_delete=models.CASCADE, related_name='LegoColor')
    element_id = models.PositiveIntegerField(null=True, unique=True, help_text='Lego Piece Element ID')
    quantity = models.PositiveSmallIntegerField(help_text='Number of Lego pieces')

    def __str__(self) -> str:
        return f'Lego Set: {self.lego_set.name}, Lego Piece: {self.lego_piece.ldraw_id}, ' \
               f'Quantity: {self.quantity}, Color: {self.lego_color.name:#08x}'

    class Meta:
        verbose_name = 'Set Piece'
        verbose_name_plural = 'Set Pieces'


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

    ldraw_id = models.CharField(max_length=64, null=True, unique=True, help_text='Lego piece LDraw ID')
    bl_item_no = models.CharField(max_length=64, null=True, unique=True, help_text='Lego piece BL Item Number')
    part_name = models.CharField(blank=True, max_length=64, help_text='Lego piece name')
    category = models.CharField(max_length=2, choices=LegoPieceCategory.choices,
                                default=LegoPieceCategory.OTHER, help_text='Lego piece category')
    description = models.TextField(max_length=256, blank=True, help_text='Lego piece Description')
    weight = models.PositiveSmallIntegerField(null=True, help_text='Lego piece weight')
    custom_piece = models.BooleanField(default=False, help_text='Lego piece is a custom piece')

    def __str__(self) -> str:
        return f'Piece: {self.part_name}, LDraw Number: {self.ldraw_id}'

    class Meta:
        verbose_name = 'Piece'
        verbose_name_plural = 'Pieces'


class LegoColor(models.Model):

    class LegoColorCategory(models.TextChoices):
        SOLID = 'SO', _('Solid')
        TRANSPARENT = 'TR', _('Transparent')
        PEARL = 'PE', _('Pearl')
        CHROME = 'CH', _('Chrome')
        METALLIC = 'ME', _('Metallic')
        MILKY = 'MI', _('Milky')
        GLITTER = 'GL', _('Glitter')
        SATIN = 'SA', _('Satin')
        SPECKLE = 'SP', _('Speckle')
        INK = 'IN', _('Ink')
        PROCESS = 'PR', _('Process')
        MODULEX = 'MO', _('Modulex')
        OTHER = 'OT', _('Other')

    material = models.CharField(max_length=2, choices=LegoColorCategory.choices,
                                default=LegoColorCategory.OTHER, help_text='Lego color material')
    lego_id = models.PositiveSmallIntegerField(null=True, help_text='Lego color ID')
    name = models.CharField(null=True, blank=True, max_length=64, help_text='Lego color name')
    bl_color_id = models.PositiveSmallIntegerField(null=True, help_text='Lego color BL ID')
    bl_color_name = models.CharField(blank=True, null=True, max_length=64, help_text='Lego color BL name')
    bo_color_name = models.CharField(blank=True, null=True, max_length=64, help_text='Lego color BO name')
    ldraw_color_id = models.PositiveSmallIntegerField(null=True, help_text='Lego color LDraw ID')
    ldraw_color_name = models.CharField(blank=True, null=True, max_length=64, help_text='Lego color LDraw name')
    peeron_name = models.CharField(blank=True, null=True, max_length=64, help_text='Lego color Peeron name')
    other = models.TextField(max_length=128, null=True, blank=True, help_text='Lego color other')
    year_start = models.PositiveSmallIntegerField(blank=True, null=True, help_text='Lego color Year Start')
    year_end = models.PositiveSmallIntegerField(blank=True, null=True, help_text='Lego color Year End')
    notes = models.TextField(max_length=128, null=True, blank=True, help_text='Lego color notes')
    hex_code = models.CharField(blank=True, null=True, max_length=6, help_text='Lego color hex code')
    cyan = models.PositiveSmallIntegerField(null=True, help_text='Lego color cyan')
    magenta = models.PositiveSmallIntegerField(null=True, help_text='Lego color magenta')
    yellow = models.PositiveSmallIntegerField(null=True, help_text='Lego color yellow')
    black = models.PositiveSmallIntegerField(null=True, help_text='Lego color black')
    pantone = models.CharField(blank=True, null=True, max_length=64, help_text='Lego color pantone')

    def __str__(self) -> str:
        return f'Color ID: {self.lego_id}, Name: {self.name}'

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
