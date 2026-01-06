"""
Script para obter informações das sessões ativas do Selenoid
e suas URLs VNC
"""

import urllib.request
import json
import sys

def obter_sessoes_ativas():
    """Obtém lista de sessões ativas do Selenoid"""
    try:
        # Buscar status do Selenoid
        req = urllib.request.Request('http://localhost:4444/status')
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            print("=" * 60)
            print("SESSOES ATIVAS NO SELENOID")
            print("=" * 60)
            
            if 'sessions' in data and data['sessions']:
                print(f"\nTotal de sessões ativas: {len(data['sessions'])}")
                print("\nDetalhes das sessões:")
                print("-" * 60)
                
                for i, session in enumerate(data['sessions'], 1):
                    session_id = session.get('id', 'N/A')
                    browser = session.get('browser', 'N/A')
                    version = session.get('version', 'N/A')
                    
                    print(f"\nSessão {i}:")
                    print(f"  ID: {session_id}")
                    print(f"  Browser: {browser} {version}")
                    
                    # Tentar obter informações do container
                    try:
                        # O Selenoid expõe VNC através do container
                        # A URL geralmente é acessível via Selenoid UI
                        vnc_url = f"http://localhost:8080/#/sessions/{session_id}"
                        print(f"  VNC URL: {vnc_url}")
                        print(f"  Selenoid UI: http://localhost:8080")
                    except Exception as e:
                        print(f"  Erro ao obter URL VNC: {e}")
                
                print("\n" + "=" * 60)
                print("Para visualizar no dashboard:")
                print("1. Acesse http://localhost:8888")
                print("2. Ou acesse http://localhost:8080 (Selenoid UI)")
                print("=" * 60)
                
            else:
                print("\nNenhuma sessão ativa no momento.")
                print("Execute o script de automação para criar uma sessão.")
            
            return data.get('sessions', [])
            
    except Exception as e:
        print(f"Erro ao obter sessões: {e}")
        return []


if __name__ == "__main__":
    obter_sessoes_ativas()

