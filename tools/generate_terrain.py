import os
import random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

class BrazilBiomeFactory:
    def __init__(self, base_dir="biomas_tiles"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        
        # Database de Biomas Brasileiros
        self.biomes = {
            # Nome: (cor_base, (densidade_vegetacao, cor_vegetacao, densidade_pedras, densidade_fissuras, tipo_vegetacao, conchas))
            "amazonia": [(25, 80, 40), (140, (15, 45, 15, 160), 10, 0, "mato", False)],
            "cerrado": [(200, 150, 85), (100, (160, 140, 60, 150), 45, 0, "capim", False)],
            "pantanal": [(90, 110, 75), (120, (30, 70, 20, 150), 20, 5, "capim", True)],
            "caatinga": [(215, 190, 145), (35, (130, 115, 90, 120), 120, 30, "mato", False)],
            "mata_atlantica": [(40, 100, 60), (150, (20, 50, 15, 170), 25, 0, "mato", False)],
            "pampa": [(110, 175, 65), (200, (40, 90, 30, 150), 5, 0, "mato", False)],
        }

    def _generate_base_texture(self, color, noise_variance, current_size):
        """Gera a textura base do bioma"""
        r, g, b = color
        noise = np.random.normal(0, noise_variance, (current_size, current_size))
        
        # Manchas de variação
        low_res_size = max(4, int(current_size / 16))
        low_res = np.random.normal(0, 12, (low_res_size, low_res_size))
        stains = np.array(Image.fromarray(low_res).resize((current_size, current_size), 
                                                        resample=Image.BICUBIC))
        
        img_array = np.zeros((current_size, current_size, 3), dtype=np.uint8)
        img_array[..., 0] = np.clip(r + noise + stains, 0, 255)
        img_array[..., 1] = np.clip(g + noise + stains, 0, 255)
        img_array[..., 2] = np.clip(b + noise + stains, 0, 255)
        
        return Image.fromarray(img_array, "RGB").convert("RGBA")

    def _add_biome_features(self, draw, biome_config, current_size):
        """Adiciona características específicas do bioma (vegetação, pedras, etc.)"""
        if not biome_config:
            return
            
        veg_density, veg_color, stone_density, crack_density, veg_type, has_shells = biome_config
        
        # Escala relativa ao padrão de 512px
        scale = current_size / 512.0
        area_scaler = scale ** 2

        # 1. Vegetação
        veg_count = int(veg_density * area_scaler)
        for _ in range(veg_count):
            x = random.randint(0, current_size)
            y = random.randint(0, current_size)
            
            if veg_type == "capim":
                height_range = (8, 18)
            else:  # "mato"
                height_range = (4, 10)
                
            height = random.randint(int(height_range[0] * scale), 
                                   int(height_range[1] * scale))
            offset_x = random.randint(int(-4 * scale), int(4 * scale))
            
            draw.line([(x, y), (x + offset_x, y - height)],
                      fill=veg_color, 
                      width=max(1, int(1.5 * scale)))

        # 2. Pedras
        stone_count = int(stone_density * area_scaler)
        for _ in range(stone_count):
            x = random.randint(0, current_size)
            y = random.randint(0, current_size)
            width = random.randint(int(5 * scale), int(12 * scale))
            stroke_width = max(1, int(2 * scale))
            
            # Sombra da pedra
            draw.ellipse([x + stroke_width, y + stroke_width, 
                         x + width + stroke_width, y + int(width * 0.8) + stroke_width],
                        fill=(0, 0, 0, 60))
            
            # Pedra principal
            gray_value = random.randint(110, 160)
            draw.ellipse([x, y, x + width, y + int(width * 0.8)],
                        fill=(gray_value, gray_value, gray_value, 220))

        # 3. Conchas (para biomas com água)
        if has_shells:
            shell_count = int(35 * area_scaler)
            for _ in range(shell_count):
                x = random.randint(0, current_size)
                y = random.randint(0, current_size)
                width = random.randint(int(3 * scale), int(7 * scale))
                start_angle = random.randint(0, 180)
                end_angle = random.randint(200, 360)
                
                draw.arc([x, y, x + width, y + width],
                        start=start_angle,
                        end=end_angle,
                        fill=(245, 245, 230, 200),
                        width=max(1, int(2 * scale)))

        # 4. Fissuras (para biomas secos)
        if crack_density > 0:
            crack_count = int(crack_density * area_scaler)
            for _ in range(crack_count):
                x = random.randint(0, current_size)
                y = random.randint(0, current_size)
                draw.line([(x, y), (x + int(10 * scale), y + int(8 * scale))],
                         fill=(0, 0, 0, 40),
                         width=max(1, int(scale)))

    def generate_biome(self, biome_name, target_size, output_folder):
        """Gera um tile para um bioma específico"""
        os.makedirs(os.path.join(self.base_dir, output_folder), exist_ok=True)
        
        if biome_name not in self.biomes:
            print(f"⚠️  Bioma '{biome_name}' não encontrado!")
            return
            
        color, config = self.biomes[biome_name]
        
        # Gera textura base
        noise_variance = 18  # Variação do ruído para biomas terrestres
        base_texture = self._generate_base_texture(color, noise_variance, target_size)
        
        # Adiciona características do bioma
        overlay = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
        self._add_biome_features(ImageDraw.Draw(overlay), config, target_size)
        
        # Combina as camadas
        final_image = Image.alpha_composite(base_texture, overlay).convert("RGB")
        final_image = final_image.filter(ImageFilter.SHARPEN)
        
        # Salva o arquivo
        output_path = os.path.join(self.base_dir, output_folder, f"{biome_name}.png")
        final_image.save(output_path)
        print(f"✅ {biome_name} ({target_size}px) salvo em: {output_path}")

    def generate_production_tiles(self, size=512):
        """Gera tiles de produção em alta resolução"""
        print(f"🚀 Gerando tiles de produção ({size}px)...")
        for biome_name in self.biomes.keys():
            self.generate_biome(biome_name, size, "producao")

    def generate_debug_tiles(self, size=64):
        """Gera tiles de debug em baixa resolução"""
        print(f"🧪 Gerando tiles de debug ({size}px)...")
        for biome_name in self.biomes.keys():
            self.generate_biome(biome_name, size, "debug")

def main():
    # Cria a fábrica de biomas
    factory = BrazilBiomeFactory()
    
    # 1. Gera tiles de produção (alta resolução)
    factory.generate_production_tiles(size=512)
    
    # 2. Gera tiles de debug (baixa resolução)
    factory.generate_debug_tiles(size=64)
    
    print(f"\n✨ Todos os biomas foram gerados com sucesso!")
    print("📁 Estrutura de arquivos criada:")
    print("   ├── producao/ (tiles de 512px)")
    print("   └── debug/ (tiles de 64px)")
    
    # Lista os biomas gerados
    print(f"\n📋 Biomas incluídos:")
    for biome in factory.biomes.keys():
        print(f"   • {biome.replace('_', ' ').title()}")

if __name__ == "__main__":
    main()