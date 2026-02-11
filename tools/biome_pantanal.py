from biome_base import BaseBiome

class PantanalBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("pantanal", base_dir)
    
    def get_base_colors(self):
        """Verdes médios e azulados - ambiente alagado"""
        return [
            (90, 130, 100),   # Verde azulado
            (80, 120, 90),    # Verde pantaneiro
            (70, 110, 100),   # Verde água
            (85, 140, 110),   # Verde claro alagado
            (75, 125, 95)     # Verde médio úmido
        ]
    
    def get_biome_config(self):
        """Configuração específica do Pantanal"""
        return {
            "vegetation": ("capim_fino", (30, 70, 20, 150), 100, {}),
            "water_areas": True,  # Áreas úmidas
            "shells": True,       # Conchas
            "color_variations": ((80, 120, 90), 10)  # Variações aquosas
        }