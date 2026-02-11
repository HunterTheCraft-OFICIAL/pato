from biome_base import BaseBiome

class AmazoniaBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("amazonia", base_dir)
    
    def get_base_colors(self):
        """Tons de verde escuro e médio - floresta tropical úmida"""
        return [
            (15, 45, 15),    # Verde muito escuro
            (25, 80, 40),    # Verde escuro
            (40, 100, 60),   # Verde médio escuro
            (30, 70, 35),    # Verde musgo
            (20, 60, 25)     # Verde floresta
        ]
    
    def get_biome_config(self):
        """Configuração específica da Amazônia"""
        return {
            "vegetation": ("mato_alto", (15, 45, 15, 180), 160, {}),
            "shadows": 50,  # Intensidade das sombras
            "color_variations": ((30, 70, 35), 20)  # Variações de verde profundo
        }