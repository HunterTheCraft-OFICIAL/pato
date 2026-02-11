import os
import random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageOps
from abc import ABC, abstractmethod

class BaseBiome(ABC):
    def __init__(self, name, base_dir="biomas_tiles"):
        self.name = name
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        
    @abstractmethod
    def get_biome_config(self):
        """Retorna configuração específica do bioma"""
        pass
    
    @abstractmethod
    def get_base_colors(self):
        """Retorna as cores principais do bioma"""
        pass
    
    def _create_pixelated_mosaic(self, colors, current_size, pixel_size=16):
        """Cria padrão pixelado estilo mosaico Minecraft"""
        # Tamanho do pixel individual
        pixel_grid = current_size // pixel_size
        
        # Cria array para o mosaico
        mosaic = np.zeros((pixel_grid, pixel_grid, 3), dtype=np.uint8)
        
        # Preenche com cores aleatórias da paleta
        for i in range(pixel_grid):
            for j in range(pixel_grid):
                color = random.choice(colors)
                # Adiciona leve variação para parecer natural
                variation = random.randint(-10, 10)
                r = max(0, min(255, color[0] + variation))
                g = max(0, min(255, color[1] + variation))
                b = max(0, min(255, color[2] + variation))
                mosaic[i, j] = [r, g, b]
        
        # Redimensiona para criar efeito pixelado
        img = Image.fromarray(mosaic, "RGB")
        img = img.resize((current_size, current_size), Image.NEAREST)
        
        return img.convert("RGBA")
    
    def _add_vegetation(self, draw, veg_config, current_size, scale):
        """Adiciona vegetação específica do bioma"""
        veg_type, veg_color, veg_density, veg_params = veg_config
        
        veg_count = int(veg_density * (scale ** 2))
        
        for _ in range(veg_count):
            x = random.randint(0, current_size)
            y = random.randint(0, current_size)
            
            if veg_type == "mato_alto":
                # Linhas para mato alto (Amazônia, Mata Atlântica)
                height = random.randint(int(12 * scale), int(24 * scale))
                offset_x = random.randint(int(-6 * scale), int(6 * scale))
                draw.line([(x, y), (x + offset_x, y - height)],
                         fill=veg_color,
                         width=max(1, int(2 * scale)))
                
            elif veg_type == "capim_fino":
                # Linhas finas para capim (Cerrado, Pampa, Pantanal)
                height = random.randint(int(6 * scale), int(16 * scale))
                # Múltiplas hastes finas
                for _ in range(random.randint(1, 3)):
                    offset_x = random.randint(int(-2 * scale), int(2 * scale))
                    draw.line([(x, y), (x + offset_x, y - height)],
                             fill=veg_color,
                             width=max(1, int(scale)))
            
            elif veg_type == "vegetacao_rala":
                # Vegetação esparsa (Caatinga)
                height = random.randint(int(4 * scale), int(10 * scale))
                if random.random() < 0.3:  # Apenas algumas plantas
                    draw.line([(x, y), (x, y - height)],
                             fill=veg_color,
                             width=max(1, int(1.5 * scale)))
    
    def _add_shadows(self, draw, current_size, scale, intensity=40):
        """Adiciona áreas sombreadas para floresta úmida"""
        shadow_count = int(20 * (scale ** 2))
        
        for _ in range(shadow_count):
            x = random.randint(0, current_size)
            y = random.randint(0, current_size)
            radius = random.randint(int(15 * scale), int(40 * scale))
            
            # Círculo de sombra suave
            for r in range(radius, 0, -1):
                alpha = int(intensity * (1 - r/radius))
                draw.ellipse([x-r, y-r, x+r, y+r],
                            fill=(0, 0, 0, alpha))
    
    def _add_water_areas(self, draw, current_size, scale):
        """Adiciona áreas úmidas com tons aquosos"""
        water_count = int(15 * (scale ** 2))
        
        for _ in range(water_count):
            x = random.randint(0, current_size)
            y = random.randint(0, current_size)
            width = random.randint(int(20 * scale), int(60 * scale))
            height = random.randint(int(15 * scale), int(30 * scale))
            
            # Área aquosa com gradiente
            for i in range(height):
                alpha = int(30 * (1 - i/height))
                draw.ellipse([x, y+i, x+width, y+height],
                            fill=(70, 130, 180, alpha),
                            outline=None)
    
    def _add_cracks(self, draw, current_size, scale, color=(0, 0, 0, 60)):
        """Adiciona fissuras para solo seco"""
        crack_count = int(30 * (scale ** 2))
        
        for _ in range(crack_count):
            x = random.randint(0, current_size)
            y = random.randint(0, current_size)
            length = random.randint(int(15 * scale), int(40 * scale))
            
            # Linha de fissura com ramificações
            for i in range(length):
                offset_x = random.randint(int(-2 * scale), int(2 * scale))
                offset_y = random.randint(int(-1 * scale), int(1 * scale))
                draw.line([(x + i, y + offset_y),
                          (x + i + offset_x, y + offset_y)],
                         fill=color,
                         width=max(1, int(scale)))
                
                # Pequenas ramificações ocasionais
                if random.random() < 0.1:
                    branch_length = random.randint(int(3 * scale), int(10 * scale))
                    for j in range(branch_length):
                        draw.line([(x + i, y + offset_y + j),
                                  (x + i, y + offset_y + j + 1)],
                                 fill=color,
                                 width=max(1, int(scale)))
    
    def _add_shells(self, draw, current_size, scale):
        """Adiciona conchas para ambientes aquáticos"""
        shell_count = int(35 * (scale ** 2))
        
        for _ in range(shell_count):
            x = random.randint(0, current_size)
            y = random.randint(0, current_size)
            size = random.randint(int(4 * scale), int(10 * scale))
            
            # Forma de concha (arco)
            draw.arc([x, y, x + size, y + size],
                    start=random.randint(0, 180),
                    end=random.randint(200, 360),
                    fill=(245, 245, 230, 180),
                    width=max(1, int(2 * scale)))
    
    def _add_stones(self, draw, current_size, scale, stone_type="regular"):
        """Adiciona pedras com diferentes estilos para cada bioma"""
        stone_count = int(45 * (scale ** 2))
        
        for _ in range(stone_count):
            x = random.randint(0, current_size)
            y = random.randint(0, current_size)
            width = random.randint(int(6 * scale), int(18 * scale))
            height = random.randint(int(4 * scale), int(12 * scale))
            
            if stone_type == "regular":
                # Pedras regulares (Cerrado)
                gray_value = random.randint(100, 180)
                draw.ellipse([x, y, x + width, y + height],
                            fill=(gray_value, gray_value, gray_value, 220))
                
                # Sombra
                draw.ellipse([x + 2, y + 2, x + width + 2, y + height + 2],
                            fill=(0, 0, 0, 40))
                            
            elif stone_type == "dark":
                # Pedras escuras (Caatinga)
                gray_value = random.randint(80, 140)
                draw.ellipse([x, y, x + width, y + height],
                            fill=(gray_value, gray_value, gray_value, 200))
    
    def _add_color_variations(self, draw, current_size, scale, base_color, variation=15):
        """Adiciona variações sutis de cor"""
        variation_count = int(25 * (scale ** 2))
        
        for _ in range(variation_count):
            x = random.randint(0, current_size)
            y = random.randint(0, current_size)
            size = random.randint(int(10 * scale), int(30 * scale))
            
            # Variação de cor
            r = max(0, min(255, base_color[0] + random.randint(-variation, variation)))
            g = max(0, min(255, base_color[1] + random.randint(-variation, variation)))
            b = max(0, min(255, base_color[2] + random.randint(-variation, variation)))
            
            draw.ellipse([x, y, x + size, y + size],
                        fill=(r, g, b, 50))
    
    def generate_biome(self, target_size, output_folder, pixel_size=16):
        """Gera um tile para o bioma específico"""
        os.makedirs(os.path.join(self.base_dir, output_folder), exist_ok=True)
        
        config = self.get_biome_config()
        base_colors = self.get_base_colors()
        
        # 1. Gera textura base pixelada estilo Minecraft
        base_texture = self._create_pixelated_mosaic(base_colors, target_size, pixel_size)
        
        # 2. Cria overlay para características específicas
        overlay = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        scale = target_size / 512.0
        
        # 3. Aplica características específicas do bioma
        for feature, params in config.items():
            if feature == "vegetation":
                self._add_vegetation(draw, params, target_size, scale)
            elif feature == "shadows":
                self._add_shadows(draw, target_size, scale, params)
            elif feature == "water_areas":
                self._add_water_areas(draw, target_size, scale)
            elif feature == "cracks":
                self._add_cracks(draw, target_size, scale, params)
            elif feature == "shells":
                self._add_shells(draw, target_size, scale)
            elif feature == "stones":
                self._add_stones(draw, target_size, scale, params)
            elif feature == "color_variations":
                self._add_color_variations(draw, target_size, scale, params[0], params[1])
        
        # 4. Combina as camadas
        final_image = Image.alpha_composite(base_texture, overlay).convert("RGB")
        
        # 5. Aplica filtro para suavizar transições
        final_image = final_image.filter(ImageFilter.SMOOTH_MORE)
        
        # 6. Salva o arquivo
        output_path = os.path.join(self.base_dir, output_folder, f"{self.name}.png")
        final_image.save(output_path)
        print(f"✅ {self.name.replace('_', ' ').title()} ({target_size}px) salvo em: {output_path}")
        return output_path