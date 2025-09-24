#!/usr/bin/env python3
"""
Script para ejecutar pruebas automáticas del sistema de autenticación
"""
import subprocess
import sys
import os
import time

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*50}")
    print(f"🔄 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("📋 SALIDA:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️  ERRORES:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - EXITOSO")
        else:
            print(f"❌ {description} - FALLÓ (código: {result.returncode})")
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def main():
    print("🚀 INICIANDO PRUEBAS AUTOMÁTICAS DEL SISTEMA DE AUTENTICACIÓN")
    
    # Cambiar al directorio de pruebas
    os.chdir('tests')
    
    # Instalar dependencias de pruebas
    success = run_command(
        "pip install -r requirements.txt",
        "Instalando dependencias de pruebas"
    )
    
    if not success:
        print("❌ No se pudieron instalar las dependencias")
        return 1
    
    # Ejecutar pruebas unitarias
    success_unit = run_command(
        "python -m pytest test_unit.py -v --tb=short",
        "Ejecutando pruebas unitarias"
    )
    
    # Ejecutar pruebas de integración
    print("\n⏳ Esperando 5 segundos para que los servicios estén listos...")
    time.sleep(5)
    
    success_integration = run_command(
        "python -m pytest test_integration.py -v --tb=short",
        "Ejecutando pruebas de integración"
    )
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE PRUEBAS")
    print(f"{'='*60}")
    print(f"Pruebas Unitarias: {'✅ PASARON' if success_unit else '❌ FALLARON'}")
    print(f"Pruebas de Integración: {'✅ PASARON' if success_integration else '❌ FALLARON'}")
    
    if success_unit and success_integration:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        return 0
    else:
        print("\n⚠️  ALGUNAS PRUEBAS FALLARON")
        return 1

if __name__ == "__main__":
    sys.exit(main())