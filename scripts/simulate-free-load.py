#!/usr/bin/env python3
"""
🆓 Simulador de Carga para AWS Free Tier
Autor: Richard Chamorro - FinOps Latam
Descripción: Simula carga de trabajo realista SIN exceder los límites gratuitos de AWS
"""

import time
import random
import requests
import boto3
from datetime import datetime
import json

class FreeTierSimulator:
    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.s3_client = boto3.client('s3')
        self.cloudwatch = boto3.client('cloudwatch')
        
    def print_header(self):
        print("🚀" * 50)
        print("🆓 FINOPS AWS - SIMULADOR FREE TIER")
        print("💰 Costo: $0.00 - Totalmente gratuito")
        print("📊 Simulando carga realista para demostración")
        print("🚀" * 50)
        print()

    def simulate_ec2_cpu_load(self, duration_minutes=10):
        """Simula carga de CPU moderada en EC2"""
        print("🖥️  Iniciando simulación de carga EC2...")
        print("   📏 Límite Free Tier: 750 horas/mes")
        print("   🎯 Objetivo: 40-60% CPU (óptimo para demo)")
        print()
        
        for minute in range(1, duration_minutes + 1):
            # Simular carga variable pero controlada
            cpu_load = random.randint(35, 65)
            
            # Patrón realista: más carga en "horario laboral"
            current_hour = datetime.now().hour
            if 9 <= current_hour <= 17:  # Horario laboral
                cpu_load = min(cpu_load + 10, 70)  # Un poco más de carga
            
            # Emitir métrica personalizada a CloudWatch (gratuita)
            try:
                self.cloudwatch.put_metric_data(
                    Namespace='FinOps/Demo',
                    MetricData=[
                        {
                            'MetricName': 'SimulatedCPULoad',
                            'Value': cpu_load,
                            'Unit': 'Percent',
                            'Dimensions': [
                                {
                                    'Name': 'InstanceType',
                                    'Value': 't2.micro'
                                },
                                {
                                    'Name': 'Simulation',
                                    'Value': 'FreeTierDemo'
                                }
                            ]
                        },
                    ]
                )
            except Exception as e:
                print(f"   ⚠️  Nota: No se pudo enviar métrica: {e}")
            
            # Visualización en consola
            load_bar = "█" * (cpu_load // 5) + "░" * (20 - (cpu_load // 5))
            print(f"   Minuto {minute:2d}: CPU [{load_bar}] {cpu_load}%")
            
            time.sleep(60)  # Esperar 1 minuto entre mediciones
        
        print("✅ Simulación EC2 completada\n")

    def simulate_s3_operations(self, bucket_name):
        """Simula operaciones S3 dentro de límites free tier"""
        print("💾 Simulando operaciones S3...")
        print("   📏 Límite Free Tier: 5GB almacenamiento")
        print("   🎯 Objetivo: Operaciones básicas de demo")
        print()
        
        operations = [
            {"type": "PUT", "size_kb": 50, "desc": "Subir archivo pequeño"},
            {"type": "GET", "size_kb": 50, "desc": "Descargar archivo"},
            {"type": "LIST", "size_kb": 0, "desc": "Listar buckets"},
            {"type": "PUT", "size_kb": 100, "desc": "Subir archivo mediano"},
            {"type": "GET", "size_kb": 100, "desc": "Descargar archivo"}
        ]
        
        for i, op in enumerate(operations, 1):
            print(f"   Operación {i}: {op['type']} - {op['desc']}")
            
            # Simular tiempo de operación
            time.sleep(2)
            
            # Aquí iría el código real para operaciones S3
            # Pero para demo, solo simulamos
            if op['type'] == "PUT":
                print(f"      📤 Subiendo {op['size_kb']}KB...")
            elif op['type'] == "GET":
                print(f"      📥 Descargando {op['size_kb']}KB...")
            elif op['type'] == "LIST":
                print("      📋 Listando contenido...")
            
            time.sleep(1)
        
        print("✅ Operaciones S3 simuladas\n")

    def simulate_lambda_invocations(self):
        """Simula invocaciones de Lambda dentro de free tier"""
        print("⚡ Simulando invocaciones Lambda...")
        print("   📏 Límite Free Tier: 1M requests/mes")
        print("   🎯 Objetivo: 10-20 invocaciones de demo")
        print()
        
        for i in range(1, 6):  # Solo 5 invocaciones para demo
            print(f"   Invocación {i}: Procesando datos demo...")
            
            # Simular procesamiento Lambda
            processing_time = random.uniform(0.1, 0.5)
            time.sleep(processing_time)
            
            print(f"      ✅ Procesado en {processing_time:.2f}s")
        
        print("✅ Invocaciones Lambda simuladas\n")

    def show_cost_simulation(self):
        """Muestra simulación de ahorros de costos"""
        print("💰 SIMULACIÓN DE AHORROS DE COSTOS")
        print("=" * 50)
        
        # Datos de simulación
        scenarios = [
            {"service": "EC2 t2.micro", "current": 8.50, "optimized": 5.10, "saving": 40},
            {"service": "S3 5GB", "current": 0.12, "optimized": 0.07, "saving": 42},
            {"service": "Lambda 100K", "current": 0.20, "optimized": 0.10, "saving": 50},
            {"service": "Data Transfer", "current": 1.50, "optimized": 0.75, "saving": 50}
        ]
        
        total_current = sum(scenario["current"] for scenario in scenarios)
        total_optimized = sum(scenario["optimized"] for scenario in scenarios)
        total_saving = ((total_current - total_optimized) / total_current) * 100
        
        for scenario in scenarios:
            print(f"   {scenario['service']}:")
            print(f"      Actual: ${scenario['current']:.2f} → Optimizado: ${scenario['optimized']:.2f}")
            print(f"      Ahorro: {scenario['saving']}%")
            print()
        
        print(f"   💵 TOTAL MENSUAL:")
        print(f"      Actual: ${total_current:.2f} → Optimizado: ${total_optimized:.2f}")
        print(f"      AHORRO POTENCIAL: {total_saving:.1f}% (${total_current - total_optimized:.2f}/mes)")
        print()

    def run_complete_simulation(self):
        """Ejecuta la simulación completa"""
        self.print_header()
        
        # Simulaciones individuales
        self.simulate_ec2_cpu_load(duration_minutes=5)  # Más corto para demo
        self.simulate_s3_operations("finops-demo-bucket")
        self.simulate_lambda_invocations()
        
        # Resultados y recomendaciones
        self.show_cost_simulation()
        
        print("🎉 SIMULACIÓN COMPLETADA EXITOSAMENTE")
        print("📊 Los datos de muestra están listos para tu dashboard CloudWatch")
        print("👨💼 Perfecto para demostraciones a clientes")

def main():
    """Función principal"""
    try:
        simulator = FreeTierSimulator()
        simulator.run_complete_simulation()
    except KeyboardInterrupt:
        print("\n⏹️  Simulación interrumpida por el usuario")
    except Exception as e:
        print(f"❌ Error durante la simulación: {e}")
        print("💡 Asegúrate de tener configuradas las credenciales de AWS")

if __name__ == "__main__":
    main()