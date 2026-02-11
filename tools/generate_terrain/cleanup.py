"""
Limpa arquivos gerados para liberar espaço
"""

import os
import shutil

def cleanup():
    """Remove pastas com arquivos gerados"""
    print("🧹 LIMPEZA DE ARQUIVOS GERADOS")
    print("=" * 60)
    
    folders_to_remove = [
        "biomas_tiles",
        "testes_rapidos",
        "teste_simples"
    ]
    
    total_freed = 0
    files_removed = 0
    
    for folder in folders_to_remove:
        if os.path.exists(folder):
            try:
                # Calcula tamanho antes de remover
                folder_size = 0
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        filepath = os.path.join(root, file)
                        folder_size += os.path.getsize(filepath)
                
                # Remove a pasta
                shutil.rmtree(folder)
                
                total_freed += folder_size
                files_removed += 1
                
                size_mb = folder_size / (1024 * 1024)
                print(f"✅ Removido: {folder} ({size_mb:.2f} MB)")
                
            except Exception as e:
                print(f"❌ Erro ao remover {folder}: {e}")
        else:
            print(f"ℹ️  Pasta não existe: {folder}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMO DA LIMPEZA:")
    print(f"   Pastas removidas: {files_removed}")
    print(f"   Espaço liberado: {total_freed / (1024 * 1024):.2f} MB")
    
    # Remove arquivos .pyc e __pycache__
    print("\n🔧 Limpando cache Python...")
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            cache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(cache_path)
                print(f"✅ Removido: {cache_path}")
            except:
                pass
        
        for file in files:
            if file.endswith(".pyc"):
                try:
                    os.remove(os.path.join(root, file))
                except:
                    pass
    
    print("\n✨ Limpeza concluída!")

def selective_cleanup():
    """Limpeza seletiva"""
    print("\n🎯 LIMPEZA SELETIVA")
    print("=" * 60)
    print("O que você gostaria de limpar?")
    print("1. 🔥 TUDO (pastas geradas + cache)")
    print("2. 📁 Apenas biomas_tiles/")
    print("3. 🧪 Apenas pastas de teste")
    print("4. 🗑️  Apenas cache Python")
    print("5. ❌ Cancelar")
    
    choice = input("\nEscolha (1-5): ").strip()
    
    if choice == "1":
        cleanup()
    elif choice == "2":
        if os.path.exists("biomas_tiles"):
            shutil.rmtree("biomas_tiles")
            print("✅ biomas_tiles/ removida")
        else:
            print("ℹ️  biomas_tiles/ não existe")
    elif choice == "3":
        for folder in ["testes_rapidos", "teste_simples"]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"✅ {folder}/ removida")
    elif choice == "4":
        # Remove apenas cache
        for root, dirs, files in os.walk("."):
            if "__pycache__" in dirs:
                cache_path = os.path.join(root, "__pycache__")
                try:
                    shutil.rmtree(cache_path)
                    print(f"✅ Removido: {cache_path}")
                except:
                    pass
        print("✨ Cache limpo!")
    else:
        print("❌ Operação cancelada")

if __name__ == "__main__":
    selective_cleanup()