"""
Script para verificar e corrigir problemas de importação
"""

import os
import sys

def check_imports():
    """Verifica se todos os imports necessários estão funcionando"""
    print("🔍 VERIFICANDO IMPORTAÇÕES")
    print("=" * 60)
    
    modules_to_check = [
        ("numpy", "np"),
        ("PIL", "PIL"),
        ("PIL.Image", "Image"),
        ("PIL.ImageDraw", "ImageDraw"),
        ("PIL.ImageFilter", "ImageFilter"),
    ]
    
    all_ok = True
    for module_name, alias in modules_to_check:
        try:
            if '.' in module_name:
                # Para sub-módulos como PIL.Image
                parts = module_name.split('.')
                exec(f"import {parts[0]}")
                for part in parts[1:]:
                    exec(f"import {part}")
            else:
                exec(f"import {module_name} as {alias}")
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✨ Todas as importações estão OK!")
    else:
        print("⚠️  Algumas importações falharam!")
    
    return all_ok

def check_biome_files():
    """Verifica se todos os arquivos de biomas existem"""
    print("\n📁 VERIFICANDO ARQUIVOS DE BIOMAS")
    print("=" * 60)
    
    biome_files = [
        "biome_base.py",
        "biome_amazonia.py",
        "biome_cerrado.py",
        "biome_pantanal.py",
        "biome_caatinga.py",
        "biome_mata_atlantica.py",
        "biome_pampa.py",
        "main.py"
    ]
    
    missing_files = []
    for file in biome_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    print("\n" + "=" * 60)
    if not missing_files:
        print("✨ Todos os arquivos necessários estão presentes!")
    else:
        print(f"⚠️  Arquivos faltando: {', '.join(missing_files)}")
    
    return len(missing_files) == 0

def create_minimal_main():
    """Cria uma versão mínima do main.py se necessário"""
    if not os.path.exists("main.py"):
        print("\n🛠️  Criando arquivo main.py mínimo...")
        with open("main.py", "w") as f:
            f.write('''"""
Versão mínima do gerador de biomas
"""

from biome_amazonia import AmazoniaBiome
from biome_cerrado import CerradoBiome
from biome_pantanal import PantanalBiome
from biome_caatinga import CaatingaBiome
from biome_mata_atlantica import MataAtlanticaBiome
from biome_pampa import PampaBiome

def main():
    print("🌿 GERADOR DE BIOMAS - VERSÃO MÍNIMA")
    
    biomes = [
        ("Amazônia", AmazoniaBiome()),
        ("Cerrado", CerradoBiome()),
        ("Pantanal", PantanalBiome()),
        ("Caatinga", CaatingaBiome()),
        ("Mata Atlântica", MataAtlanticaBiome()),
        ("Pampa", PampaBiome())
    ]
    
    for name, biome in biomes:
        print(f"\\n📍 Gerando {name}...")
        try:
            biome.generate_biome(256, "minimal", 8)
            print(f"✅ {name} gerado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao gerar {name}: {e}")

if __name__ == "__main__":
    main()
''')
        print("✅ main.py criado!")

if __name__ == "__main__":
    print("🛠️  DIAGNÓSTICO DO SISTEMA")
    print("=" * 60)
    
    imports_ok = check_imports()
    files_ok = check_biome_files()
    
    if not files_ok:
        create_minimal_main()
    
    print("\n" + "=" * 60)
    print("🎯 PRÓXIMOS PASSOS RECOMENDADOS:")
    
    if imports_ok and files_ok:
        print("1. ✅ Sistema está pronto para uso!")
        print("2. 🚀 Execute: python main.py")
        print("3. 🎮 Ou use o menu: python run_all.py")
    else:
        print("1. ⚠️  Existem problemas que precisam ser corrigidos")
        print("2. 🔧 Verifique as mensagens acima")
        print("3. 📚 Consulte o README.md para ajuda")
    
    print("=" * 60)