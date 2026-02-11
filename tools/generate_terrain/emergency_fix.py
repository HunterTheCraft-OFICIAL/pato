# Arquivo 20: emergency_fix.py
import os
import sys

print("🚨 CORREÇÃO DE EMERGÊNCIA")
print("=" * 60)

# Verifica se numpy está instalado
try:
    import numpy
    print("✅ numpy OK")
except:
    print("❌ numpy não instalado")
    print("👉 Execute no terminal: pip install numpy")

# Verifica se PIL está instalado
try:
    from PIL import Image
    print("✅ PIL/Pillow OK")
except:
    print("❌ PIL/Pillow não instalado")
    print("👉 Execute no terminal: pip install Pillow")

# Cria versão de fallback se main.py não existir
if not os.path.exists("main.py"):
    print("\n⚠️  main.py não encontrado, criando versão básica...")
    with open("main.py", "w") as f:
        f.write('''
print("🌿 GERADOR DE BIOMAS - MODO DE EMERGÊNCIA")
print("Instale as dependências primeiro:")
print("pip install numpy Pillow")
''')

print("\n" + "=" * 60)
print("🎯 SE NADA FUNCIONAR, TENTE:")
print("1. pip install numpy Pillow")
print("2. python simple_test.py")
print("=" * 60)