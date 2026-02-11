from biome_base import BaseBiome

class CerradoBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("cerrado", base_dir)
    
    def get_base_colors(self):
        """Tons de verde amarelado e marrom claro - campos abertos"""
        return [
            (200, 180, 100),  # Amarelo esverdeado
            (185, 165, 85),   # Amarelo terroso
            (170, 150, 70),   # Marrom amarelado
            (160, 140, 60),   # Marrom claro
            (150, 130, 50)    # Marrom campo
        ]
    
    def get_biome_config(self):
        """Configuração específica do Cerrado"""
        return {
            "vegetation": ("capim_fino", (160, 140, 60, 160), 120, {}),
            "stones": "regular",  # Pedras cinzas espalhadas
            "color_variations": ((170, 150, 70), 15)  # Tons terrosos
        }