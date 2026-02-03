import os
import numpy as np
import random
from PIL import Image, ImageFilter, ImageDraw

class BrazilHydricFactoryV6:
    def __init__(self, size=512, base_dir="tiles_hidricos_v6"):
        self.size = size
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def _generate_water_texture(self, color, current_size):
        """Gera a textura interna da água proporcional ao tamanho."""
        r, g, b = color
        scale = current_size / 512.0
        
        noise = np.random.normal(0, 8, (current_size, current_size))
        low_res_val = max(4, int(current_size / 32))
        low_res = np.random.normal(0, 12, (low_res_val, low_res_val))
        stains = np.array(Image.fromarray(low_res).resize((current_size, current_size), resample=Image.BICUBIC))
        
        img_array = np.zeros((current_size, current_size, 3), dtype=np.uint8)
        img_array[...,0] = np.clip(r + noise + stains, 0, 255)
        img_array[...,1] = np.clip(g + noise + stains, 0, 255)
        img_array[...,2] = np.clip(b + noise + stains, 0, 255)
        
        return Image.fromarray(img_array, "RGB").filter(ImageFilter.GaussianBlur(radius=2.0 * scale))

    def create_modular_water(self, name, color, connections, target_size, folder, size_type="M", is_lake=False, is_sea_transition=False):
        os.makedirs(os.path.join(self.base_dir, folder), exist_ok=True)
        scale = target_size / 512.0
        
        water_tex = self._generate_water_texture(color, target_size).convert("RGBA")
        mask = Image.new("L", (target_size, target_size), 0)
        draw = ImageDraw.Draw(mask)
        
        center = target_size / 2
        # Proporções de largura (P=20%, M=40%, G=75%)
        config_w = {"P": 0.2, "M": 0.4, "G": 0.75}
        half_w = (target_size * config_w[size_type]) / 2
        
        # 1. LOGICA DE LAGO
        if is_lake:
            l_m = 1.35 
            draw.rectangle([center - (half_w * l_m), center - (half_w * l_m), 
                            center + (half_w * l_m), center + (half_w * l_m)], fill=255)

        # 2. LOGICA DE VIAS
        for conn in connections:
            if is_sea_transition:
                if conn == 'N': draw.polygon([(center-half_w, center), (center+half_w, center), (target_size, 0), (0, 0)], fill=255)
                if conn == 'S': draw.polygon([(center-half_w, center), (center+half_w, center), (target_size, target_size), (0, target_size)], fill=255)
                if conn == 'W': draw.polygon([(center, center-half_w), (center, center+half_w), (0, target_size), (0, 0)], fill=255)
                if conn == 'E': draw.polygon([(center, center-half_w), (center, center+half_w), (target_size, target_size), (target_size, 0)], fill=255)
            else:
                if conn == 'N': draw.rectangle([center-half_w, 0, center+half_w, center+half_w], fill=255)
                if conn == 'S': draw.rectangle([center-half_w, center-half_w, center+half_w, target_size], fill=255)
                if conn == 'W': draw.rectangle([0, center-half_w, center+half_w, center+half_w], fill=255)
                if conn == 'E': draw.rectangle([center-half_w, center-half_w, target_size, center+half_w], fill=255)

        # 3. SUAVIZAÇÃO (Feathering) Proporcional
        # Forçamos um mínimo de 1px de blur para não serrilhar no MVP
        blur_rad = max(1.0, (10 + (config_w[size_type] * 18)) * scale)
        mask = mask.filter(ImageFilter.GaussianBlur(radius=blur_rad))
        
        water_tex.putalpha(mask)
        water_tex.save(os.path.join(self.base_dir, folder, f"{name}.png"))

if __name__ == "__main__":
    PROD_SIZE = 512
    factory = BrazilHydricFactoryV6(size=PROD_SIZE)
    
    # Cor padrão de rio
    c_padrao = (45, 110, 190)

    # 1. GERAÇÃO PRODUÇÃO (Exemplo reduzido para focar na estrutura)
    print(f"🌊 Gerando Rios de Produção ({PROD_SIZE}px)...")
    factory.create_modular_water("rio_reto_V_producao", c_padrao, ['N', 'S'], PROD_SIZE, "producao", "M")
    factory.create_modular_water("lago_G_producao", c_padrao, [], PROD_SIZE, "producao", "G", is_lake=True)

    # 2. GERAÇÃO MVP (64px - As 6 Variantes Escolhidas)
    print(f"🧪 Gerando Pasta MVP Hídrico (64px)...")
    
    mvp_list = [
        ("debug_rio_reto_V", ['N', 'S'], "M", False, False),
        ("debug_curva_NE", ['N', 'E'], "M", False, False),
        ("debug_lago_G", [], "G", True, False),
        ("debug_foz_N", ['N'], "G", False, True),
        ("debug_cruzamento_P", ['N', 'S', 'E', 'W'], "P", False, False),
        ("debug_ponta_S", ['S'], "M", False, False)
    ]

    for name, conns, sz_tp, lake, sea in mvp_list:
        factory.create_modular_water(name, c_padrao, conns, 64, "MVP", sz_tp, is_lake=lake, is_sea_transition=sea)

    print("\n✨ V6 Hídrica Concluída com Sucesso!")