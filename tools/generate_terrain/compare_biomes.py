"""
Compara as duas versões do gerador de biomas - Versão corrigida
"""

import os
from PIL import Image
import numpy as np

def compare_versions():
    """Compara as texturas geradas pelas duas versões"""
    print("🔍 COMPARANDO VERSÕES DE BIOMAS")
    print("=" * 60)
    
    biomes = ["amazonia", "cerrado", "pantanal", "caatinga", "mata_atlantica", "pampa"]
    
    print("\n📊 ESTATÍSTICAS DAS TEXTURAS GERADAS:")
    print("-" * 60)
    
    for biome in biomes:
        path = f"biomas_tiles/producao/{biome}.png"
        if os.path.exists(path):
            try:
                img = Image.open(path)
                print(f"\n📍 {biome.upper().replace('_', ' ')}")
                print(f"   Tamanho: {img.size}")
                print(f"   Modo: {img.mode}")
                print(f"   Formato: {img.format}")
                
                # Calcula estatísticas de cores sem matplotlib
                if img.mode == 'RGB':
                    arr = np.array(img)
                    
                    # Cores únicas
                    unique_colors = len(np.unique(arr.reshape(-1, 3), axis=0))
                    print(f"   Cores únicas: {unique_colors}")
                    
                    # Média das cores
                    mean_color = arr.mean(axis=(0,1)).astype(int)
                    print(f"   Cor média: RGB{tuple(mean_color)}")
                    
                    # Contraste
                    contrast = arr.std()
                    print(f"   Contraste: {contrast:.1f}")
                    
                    # Tamanho do arquivo
                    file_size = os.path.getsize(path) / 1024
                    print(f"   Tamanho arquivo: {file_size:.1f} KB")
                    
            except Exception as e:
                print(f"   ❌ Erro ao analisar {biome}: {e}")
        else:
            print(f"\n📍 {biome.upper().replace('_', ' ')}")
            print(f"   ⚠️  Arquivo não encontrado: {path}")
    
    print("\n" + "=" * 60)
    print("📁 RESUMO DE ARQUIVOS GERADOS:")
    
    total_files = 0
    total_size = 0
    
    for root, dirs, files in os.walk("biomas_tiles"):
        level = root.replace("biomas_tiles", '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for f in files:
            if f.endswith('.png'):
                filepath = os.path.join(root, f)
                size = os.path.getsize(filepath) / 1024
                total_size += size
                total_files += 1
                print(f'{subindent}{f} ({size:.1f} KB)')
    
    print(f"\n📈 TOTAL: {total_files} arquivos, {total_size:.1f} KB")
    print("=" * 60)

def check_biome_quality():
    """Verifica a qualidade visual dos biomas"""
    print("\n🎨 ANÁLISE DE QUALIDADE VISUAL:")
    print("-" * 60)
    
    biomes = ["amazonia", "cerrado", "pantanal", "caatinga", "mata_atlantica", "pampa"]
    
    for biome in biomes:
        prod_path = f"biomas_tiles/producao/{biome}.png"
        debug_path = f"biomas_tiles/debug/{biome}.png"
        
        prod_exists = os.path.exists(prod_path)
        debug_exists = os.path.exists(debug_path)
        
        status = []
        if prod_exists:
            prod_size = os.path.getsize(prod_path) / 1024
            status.append(f"Produção: {prod_size:.1f}KB")
        if debug_exists:
            debug_size = os.path.getsize(debug_path) / 1024
            status.append(f"Debug: {debug_size:.1f}KB")
        
        if prod_exists and debug_exists:
            print(f"✅ {biome.upper().replace('_', ' ')}: {' | '.join(status)}")
        elif prod_exists or debug_exists:
            print(f"⚠️  {biome.upper().replace('_', ' ')}: {' | '.join(status)} (parcial)")
        else:
            print(f"❌ {biome.upper().replace('_', ' ')}: Nenhum arquivo encontrado")

if __name__ == "__main__":
    compare_versions()
    check_biome_quality()