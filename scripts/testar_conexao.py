"""
Script para testar a conexão com o Selenium Hub/Selenoid
Use este script para diagnosticar problemas de conexão
"""

import urllib.request
import urllib.error
import sys

def testar_selenoid():
    """Testa a conexão com o Selenoid"""
    print("[*] Testando conexao com Selenoid...")
    
    urls = [
        "http://localhost:4444/status",
        "http://localhost:4444/wd/hub/status",
        "http://127.0.0.1:4444/status"
    ]
    
    for url in urls:
        try:
            print(f"\n[*] Tentando conectar em: {url}")
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                status_code = response.getcode()
                if status_code == 200:
                    print(f"[OK] Sucesso! Status: {status_code}")
                    data = response.read().decode('utf-8')
                    print(f"     Resposta: {data[:200]}...")
                    return True
                else:
                    print(f"[!] Status: {status_code}")
        except urllib.error.URLError as e:
            print(f"[ERRO] Erro: {e}")
        except Exception as e:
            print(f"[ERRO] Erro inesperado: {e}")
    
    print("\n[ERRO] Nao foi possivel conectar ao Selenoid")
    print("\n[DICA] Verificacoes:")
    print("   1. Verifique se o Docker esta rodando")
    print("   2. Execute: docker ps (deve mostrar o container 'selenoid')")
    print("   3. Execute: docker logs selenoid (para ver erros)")
    print("   4. Verifique se a porta 4444 esta livre")
    return False


def verificar_containers():
    """Verifica se os containers necessários estão rodando"""
    import subprocess
    
    print("\n[*] Verificando containers Docker...")
    
    containers_necessarios = ['selenoid', 'selenoid-ui']
    
    try:
        result = subprocess.run(
            ['docker', 'ps', '--format', '{{.Names}}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        containers_rodando = result.stdout.strip().split('\n')
        containers_rodando = [c for c in containers_rodando if c]
        
        print(f"     Containers rodando: {len(containers_rodando)}")
        
        for container in containers_necessarios:
            if container in containers_rodando:
                print(f"     [OK] {container} esta rodando")
            else:
                print(f"     [ERRO] {container} NAO esta rodando")
                print(f"            Execute: docker compose up -d {container}")
        
        return all(c in containers_rodando for c in containers_necessarios)
        
    except FileNotFoundError:
        print("[ERRO] Docker nao encontrado. Instale o Docker Desktop")
        return False
    except Exception as e:
        print(f"[ERRO] Erro ao verificar containers: {e}")
        return False


if __name__ == "__main__":
    import sys
    import io
    # Configurar encoding UTF-8 para Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 60)
    print("TESTE DE CONEXAO SELENOID")
    print("=" * 60)
    
    containers_ok = verificar_containers()
    conexao_ok = testar_selenoid()
    
    print("\n" + "=" * 60)
    if containers_ok and conexao_ok:
        print("[OK] Tudo funcionando! Voce pode executar o script de automacao.")
        sys.exit(0)
    else:
        print("[ERRO] Problemas detectados. Verifique as mensagens acima.")
        sys.exit(1)

