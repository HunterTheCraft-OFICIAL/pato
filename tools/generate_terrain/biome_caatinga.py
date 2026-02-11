from biome_base import BaseBiome

class CaatingaBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("caatinga", base_dir)
    
    def get_base_colors(self):
        """Tons de bege, marrom claro e verde seco - clima semiárido"""
        return [
            (215, 195, 155),  # Bege claro
            (200, 180, 140),  # Bege
            (185, 165, 125),  # Bege escuro
            (170, 150, 110),  # Marrom claro
            (155, 135, 95)    # Marrom terroso
        ]
    
    def get_biome_config(self):
        """Configuração específica da Caatinga"""
        return {
            "vegetation": ("vegetacao_rala", (130, 115, 90, 120), 40, {}),
            "cracks": (0, 0, 0, 60),  # Fissuras no solo
            "stones": "dark",  # Pedras escuras
            "color_variations": ((185, 165, 125), 20)  # Aspecto árido
        }