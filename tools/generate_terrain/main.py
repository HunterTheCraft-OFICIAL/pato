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
    
    def generate_all_biomes(self, size=512, output_folder="producao", pixel_size=16):
        """Gera todos os biomas em uma resolução específica"""
        print(f"🚀 Gerando tiles de {output_folder} ({size}px, pixel_size={pixel_size})...")
        print("=" * 60)
        for biome_name, biome_instance in self.biomes.items():
            biome_instance.generate_biome(size, output_folder, pixel_size)
        print("=" * 60)
    
    def generate_production_tiles(self, size=512):
        """Gera tiles de produção em alta resolução"""
        print("\n🌿 GERANDO BIOMAS BRASILEIROS - ESTILO MINECRAFT")
        print("🎨 Texturas pixeladas com elementos específicos de cada bioma")
        print("=" * 60)
        self.generate_all_biomes(size, "producao", pixel_size=16)
    
    def generate_debug_tiles(self, size=64):
        """Gera tiles de debug em baixa resolução"""
        self.generate_all_biomes(size, "debug", pixel_size=4)
    
    def generate_specific_biome(self, biome_name, target_size=512, output_folder="producao", pixel_size=16):
        """Gera um bioma específico"""
        if biome_name in self.biomes:
            print(f"\n🎯 Gerando apenas: {biome_name.replace('_', ' ').title()}")
            self.biomes[biome_name].generate_biome(target_size, output_folder, pixel_size)
        else:
            print(f"⚠️  Bioma '{biome_name}' não encontrado!")
    
    def list_biome_features(self):
        """Lista características específicas de cada bioma"""
        print("\n📋 CARACTERÍSTICAS ESPECÍFICAS DOS BIOMAS:")
        print("=" * 60)
        
        features = {
            "amazonia": [
                "🎨 Paleta: Tons de verde escuro e médio",
                "🌿 Vegetação: Mato alto denso",
                "🌳 Elementos: Áreas sombreadas de floresta úmida",
                "🎯 Estilo: Floresta tropical densa"
            ],
            "cerrado": [
                "🎨 Paleta: Verde amarelado e marrom claro",
                "🌿 Vegetação: Capim fino",
                "🪨 Elementos: Pedras cinzas espalhadas",
                "🎯 Estilo: Campos abertos e vegetação rala"
            ],
            "pantanal": [
                "🎨 Paleta: Verdes médios e azulados",
                "🌿 Vegetação: Capim baixo",
                "💧 Elementos: Áreas úmidas e conchas",
                "🎯 Estilo: Ambiente alagado e rico em água"
            ],
            "caatinga": [
                "🎨 Paleta: Bege, marrom claro e verde seco",
                "🌿 Vegetação: Vegetação rala e acinzentada",
                "🏜️ Elementos: Fissuras no solo e pedras escuras",
                "🎯 Estilo: Clima semiárido e solo rachado"
            ],
            "mata_atlantica": [
                "🎨 Paleta: Verdes vibrantes e escuros",
                "🌿 Vegetação: Vegetação densa em linhas curtas",
                "🌴 Elementos: Manchas sombreadas úmidas",
                "🎯 Estilo: Floresta tropical costeira"
            ],
            "pampa": [
                "🎨 Paleta: Verdes claros e médios",
                "🌿 Vegetação: Capim baixo em linhas finas",
                "🌾 Elementos: Variações sutis de cor",
                "🎯 Estilo: Pradarias e planícies extensas"
            ]
        }
        
        for biome_name, feat_list in features.items():
            print(f"\n📍 {biome_name.replace('_', ' ').title()}:")
            for feature in feat_list:
                print(f"   {feature}")
    
    def list_available_biomes(self):
        """Lista todos os biomas disponíveis"""
        print("📋 BIOMAS DISPONÍVEIS:")
        for biome_name in self.biomes.keys():
            print(f"   • {biome_name.replace('_', ' ').title()}")
        return list(self.biomes.keys())

def main():
    # Cria o gerenciador de biomas
    manager = BrazilBiomeManager()
    
    print("\n" + "=" * 60)
    print("🌿 GERADOR DE BIOMAS BRASILEIROS - ESTILO MINECRAFT")
    print("🎨 Padrões pixelados com elementos específicos de cada bioma")
    print("=" * 60)
    
    # 1. Lista biomas e características
    manager.list_available_biomes()
    manager.list_biome_features()
    
    # 2. Gera tiles de produção (alta resolução)
    print("\n" + "=" * 60)
    print("📦 GERANDO TILES DE PRODUÇÃO...")
    manager.generate_production_tiles(size=512)
    
    # 3. Gera tiles de debug (baixa resolução)
    print("\n" + "=" * 60)
    print("🐛 GERANDO TILES DE DEBUG...")
    manager.generate_debug_tiles(size=64)
    
    print("\n" + "=" * 60)
    print("✨ TODOS OS BIOMAS FORAM GERADOS COM SUCESSO!")
    print("📁 ESTRUTURA DE ARQUIVOS CRIADA:")
    print("   ├── producao/ (tiles de 512px, pixel_size=16)")
    print("   └── debug/ (tiles de 64px, pixel_size=4)")
    print("=" * 60)

if __name__ == "__main__":
    main()