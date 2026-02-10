"""
Gerador de tiles de biomas brasileiros (VERSÃO PLANÍCIES).
Gera texturas base para planícies de cada bioma, sem variações topográficas.
Outros scripts podem gerar variações (montanhas, colinas, etc.) para o mesmo diretório.
"""

import os
import random
import math
from pathlib import Path
from typing import Dict, Tuple, List

import numpy as np
from PIL import Image, ImageFilter, ImageDraw

class PlainsBiomeGenerator:
    """Gerador de tiles para planícies dos biomas brasileiros."""
    
    # Configurações específicas para PLANÍCIES
    BIOME_PLAINS = {
        "amazonia": {
            "name": "Amazônia",
            "base_color": (25, 70, 35),  # Verde escuro saturado
            "moisture_level": 0.75,  # Alto
            "vegetation_density": 160,
            "vegetation_colors": [(15, 45, 15, 170), (20, 50, 18, 165), (25, 55, 20, 160)],
            "vegetation_type": "mato",
            "stone_density": 8,  # Poucas pedras
            "features": ["leaf_litter", "moss", "dense_undergrowth", "fallen_logs"],
            "leaf_litter": {
                "density": 180,
                "colors": [(40, 30, 15, 180), (50, 40, 20, 170), (60, 50, 25, 160)],
                "wet_look": True
            },
            "crack_density": 0,  # Solo úmido não racha
            "has_shells": False,
            "moss_on_stones": True,
            "mushrooms": True,
            "texture_variance": 12  # Moderada variação
        },
        
        "cerrado": {
            "name": "Cerrado",
            "base_color": (190, 140, 80),  # Solo avermelhado-alaranjado
            "moisture_level": 0.3,  # Baixo
            "vegetation_density": 100,
            "vegetation_colors": [(160, 140, 60, 150), (150, 130, 50, 155), (140, 120, 40, 160)],
            "vegetation_type": "capim",
            "stone_density": 50,  # Muitas pedras
            "features": ["termite_mounds", "dry_grass", "scattered_bushes"],
            "termite_mounds": {
                "density": 0.02,  # 2% de chance por unidade de área
                "colors": [(180, 150, 110, 200), (190, 160, 120, 190)]
            },
            "crack_density": 5,  # Algumas rachaduras
            "has_shells": False,
            "moss_on_stones": False,
            "mushrooms": False,
            "texture_variance": 20  # Alta variação (solo seco)
        },
        
        "pantanal": {
            "name": "Pantanal",
            "base_color": (65, 85, 60),  # Verde-escuro úmido
            "moisture_level": 0.85,  # Muito alto
            "vegetation_density": 140,  # Vegetação densa
            "vegetation_colors": [(25, 65, 20, 180), (30, 70, 25, 175), (35, 75, 30, 170)],
            "vegetation_type": "capim",
            "stone_density": 15,
            "features": ["moss", "mushrooms", "lush_vegetation", "wet_soil"],
            "moss": {
                "density": 0.4,  # 40% de cobertura em pedras
                "colors": [(40, 70, 30, 180), (50, 80, 40, 170), (60, 90, 50, 160)]
            },
            "crack_density": 0,  # Solo constantemente úmido
            "has_shells": False,  # Conchas serão adicionadas pela camada de água depois
            "moss_on_stones": True,
            "mushrooms": True,
            "mushroom_density": 0.1,
            "texture_variance": 8  # Baixa variação (solo uniforme)
        },
        
        "caatinga": {
            "name": "Caatinga",
            "base_color": (210, 185, 140),  # Solo claro
            "moisture_level": 0.15,  # Muito baixo
            "vegetation_density": 30,  # Vegetação esparsa
            "vegetation_colors": [(130, 115, 90, 120), (120, 105, 80, 125), (110, 95, 70, 130)],
            "vegetation_type": "mato",
            "stone_density": 130,  # Muitíssimas pedras
            "features": ["cracks", "cacti", "dry_vegetation", "exposed_rocks"],
            "cacti": {
                "density": 0.15,
                "colors": [(70, 100, 60, 200), (80, 110, 70, 190)]
            },
            "crack_density": 40,  # Muitas rachaduras
            "has_shells": False,
            "moss_on_stones": False,
            "mushrooms": False,
            "texture_variance": 25  # Muita variação (solo seco)
        },
        
        "mata_atlantica": {
            "name": "Mata Atlântica",
            "base_color": (35, 90, 50),  # Verde intermediário
            "moisture_level": 0.65,
            "vegetation_density": 155,
            "vegetation_colors": [(20, 50, 15, 170), (25, 55, 18, 165), (30, 60, 20, 160)],
            "vegetation_type": "mato",
            "stone_density": 20,
            "features": ["leaf_litter", "moss", "ferns", "fungi"],
            "leaf_litter": {
                "density": 120,
                "colors": [(45, 35, 20, 170), (55, 45, 25, 165), (65, 55, 30, 160)],
                "wet_look": True
            },
            "crack_density": 2,
            "has_shells": False,
            "moss_on_stones": True,
            "mushrooms": True,
            "mushroom_density": 0.08,
            "texture_variance": 15
        },
        
        "pampa": {
            "name": "Pampa",
            "base_color": (105, 165, 60),  # Verde pastagem
            "moisture_level": 0.45,  # Moderado
            "vegetation_density": 210,  # Muita grama
            "vegetation_colors": [(40, 90, 30, 150), (45, 95, 35, 145), (50, 100, 40, 140)],
            "vegetation_type": "mato",
            "stone_density": 3,  # Quase nenhuma pedra
            "features": ["wildflowers", "grasses", "open_field"],
            "wildflowers": {
                "density": 0.25,
                "colors": [
                    (220, 60, 60, 200),   # Vermelho
                    (240, 180, 60, 200),  # Amarelo
                    (180, 80, 180, 200),  # Roxo
                    (240, 140, 60, 200)   # Laranja
                ]
            },
            "crack_density": 0,
            "has_shells": False,
            "moss_on_stones": False,
            "mushrooms": False,
            "texture_variance": 18
        }
    }
    
    def __init__(self, output_dir: str = "biomas_tiles"):
        """Inicializa o gerador de planícies.
        
        Args:
            output_dir: Diretório base para salvar os tiles
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_plains_base_texture(self, config: dict, size: int) -> Image.Image:
        """Gera a textura base para planície.
        
        Args:
            config: Configuração do bioma
            size: Tamanho do tile
            
        Returns:
            Imagem RGBA com textura base
        """
        r, g, b = config["base_color"]
        variance = config["texture_variance"]
        
        # Ruído base
        noise = np.random.normal(0, variance, (size, size))
        
        # Manchas de baixa frequência
        low_res_size = max(4, size // 16)
        low_res = np.random.normal(0, variance * 0.6, (low_res_size, low_res_size))
        stains = np.array(Image.fromarray(low_res).resize(
            (size, size), resample=Image.BICUBIC
        ))
        
        # Combina
        combined = noise * 0.7 + stains * 0.3
        
        # Cria imagem
        img_array = np.zeros((size, size, 3), dtype=np.uint8)
        img_array[..., 0] = np.clip(r + combined, 0, 255)
        img_array[..., 1] = np.clip(g + combined, 0, 255)
        img_array[..., 2] = np.clip(b + combined, 0, 255)
        
        return Image.fromarray(img_array, "RGB").convert("RGBA")
    
    def _add_vegetation_plains(self, draw: ImageDraw.Draw, config: dict, 
                              scale: float, size: int) -> None:
        """Adiciona vegetação típica de planície.
        
        Args:
            draw: Objeto de desenho
            config: Configuração do bioma
            scale: Fator de escala
            size: Tamanho do tile
        """
        density = config["vegetation_density"]
        veg_type = config["vegetation_type"]
        area_scaler = scale ** 2
        
        # Número de elementos baseado na densidade
        if veg_type == "capim":
            count = int(density * 0.8 * area_scaler)  # Capim é mais esparso
            height_range = (6, 16)
            width_range = (1, 2)
        else:  # "mato"
            count = int(density * area_scaler)
            height_range = (4, 10)
            width_range = (1, 3)
        
        for _ in range(count):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            height = random.randint(
                int(height_range[0] * scale),
                int(height_range[1] * scale)
            )
            width = max(1, int(random.uniform(*width_range) * scale))
            
            # Ligeira curvatura
            offset_x = random.randint(int(-3 * scale), int(3 * scale))
            
            draw.line(
                [(x, y), (x + offset_x, y - height)],
                fill=random.choice(config["vegetation_colors"]),
                width=width
            )
    
    def _add_stones_plains(self, draw: ImageDraw.Draw, config: dict,
                          scale: float, size: int) -> None:
        """Adiciona pedras em planície.
        
        Args:
            draw: Objeto de desenho
            config: Configuração do bioma
            scale: Fator de escala
            size: Tamanho do tile
        """
        density = config["stone_density"]
        area_scaler = scale ** 2
        count = int(density * area_scaler)
        
        for _ in range(count):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            width = random.randint(int(4 * scale), int(10 * scale))
            height = int(width * random.uniform(0.7, 0.9))
            stroke_width = max(1, int(1.5 * scale))
            
            # Cor base da pedra
            gray_base = random.randint(100, 150)
            stone_color = (gray_base, gray_base, gray_base, 220)
            
            # Sombra
            shadow_offset = int(2 * scale)
            draw.ellipse([
                x + shadow_offset, y + shadow_offset,
                x + width + shadow_offset, y + height + shadow_offset
            ], fill=(0, 0, 0, 60))
            
            # Pedra principal
            draw.ellipse([x, y, x + width, y + height], fill=stone_color)
            
            # Adiciona musgo se configurado
            if config.get("moss_on_stones", False) and random.random() < 0.3:
                moss_x = x + random.randint(int(width * 0.2), int(width * 0.8))
                moss_y = y + random.randint(int(height * 0.2), int(height * 0.8))
                moss_radius = random.randint(int(2 * scale), int(4 * scale))
                moss_color = random.choice(config.get("moss", {}).get("colors", [(50, 80, 40, 180)]))
                
                draw.ellipse([
                    moss_x, moss_y,
                    moss_x + moss_radius, moss_y + int(moss_radius * 0.5)
                ], fill=moss_color)
    
    def _add_leaf_litter(self, draw: ImageDraw.Draw, config: dict,
                        scale: float, size: int) -> None:
        """Adiciona camada de folhas caídas (para florestas).
        
        Args:
            draw: Objeto de desenho
            config: Configuração do bioma
            scale: Fator de escala
            size: Tamanho do tile
        """
        if "leaf_litter" not in config:
            return
            
        leaf_config = config["leaf_litter"]
        area_scaler = scale ** 2
        count = int(leaf_config["density"] * area_scaler)
        
        for _ in range(count):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            
            # Forma de folha (simplificada)
            width = random.randint(int(3 * scale), int(8 * scale))
            height = int(width * random.uniform(0.6, 0.8))
            
            # Folha caída em ângulo aleatório
            angle = random.uniform(0, 2 * math.pi)
            
            # Pontos para uma forma de folha oval
            points = []
            for i in range(8):
                a = 2 * math.pi * i / 8
                rx = width / 2
                ry = height / 2
                px = x + rx * math.cos(a + angle)
                py = y + ry * math.sin(a + angle)
                points.append((px, py))
            
            draw.polygon(points, fill=random.choice(leaf_config["colors"]))
    
    def _add_cracks(self, draw: ImageDraw.Draw, config: dict,
                   scale: float, size: int) -> None:
        """Adiciona rachaduras no solo (para biomas secos).
        
        Args:
            draw: Objeto de desenho
            config: Configuração do bioma
            scale: Fator de escala
            size: Tamanho do tile
        """
        density = config["crack_density"]
        if density <= 0:
            return
            
        area_scaler = scale ** 2
        count = int(density * area_scaler)
        
        for _ in range(count):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            length = random.randint(int(8 * scale), int(20 * scale))
            width = max(1, int(scale * 0.8))
            
            # Rachadura irregular
            points = [(x, y)]
            for i in range(1, 5):
                px = x + int((i * length / 4) * random.uniform(0.8, 1.2))
                py = y + random.randint(int(-3 * scale), int(3 * scale))
                points.append((px, py))
            
            draw.line(points, fill=(40, 30, 20, 80), width=width, joint="curve")
    
    def _add_cacti(self, draw: ImageDraw.Draw, config: dict,
                  scale: float, size: int) -> None:
        """Adiciona cactos (para Caatinga).
        
        Args:
            draw: Objeto de desenho
            config: Configuração do bioma
            scale: Fator de escala
            size: Tamanho do tile
        """
        if "cacti" not in config:
            return
            
        cactus_config = config["cacti"]
        area_scaler = scale ** 2
        count = int(cactus_config["density"] * 100 * area_scaler)  # Densidade relativa
        
        for _ in range(count):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            height = random.randint(int(10 * scale), int(25 * scale))
            width = random.randint(int(3 * scale), int(8 * scale))
            
            # Forma do cacto (colunar simples)
            cactus_color = random.choice(cactus_config["colors"])
            
            # Corpo principal
            draw.ellipse([
                x, y,
                x + width, y + height
            ], fill=cactus_color)
            
            # "Braços" do cacto (opcional)
            if random.random() < 0.4:
                arm_x = x + random.randint(int(width * 0.3), int(width * 0.7))
                arm_y = y + random.randint(int(height * 0.3), int(height * 0.7))
                arm_width = random.randint(int(2 * scale), int(5 * scale))
                arm_height = random.randint(int(5 * scale), int(15 * scale))
                
                draw.ellipse([
                    arm_x, arm_y,
                    arm_x + arm_width, arm_y + arm_height
                ], fill=cactus_color)
    
    def _add_wildflowers(self, draw: ImageDraw.Draw, config: dict,
                        scale: float, size: int) -> None:
        """Adiciona flores campestres (para Pampa).
        
        Args:
            draw: Objeto de desenho
            config: Configuração do bioma
            scale: Fator de escala
            size: Tamanho do tile
        """
        if "wildflowers" not in config:
            return
            
        flower_config = config["wildflowers"]
        area_scaler = scale ** 2
        count = int(flower_config["density"] * 50 * area_scaler)
        
        for _ in range(count):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            radius = random.randint(int(2 * scale), int(4 * scale))
            
            # Flor simples (círculo colorido)
            draw.ellipse([
                x, y,
                x + radius * 2, y + radius * 2
            ], fill=random.choice(flower_config["colors"]))
    
    def _add_mushrooms(self, draw: ImageDraw.Draw, config: dict,
                      scale: float, size: int) -> None:
        """Adiciona cogumelos (para biomas úmidos).
        
        Args:
            draw: Objeto de desenho
            config: Configuração do bioma
            scale: Fator de escala
            size: Tamanho do tile
        """
        if not config.get("mushrooms", False):
            return
            
        density = config.get("mushroom_density", 0.05)
        area_scaler = scale ** 2
        count = int(density * 30 * area_scaler)
        
        for _ in range(count):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            
            # Chapéu do cogumelo
            cap_size = random.randint(int(3 * scale), int(6 * scale))
            cap_color = random.choice([
                (180, 60, 60, 220),   # Vermelho
                (220, 180, 60, 220),  # Amarelo
                (200, 200, 200, 220),  # Branco
                (150, 100, 60, 220)   # Marrom
            ])
            
            # Caule
            stem_height = random.randint(int(4 * scale), int(8 * scale))
            stem_width = max(1, int(scale))
            
            # Desenha caule
            draw.rectangle([
                x - stem_width//2, y - stem_height,
                x + stem_width//2, y
            ], fill=(220, 200, 180, 240))
            
            # Desenha chapéu
            draw.ellipse([
                x - cap_size//2, y - stem_height - cap_size//3,
                x + cap_size//2, y - stem_height + cap_size//3
            ], fill=cap_color)
    
    def _add_termite_mounds(self, draw: ImageDraw.Draw, config: dict,
                           scale: float, size: int) -> None:
        """Adiciona cupinzeiros (para Cerrado).
        
        Args:
            draw: Objeto de desenho
            config: Configuração do bioma
            scale: Fator de escala
            size: Tamanho do tile
        """
        if "termite_mounds" not in config:
            return
            
        mound_config = config["termite_mounds"]
        area_scaler = scale ** 2
        count = int(mound_config["density"] * 100 * area_scaler)
        
        for _ in range(count):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            width = random.randint(int(6 * scale), int(15 * scale))
            height = random.randint(int(8 * scale), int(20 * scale))
            
            # Forma irregular do cupinzeiro
            draw.ellipse([
                x, y,
                x + width, y + height
            ], fill=random.choice(mound_config["colors"]))
    
    def generate_plains_tile(self, biome_name: str, size: int,
                           folder: str) -> Path:
        """Gera um tile de planície para um bioma específico.
        
        Args:
            biome_name: Nome do bioma
            size: Tamanho do tile
            folder: Subpasta (producao/debug)
            
        Returns:
            Caminho do arquivo salvo
        """
        if biome_name not in self.BIOME_PLAINS:
            raise ValueError(f"Bioma '{biome_name}' não encontrado")
        
        config = self.BIOME_PLAINS[biome_name]
        
        # Cria diretório de saída
        output_folder = self.output_dir / folder
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Gera textura base
        base_texture = self._generate_plains_base_texture(config, size)
        
        # Cria overlay para características
        overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Fator de escala
        scale = size / 512.0
        
        # Adiciona características na ordem correta
        self._add_leaf_litter(draw, config, scale, size)
        self._add_cracks(draw, config, scale, size)
        self._add_stones_plains(draw, config, scale, size)
        self._add_vegetation_plains(draw, config, scale, size)
        self._add_cacti(draw, config, scale, size)
        self._add_wildflowers(draw, config, scale, size)
        self._add_mushrooms(draw, config, scale, size)
        self._add_termite_mounds(draw, config, scale, size)
        
        # Combina camadas
        final_image = Image.alpha_composite(base_texture, overlay)
        final_image = final_image.convert("RGB")
        
        # Aplica filtros de nitidez (sutil)
        final_image = final_image.filter(ImageFilter.SHARPEN)
        
        # Salva arquivo
        filename = f"{biome_name}_plains.png"
        output_path = output_folder / filename
        final_image.save(output_path)
        
        return output_path
    
    def generate_all_plains(self, size: int, folder: str) -> Dict[str, Path]:
        """Gera tiles de planície para todos os biomas.
        
        Args:
            size: Tamanho dos tiles
            folder: Subpasta para salvar
            
        Returns:
            Dicionário com biomas e caminhos dos arquivos
        """
        print(f"🌄 Gerando planícies {folder} ({size}px)...")
        
        results = {}
        for biome_name in self.BIOME_PLAINS.keys():
            try:
                path = self.generate_plains_tile(biome_name, size, folder)
                results[biome_name] = path
                biome_display = self.BIOME_PLAINS[biome_name]["name"]
                print(f"   ✅ {biome_display}")
            except Exception as e:
                print(f"   ❌ Erro em {biome_name}: {e}")
        
        return results
    
    def generate_production_plains(self) -> Dict[str, Path]:
        """Gera tiles de produção (512px) para planícies."""
        return self.generate_all_plains(512, "producao")
    
    def generate_debug_plains(self) -> Dict[str, Path]:
        """Gera tiles de debug (64px) para planícies."""
        return self.generate_all_plains(64, "debug")


def main():
    """Função principal - gera todas as planícies."""
    print("=" * 60)
    print("GERADOR DE PLANÍCIES - BIOMAS BRASILEIROS")
    print("=" * 60)
    
    # Cria gerador
    generator = PlainsBiomeGenerator()
    
    # Gera tiles de produção
    print("\n🏞️  GERANDO PLANÍCIES DE PRODUÇÃO (512px)")
    print("-" * 40)
    production = generator.generate_production_plains()
    
    # Gera tiles de debug
    print("\n🔍 GERANDO PLANÍCIES DE DEBUG (64px)")
    print("-" * 40)
    debug = generator.generate_debug_plains()
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DA GERAÇÃO DE PLANÍCIES")
    print("=" * 60)
    
    print(f"\n📊 Estatísticas:")
    print(f"   • Biomas processados: {len(generator.BIOME_PLAINS)}")
    print(f"   • Tiles de produção: {len(production)} arquivos")
    print(f"   • Tiles de debug: {len(debug)} arquivos")
    
    print(f"\n📁 Estrutura criada em: {generator.output_dir}/")
    print("   ├── producao/")
    for biome in generator.BIOME_PLAINS.keys():
        print(f"   │   ├── {biome}_plains.png")
    print("   └── debug/")
    for biome in generator.BIOME_PLAINS.keys():
        print(f"       ├── {biome}_plains.png")
    
    print(f"\n🌎 Biomas gerados (planícies):")
    for biome_name, config in generator.BIOME_PLAINS.items():
        features = ", ".join(config["features"][:3])
        print(f"   • {config['name']}: {features}")
    
    print("\n💡 Dica: Use outros scripts para gerar variações")
    print("   (montanhas, colinas, etc.) no mesmo diretório.")
    
    print("\n✨ Concluído!")


if __name__ == "__main__":
    main()