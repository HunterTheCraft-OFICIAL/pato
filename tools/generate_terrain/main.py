from biome_amazonia import AmazoniaBiome
from biome_cerrado import CerradoBiome
from biome_pantanal import PantanalBiome
from biome_caatinga import CaatingaBiome
from biome_mata_atlantica import MataAtlanticaBiome
from biome_pampa import PampaBiome

class BrazilBiomeManager:
    def __init__(self, base_dir="biomas_tiles"):
        self.base_dir = base_dir
        self.biomes = {
            "amazonia": AmazoniaBiome(base_dir),
            "cerrado": CerradoBiome(base_dir),
            "pantanal": PantanalBiome(base_dir),
            "caatinga": CaatingaBiome(base_dir),
            "mata_atlantica": MataAtlanticaBiome(base_dir),
            "pampa": PampaBiome(base_dir)
        }
    
    def generate_all_biomes(self, size=512, output_folder="producao"):
        """Gera todos os biomas em uma resolução específica"""
        print(f"🚀 Gerando tiles de {output_folder} ({size}px)...")
        for biome_name, biome_instance in self.biomes.items():
            biome_instance.generate_biome(size, output_folder)
    
    def generate_production_tiles(self, size=512):
        """Gera tiles de produção em alta resolução"""
        self.generate_all_biomes(size, "producao")
    
    def generate_debug_tiles(self, size=64):
        """Gera tiles de debug em baixa resolução"""
        self.generate_all_biomes(size, "debug")
    
    def generate_specific_biome(self, biome_name, target_size=512, output_folder="producao"):
        """Gera um bioma específico"""
        if biome_name in self.biomes:
            self.biomes[biome_name].generate_biome(target_size, output_folder)
        else:
            print(f"⚠️  Bioma '{biome_name}' não encontrado!")
    
    def list_available_biomes(self):
        """Lista todos os biomas disponíveis"""
        print("📋 Biomas disponíveis:")
        for biome_name in self.biomes.keys():
            print(f"   • {biome_name.replace('_', ' ').title()}")
        return list(self.biomes.keys())

def main():
    # Cria o gerenciador de biomas
    manager = BrazilBiomeManager()
    
    print("=" * 50)
    print("🌿 GERADOR DE BIOMAS BRASILEIROS - PIXEL ART")
    print("=" * 50)
    
    # 1. Lista biomas disponíveis
    manager.list_available_biomes()
    print()
    
    # 2. Gera tiles de produção (alta resolução)
    print("📦 Gerando tiles de produção...")
    manager.generate_production_tiles(size=512)
    print()
    
    # 3. Gera tiles de debug (baixa resolução)
    print("🐛 Gerando tiles de debug...")
    manager.generate_debug_tiles(size=64)
    
    print(f"\n{'='*50}")
    print("✨ Todos os biomas foram gerados com sucesso!")
    print("📁 Estrutura de arquivos criada:")
    print("   ├── producao/ (tiles de 512px)")
    print("   └── debug/ (tiles de 64px)")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()