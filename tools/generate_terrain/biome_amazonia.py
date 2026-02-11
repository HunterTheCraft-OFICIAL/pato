from biome_base import BaseBiome

class AmazoniaBiome(BaseBiome):
    def __init__(self, base_dir="biomas_tiles"):
        super().__init__("amazonia", base_dir)
    
    def get_base_color(self):
        return (25, 80, 40)
    
    def get_biome_config(self):
        # (densidade_vegetacao, cor_vegetacao, densidade_pedras, densidade_fissuras, tipo_vegetacao, conchas)
        return (140, (15, 45, 15, 160), 10, 0, "mato", False)