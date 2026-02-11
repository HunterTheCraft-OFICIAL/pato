from biome_base import BaseBiome

class MataAtlanticaBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("mata_atlantica", base_dir)
    
    def get_base_color(self):
        return (40, 100, 60)
    
    def get_biome_config(self):
        return (150, (20, 50, 15, 170), 25, 0, "mato", False)