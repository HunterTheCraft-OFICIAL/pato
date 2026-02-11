from biome_base import BaseBiome

class CaatingaBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("caatinga", base_dir)
    
    def get_base_color(self):
        return (215, 190, 145)
    
    def get_biome_config(self):
        return (35, (130, 115, 90, 120), 120, 30, "mato", False)