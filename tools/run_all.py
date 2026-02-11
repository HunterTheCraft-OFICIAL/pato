"""
Script para executar todas as funcionalidades
"""

import os
import sys

def main_menu():
    """Menu principal"""
    print("\n" + "=" * 60)
    print("🌿 GERADOR DE BIOMAS BRASILEIROS - MENU PRINCIPAL")
    print("=" * 60)
    print("\nSelecione uma opção:")
    print("1. 🚀 Gerar todos os biomas (produção + debug)")
    print("2. 🧪 Teste rápido (prévia 256px)")
    print("3. 🔍 Comparar versões e estatísticas")
    print("4. 🎨 Criar tileset e cartões visuais")
    print("5. 📁 Listar arquivos gerados")
    print("6. ❌ Sair")
    
    choice = input("\nOpção: ").strip()
    
    if choice == "1":
        print("\nExecutando geração completa...")
        os.system("python main.py")
        
    elif choice == "2":
        print("\nExecutando teste rápido...")
        os.system("python test_single.py")
        
    elif choice == "3":
        print("\nExecutando comparação...")
        os.system("python compare_biomes.py")
        
    elif choice == "4":
        print("\nCriando tileset...")
        os.system("python create_tileset.py")
        
    elif choice == "5":
        print("\nListando arquivos...")
        if os.path.exists("biomas_tiles"):
            for root, dirs, files in os.walk("biomas_tiles"):
                level = root.replace("biomas_tiles", '').count(os.sep)
                indent = ' ' * 2 * level
                print(f'{indent}{os.path.basename(root)}/')
                subindent = ' ' * 2 * (level + 1)
                for f in files:
                    if f.endswith('.png'):
                        size = os.path.getsize(os.path.join(root, f))
                        print(f'{subindent}{f} ({size/1024:.1f} KB)')
        else:
            print("⚠️  Pasta 'biomas_tiles' não encontrada")
            
    elif choice == "6":
        print("\n👋 Até logo!")
        sys.exit(0)
        
    else:
        print("\n⚠️  Opção inválida!")
    
    # Retorna ao menu
    input("\nPressione Enter para continuar...")
    main_menu()

if __name__ == "__main__":
    # Verifica se os arquivos necessários existem
    required_files = ["main.py", "biome_base.py"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("⚠️  Arquivos faltando:", missing_files)
        print("Por favor, certifique-se de que todos os arquivos estão no diretório.")
    else:
        main_menu()