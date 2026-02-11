from biome_base import BaseBiome

class PantanalBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("pantanal", base_dir)
    
    def get_base_color(self):
        return (90, 110, 75)
    
    def get_biome_config(self):
        return (120, (30, 70, 20, 150), 20, 5, "capim", True)