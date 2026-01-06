"""
Exemplo de automação Python com Selenium
Conecta nos workers Docker via Selenium Remote
"""

import sys
import io

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
import random
import urllib.request
import urllib.error

def verificar_conexao(url="http://localhost:4444/wd/hub", timeout=5):
    """
    Verifica se o Selenium Hub está acessível
    
    Args:
        url: URL do hub
        timeout: Timeout em segundos
    """
    try:
        # Remove /wd/hub para verificar status
        status_url = url.replace('/wd/hub', '/status')
        req = urllib.request.Request(status_url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.getcode() == 200:
                print(f"✅ Selenium Hub está acessível em {status_url}")
                return True
            else:
                print(f"⚠️  Selenium Hub respondeu com status {response.getcode()}")
                return False
    except urllib.error.URLError as e:
        print(f"❌ Não foi possível conectar ao Selenium Hub: {e}")
        print("   Verifique se o Docker está rodando e os containers estão ativos")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar conexão: {e}")
        return False


def criar_driver(worker_url="http://localhost:4444/wd/hub"):
    """
    Cria um driver Selenium conectado ao worker Docker
    
    Args:
        worker_url: URL do Selenium Remote (Selenoid ou worker direto)
    """
    # Verifica conexão antes de tentar criar driver
    if not verificar_conexao(worker_url):
        raise ConnectionError("Não foi possível conectar ao Selenium Hub")
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-extensions')
    
    # Configurar capabilities do Selenoid para VNC
    # O Selenoid usa 'selenoid:options' para configurações específicas
    chrome_options.set_capability('selenoid:options', {
        'enableVNC': True,      # Habilita VNC para visualização em tempo real
        'enableVideo': False,    # Desabilita vídeo (pode habilitar se quiser gravar)
        'screenResolution': '1920x1080x24'
    })
    
    print(f"🔗 Conectando ao Selenium Hub: {worker_url}")
    print("   VNC habilitado - você pode visualizar a sessão no dashboard")
    try:
        driver = webdriver.Remote(
            command_executor=worker_url,
            options=chrome_options
        )
        
        driver.set_window_size(1920, 1080)
        print("✅ Driver criado com sucesso!")
        return driver
    except WebDriverException as e:
        print(f"❌ Erro ao criar driver: {e}")
        raise


def exemplo_automacao_simples():
    """Exemplo básico de automação"""
    print("🚀 Iniciando automação...")
    
    # Conecta no Selenoid (ou você pode usar worker direto: http://localhost:4444)
    driver = criar_driver("http://localhost:4444/wd/hub")
    
    try:
        # Navega para um site
        print("📍 Acessando site...")
        driver.get("https://www.google.com")
        
        # Aguarda carregar
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        # Digita algo
        print("⌨️  Digitando busca...")
        search_box.send_keys("Selenium Docker automation")
        time.sleep(1)
        
        # Submete
        search_box.submit()
        print("🔍 Busca realizada!")
        
        # Aguarda resultados (tenta encontrar qualquer elemento de resultado)
        try:
            # Tenta encontrar resultados de várias formas possíveis
            wait.until(EC.presence_of_element_located((By.ID, "search")))
            print("✅ Resultados carregados!")
        except TimeoutException:
            # Se não encontrar pelo ID, tenta por outros seletores
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#search, div[data-async-context]")))
                print("✅ Resultados carregados (método alternativo)!")
            except TimeoutException:
                # Se ainda não encontrar, apenas aguarda um tempo e continua
                print("⚠️  Aguardando carregamento da página...")
                time.sleep(2)
        
        # Simula navegação
        time.sleep(2)
        
        print("✨ Automação concluída com sucesso!")
        
    except TimeoutException as e:
        print(f"⏱️  Timeout na automação: {e}")
        print("   O elemento pode não ter carregado a tempo")
    except WebDriverException as e:
        print(f"❌ Erro do WebDriver: {e}")
        print("   Verifique se o Selenoid está rodando corretamente")
    except Exception as e:
        print(f"❌ Erro na automação: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        try:
            driver.quit()
            print("🏁 Driver encerrado")
        except Exception:
            print("⚠️  Erro ao encerrar driver (pode já estar fechado)")


def exemplo_automacao_worker_especifico(worker_id=1):
    """
    Conecta em um worker específico (útil para debug)
    
    Args:
        worker_id: ID do worker (1-4)
    """
    worker_ports = {
        1: 4444,  # chrome-worker-1
        2: 4444,  # chrome-worker-2
        3: 4444,  # chrome-worker-3
        4: 4444   # chrome-worker-4
    }
    
    # Para conectar direto no worker (sem Selenoid):
    # worker_url = f"http://localhost:{7900 + worker_id}/wd/hub"
    
    # Para usar Selenoid (recomendado):
    worker_url = "http://localhost:4444/wd/hub"
    
    print(f"🎯 Conectando no Worker {worker_id}...")
    driver = criar_driver(worker_url)
    
    try:
        driver.get("https://example.com")
        print(f"✅ Worker {worker_id} executando!")
        time.sleep(5)
        
    finally:
        driver.quit()


def exemplo_multiplas_automacoes():
    """Executa múltiplas automações em paralelo (use threading/multiprocessing)"""
    from concurrent.futures import ThreadPoolExecutor
    
    def tarefa(task_id):
        print(f"📌 Tarefa {task_id} iniciada")
        driver = criar_driver()
        try:
            driver.get(f"https://www.google.com/search?q=test+{task_id}")
            time.sleep(random.randint(3, 8))
            print(f"✅ Tarefa {task_id} concluída")
        finally:
            driver.quit()
    
    print("🚀 Executando 4 automações em paralelo...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(tarefa, range(1, 5))
    
    print("🏁 Todas as tarefas concluídas!")


if __name__ == "__main__":
    # Escolha qual exemplo executar:
    
    # 1. Automação simples
    exemplo_automacao_simples()
    
    # 2. Worker específico
    # exemplo_automacao_worker_especifico(worker_id=1)
    
    # 3. Múltiplas automações
    # exemplo_multiplas_automacoes()
