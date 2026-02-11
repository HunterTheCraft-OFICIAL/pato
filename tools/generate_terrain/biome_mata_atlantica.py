from biome_base import BaseBiome

class MataAtlanticaBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("mata_atlantica", base_dir)
    
    def get_base_colors(self):
        """Verdes vibrantes e escuros - floresta tropical costeira"""
        return [
            (40, 100, 60),    # Verde vibrante
            (30, 90, 50),     # Verde escuro vibrante
            (50, 110, 70),    # Verde claro vibrante
            (35, 95, 55),     # Verde médio vibrante
            (45, 105, 65)     # Verde floresta costeira
        ]
    
    def get_biome_config(self):
        """Configuração específica da Mata Atlântica"""
        return {
            "vegetation": ("mato_alto", (20, 50, 15, 170), 180, {}),
            "shadows": 60,  # Manchas sombreadas densas
            "color_variations": ((40, 100, 60), 15)  # Variações sutis de verde
        }