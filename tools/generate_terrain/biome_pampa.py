from biome_base import BaseBiome

class PampaBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("pampa", base_dir)
    
    def get_base_color(self):
        return (110, 175, 65)
    
    def get_biome_config(self):
        return (200, (40, 90, 30, 150), 5, 0, "mato", False)