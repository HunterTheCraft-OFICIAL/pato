from biome_base import BaseBiome

class PampaBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("pampa", base_dir)
    
    def get_base_colors(self):
        """Verdes claros e médios - pradarias e planícies"""
        return [
            (120, 185, 75),   # Verde claro vibrante
            (110, 175, 65),   # Verde pradaria
            (100, 165, 55),   # Verde médio
            (130, 195, 85),   # Verde claro aberto
            (90, 155, 45)     # Verde campo
        ]
    
    def get_biome_config(self):
        """Configuração específica do Pampa"""
        return {
            "vegetation": ("capim_fino", (40, 90, 30, 150), 220, {}),
            "color_variations": ((110, 175, 65), 10)  # Pequenas variações suaves
        }