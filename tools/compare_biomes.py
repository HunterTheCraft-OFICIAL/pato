"""
Compara as duas versões do gerador de biomas
"""

import os
from PIL import Image
import matplotlib.pyplot as plt

def compare_versions():
    """Compara as texturas geradas pelas duas versões"""
    print("🔍 COMPARANDO VERSÕES DE BIOMAS")
    print("=" * 60)
    
    biomes = ["amazonia", "cerrado", "pantanal", "caatinga", "mata_atlantica", "pampa"]
    
    print("\n📊 ESTATÍSTICAS DAS TEXTURAS GERADAS:")
    print("-" * 60)
    
    for biome in biomes:
        old_path = f"biomas_tiles/producao/{biome}.png"
        # Verifica se o arquivo existe
        if os.path.exists(old_path):
            try:
                img = Image.open(old_path)
                print(f"\n📍 {biome.upper().replace('_', ' ')}")
                print(f"   Tamanho: {img.size}")
                print(f"   Modo: {img.mode}")
                print(f"   Formato: {img.format}")
                
                # Calcula estatísticas de cores
                if img.mode == 'RGB':
                    # Converte para array numpy para análise
                    import numpy as np
                    arr = np.array(img)
                    print(f"   Cores únicas: {len(np.unique(arr.reshape(-1, 3), axis=0))}")
                    
                    # Média das cores
                    mean_color = arr.mean(axis=(0,1)).astype(int)
                    print(f"   Cor média: RGB{tuple(mean_color)}")
                    
            except Exception as e:
                print(f"   ❌ Erro ao analisar {biome}: {e}")
        else:
            print(f"\n📍 {biome.upper().replace('_', ' ')}")
            print(f"   ⚠️  Arquivo não encontrado: {old_path}")
    
    print("\n" + "=" * 60)
    print("📁 ESTRUTURA DE PASTAS:")
    
    def list_files(startpath):
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for f in files:
                if f.endswith('.png'):
                    size = os.path.getsize(os.path.join(root, f))
                    print(f'{subindent}{f} ({size/1024:.1f} KB)')

    if os.path.exists("biomas_tiles"):
        list_files("biomas_tiles")
    else:
        print("⚠️  Pasta 'biomas_tiles' não encontrada")

if __name__ == "__main__":
    compare_versions()