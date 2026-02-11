from biome_base import BaseBiome

class CerradoBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("cerrado", base_dir)
    
    def get_base_color(self):
        return (200, 150, 85)
    
    def get_biome_config(self):
        return (100, (160, 140, 60, 150), 45, 0, "capim", False)