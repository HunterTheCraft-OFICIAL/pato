"""
Arquivo para testar biomas individuais rapidamente
"""

from biome_amazonia import AmazoniaBiome
from biome_cerrado import CerradoBiome
from biome_pantanal import PantanalBiome
from biome_caatinga import CaatingaBiome
from biome_mata_atlantica import MataAtlanticaBiome
from biome_pampa import PampaBiome

def test_biome(biome_class, size=256, pixel_size=8):
    """Testa um bioma específico"""
    print(f"\n🧪 Testando: {biome_class.__name__}")
    biome = biome_class("testes_rapidos")
    biome.generate_biome(size, "teste", pixel_size)
    print(f"✅ Teste concluído para {biome_class.__name__}")
    return True

def quick_preview():
    """Gera uma prévia rápida de todos os biomas"""
    print("🚀 GERANDO PRÉVIA RÁPIDA (256px)")
    print("=" * 50)
    
    biomes = [
        AmazoniaBiome,
        CerradoBiome,
        PantanalBiome,
        CaatingaBiome,
        MataAtlanticaBiome,
        PampaBiome
    ]
    
    for biome_class in biomes:
        test_biome(biome_class, 256, 8)
    
    print("\n" + "=" * 50)
    print("✨ Prévia de todos os biomas concluída!")
    print("📁 Arquivos salvos em: testes_rapidos/teste/")

if __name__ == "__main__":
    quick_preview()