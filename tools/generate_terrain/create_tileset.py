"""
Cria um tileset combinando todos os biomas em uma única imagem
"""

import os
from PIL import Image

def create_tileset():
    """Cria um tileset com todos os biomas"""
    print("🎨 CRIANDO TILESET COM TODOS OS BIOMAS")
    print("=" * 60)
    
    biomes = ["amazonia", "cerrado", "pantanal", "caatinga", "mata_atlantica", "pampa"]
    
    # Tamanho de cada tile
    tile_size = 64
    cols = 3  # 3 colunas
    rows = 2  # 2 linhas (para 6 biomas)
    
    # Cria imagem do tileset
    tileset = Image.new('RGB', (cols * tile_size, rows * tile_size))
    
    for i, biome in enumerate(biomes):
        row = i // cols
        col = i % cols
        
        # Tenta carregar a imagem
        paths = [
            f"biomas_tiles/debug/{biome}.png",
            f"biomas_tiles/producao/{biome}.png"
        ]
        
        img = None
        for path in paths:
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    # Redimensiona para o tamanho do tile
                    img = img.resize((tile_size, tile_size), Image.NEAREST)
                    break
                except:
                    continue
        
        if img:
            # Posiciona no tileset
            x = col * tile_size
            y = row * tile_size
            tileset.paste(img, (x, y))
            print(f"✅ {biome} adicionado ao tileset")
        else:
            print(f"⚠️  {biome} não encontrado")
    
    # Salva o tileset
    tileset.save("biomas_tiles/tileset_completo.png")
    print(f"\n✨ Tileset salvo em: biomas_tiles/tileset_completo.png")
    print(f"📐 Dimensões: {tileset.size}")
    
    # Mostra o tileset (opcional)
    try:
        tileset.show()
    except:
        print("ℹ️  Não foi possível exibir a imagem automaticamente")
    
    return tileset

def create_biome_cards():
    """Cria cartões visuais para cada bioma"""
    print("\n🃏 CRIANDO CARTÕES VISUAIS")
    print("=" * 60)
    
    biomes = {
        "amazonia": "Amazônia",
        "cerrado": "Cerrado",
        "pantanal": "Pantanal",
        "caatinga": "Caatinga",
        "mata_atlantica": "Mata Atlântica",
        "pampa": "Pampa"
    }
    
    for biome_key, biome_name in biomes.items():
        try:
            # Carrega a imagem
            img_path = f"biomas_tiles/debug/{biome_key}.png"
            if os.path.exists(img_path):
                img = Image.open(img_path)
                
                # Cria um cartão com nome
                from PIL import ImageDraw, ImageFont
                
                # Tenta usar uma fonte, senão usa padrão
                try:
                    # Em dispositivos Android, pode ser necessário caminho diferente
                    font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 12)
                except:
                    font = ImageFont.load_default()
                
                # Cria imagem para o cartão
                card = Image.new('RGB', (80, 100), (240, 240, 240))
                draw = ImageDraw.Draw(card)
                
                # Adiciona a imagem
                thumb = img.resize((64, 64), Image.NEAREST)
                card.paste(thumb, (8, 8))
                
                # Adiciona o nome
                draw.text((40, 75), biome_name, fill=(0, 0, 0), font=font, anchor="mm")
                
                # Salva o cartão
                card.save(f"biomas_tiles/card_{biome_key}.png")
                print(f"✅ Cartão criado: {biome_name}")
                
        except Exception as e:
            print(f"⚠️  Erro ao criar cartão para {biome_name}: {e}")
    
    print("\n✨ Cartões visuais criados!")

if __name__ == "__main__":
    create_tileset()
    create_biome_cards()