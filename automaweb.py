"""
biblioteca destinada à automatização de tarefas na web
bem como interações com o gerenciamento de arquivos no computador
"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


class AutomacaoWeb:

    '''
    Explicações...
    '''

    def __init__(self, headless=False):
        
        #inicializa o driver e configura as opções do navegador.
        edge_options = Options()
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)
        
        #se headless for verdadeiro, configura o driver para rodar em modo headless
        if headless:
            edge_options.add_argument("--headless=new") 
        self.driver = webdriver.Edge(options=edge_options)
        
        #configura o tamanho da janela para headless
        if headless:
            #em headless, é bom definir um tamanho fixo para evitar que o site carregue em formato mobile (800x600)
            self.driver.set_window_size(1920, 1080)
        else:
            #se tiver interface, maximiza normal
            self.driver.maximize_window()
        
        self.driver = webdriver.Edge()
        self.timeout = 10 #define tempo de espera padrão



### NAVEGAÇÕES DENTRO DO DRIVER

    def abrir_url(self, url):
        
        #carrega uma página web.
        self.driver.get(url)
    
    def abrir_nova_aba(self, url):
        
        #abre uma nova aba e foca nela automaticamente.
        try:
            # 'tab' abre uma aba. 'window' abriria uma nova janela separada.
            self.driver.switch_to.new_window('tab') 
            self.driver.get(url)
        except Exception as e:
            print(f"Erro ao abrir nova aba: {e}")
    
    def alternar_aba(self, indice):
        #muda o foco para a aba especificada pelo índice (0 é a primeira, 1 é a segunda...).
        try:
            abas = self.driver.window_handles
            self.driver.switch_to.window(abas[indice])
        except Exception as e:
            print(f"Erro ao mudar para a aba {indice}: {e}")
        
    def fechar_aba_atual(self):
    
        #fecha a aba atual e volta o foco para a aba anterior (se houver).    
        try:
            # .close() fecha SÓ a aba atual (diferente de .quit() que fecha tudo)
            self.driver.close()
            
            #boa prática: voltar o foco para a última aba aberta para não ficar "sem foco"
            if len(self.driver.window_handles) > 0:
                self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as e:
            print(f"Erro ao fechar aba: {e}")

    def fechar_navegador(self):
        
        #fecha o navegador e encerra a sessão do driver.
        self.driver.quit()



### INTERAÇÕES COM A PÁGINA

    def clicar(self, xpath):
    
        #clica em um elemento identificado pelo xpath.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elemento.click()
        except Exception as e:
            print(f"Erro ao clicar no elemento {xpath}: {e}")

    def digitar(self, xpath, texto):
        
        #digita um texto em um elemento identificado pelo xpath.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elemento.clear()
            elemento.send_keys(texto)
        except Exception as e:
            print(f"Erro ao digitar no elemento {xpath}: {e}")
    
    def passar_mouse(self, xpath):
        
        #simula a ação de mover o cursor do mouse sobre o elemento (Hover).
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            actions = ActionChains(self.driver)
            actions.move_to_element(elemento).perform()
        except Exception as e:
            print(f"Erro ao passar mouse sobre {xpath}: {e}")
    
    def selecionar_texto(self, xpath, texto):

        #seleciona um texto dentro de um elemento.
        try:
            Select(WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))).select_by_visible_text(texto)
        except Exception as e:
            print(f"Erro ao selecionar {texto} no elemento {xpath}: {e}")

    def selecionar_valor(self, xpath, valor):

        #seleciona um valor dentro de um elemento.
        try:
            Select(WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))).select_by_value(valor)
        except Exception as e:
            print(f"Erro ao selecionar {valor} no elemento {xpath}: {e}")

    def limpar(self, xpath):

        #limpa o conteúdo de um elemento de entrada.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath))); elemento.clear()
        except Exception as e:
            print(f"Erro ao limpar o conteúdo do elemento {xpath}: {e}")
    
    def obter_texto(self, xpath):

        #obtém o texto de um elemento.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.text
        except Exception as e:
            print(f"Erro ao obter o texto do elemento {xpath}: {e}")
    
    def obter_atributo(self, xpath, atributo):

        #obtém o atributo de um elemento.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.get_attribute(atributo)
        except Exception as e:
            print(f"Erro ao obter o atributo do elemento {xpath}: {e}")
    
    def rolar_ate_elemento(self, xpath):
        
        #rola a tela até que o elemento específico esteja visível.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        except Exception as e:
            print(f"Erro ao rolar até o elemento {xpath}: {e}")
    
    def aguardar_elemento_sumir(self, xpath):
        
        #aguarda até que o elemento não esteja mais visível.
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            print(f"Erro ou timeout ao aguardar elemento sumir {xpath}: {e}")
    
    def encontrar_elementos(self, xpath):
        
        #retorna uma lista com todos os elementos identificados pelo xpath.
        try:
            return self.driver.find_elements(By.XPATH, xpath)
        except Exception as e:
            print(f"Erro ao encontrar elementos {xpath}: {e}")

    def tirar_screenshot(self, nome_arquivo):
        
        #salva uma imagem da tela atual.
        try:
            self.driver.save_screenshot(f"{nome_arquivo}.png")
        except Exception as e:
            print(f"Erro ao salvar screenshot: {e}")
    
    def entrar_iframe(self, xpath):
        
        #muda o foco do driver para dentro de um iframe.
        try:
            WebDriverWait(self.driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))
        except Exception as e:
            print(f"Erro ao entrar no iframe {xpath}: {e}")

    def sair_iframe(self):
        
        # Volta o foco para a página principal.
        self.driver.switch_to.default_content()



### VERIFICAÇÕES

    def verifica_selecao(self, xpath, timeout=None):

        #como não dá pra passar o self.timeout no argumento da função,
        #tem-se que passar como None e definir o timeout dentro da função.
        #se não for seleiconado um valor pro timeout ele usa o self.timeout.
        if timeout is None:
            timeout = self.timeout

        #verifica se um elemento (como checkbox) está selecionado.
        try:
            elemento = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.is_selected()
        except Exception as e:
            print(f"Erro ao obter o texto do elemento {xpath}: {e}")
    
    def verifica_habilitado(self, xpath, timeout=None):
 
        #como não dá pra passar o self.timeout no argumento da função,
        #tem-se que passar como None e definir o timeout dentro da função.
        #se não for seleiconado um valor pro timeout ele usa o self.timeout.
        if timeout is None:
            timeout = self.timeout

        #verifica se um elemento está habilitado
        try:
            elemento = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.is_enabled()
        except Exception as e:
            print(f"Erro ao obter o texto do elemento {xpath}: {e}")

    def verifica_clicavel(self, xpath, timeout=None):
    
        #como não dá pra passar o self.timeout no argumento da função,
        #tem-se que passar como None e definir o timeout dentro da função.
        #se não for seleiconado um valor pro timeout ele usa o self.timeout.
        if timeout is None:
            timeout = self.timeout

        #verifica se o elemento está visível E habilitado para clique.
        try:
            #o wait.until vai esperar até que o elemento seja clicável ou o tempo esgote
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            return True
        except TimeoutException:
            #se o tempo (10s) passar e não ficar clicável, retorna False
            return False
        except Exception as e:
            print(f"Erro ao verificar clicabilidade de {xpath}: {e}")
            return False
    
    def verifica_existe(self, xpath):

        #como não dá pra passar o self.timeout no argumento da função,
        #tem-se que passar como None e definir o timeout dentro da função.
        #se não for seleiconado um valor pro timeout ele usa o self.timeout.
        if timeout is None:
            timeout = self.timeout

        #verifica se um elemento existe na página (Retorna True ou False).
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False
        except Exception as e:
            print(f"Erro inesperado ao verificar elemento {xpath}: {e}")
            return False

import os
import shutil
import time # Útil para aguardar downloads antes de mover
from datetime import datetime

class FileExplorer:
    
    '''
    Classe destinada à manipulação de arquivos e pastas no sistema operacional.
    '''

    def __init__(self):
        
        #inicializador simples, pode ser expandido se necessário manter estados (ex: pasta padrão)
        pass

### MANIPULAÇÃO DE ARQUIVOS

    def renomear_arquivo(self, caminho_atual, novo_nome):
        
        #renomeia um arquivo mantendo-o na mesma pasta.
        #'caminho_atual' deve ser o path completo.
        #'novo_nome' deve ser apenas o nome do arquivo com extensão (ex: "relatorio_final.pdf").
        try:
            diretorio = os.path.dirname(caminho_atual)
            novo_caminho = os.path.join(diretorio, novo_nome)
            
            os.rename(caminho_atual, novo_caminho)
            print(f"Arquivo renomeado para: {novo_nome}")
            return novo_caminho # Retorna o novo path para uso futuro
        except Exception as e:
            print(f"Erro ao renomear arquivo {caminho_atual}: {e}")

    def mover_arquivo(self, origem, destino):
        
        #move um arquivo de 'origem' para 'destino'.
        #o destino pode ser uma pasta ou um novo caminho completo de arquivo.
        try:
            shutil.move(origem, destino)
            print(f"Arquivo movido de {origem} para {destino}")
        except Exception as e:
            print(f"Erro ao mover arquivo: {e}")

    def copiar_arquivo(self, origem, destino):
        
        #copia um arquivo mantendo os metadados (datas de criação, etc).
        try:
            shutil.copy2(origem, destino)
            print(f"Arquivo copiado para {destino}")
        except Exception as e:
            print(f"Erro ao copiar arquivo: {e}")

    def excluir_arquivo(self, caminho):
        
        #remove um arquivo permanentemente.
        try:
            if os.path.exists(caminho):
                os.remove(caminho)
                print(f"Arquivo excluído: {caminho}")
            else:
                print(f"Arquivo não encontrado para exclusão: {caminho}")
        except Exception as e:
            print(f"Erro ao excluir arquivo: {e}")

### GERENCIAMENTO DE PASTAS

    def criar_pasta(self, caminho_pasta):
        
        #cria uma pasta (e subpastas se necessário). 
        #exist_ok=True evita erro se a pasta já existir.
        try:
            os.makedirs(caminho_pasta, exist_ok=True)
            print(f"Pasta garantida: {caminho_pasta}")
        except Exception as e:
            print(f"Erro ao criar pasta: {e}")

    def listar_arquivos(self, diretorio, extensao=None):
        
        #retorna uma lista com os nomes dos arquivos no diretório.
        #se 'extensao' for informado (ex: '.pdf'), filtra a lista.
        try:
            arquivos = os.listdir(diretorio)
            if extensao:
                arquivos = [f for f in arquivos if f.endswith(extensao)]
            return arquivos
        except Exception as e:
            print(f"Erro ao listar arquivos em {diretorio}: {e}")
            return []

### UTILITÁRIOS E VERIFICAÇÕES

    def verifica_existe(self, caminho):
        
        #verifica se um arquivo ou pasta existe.
        return os.path.exists(caminho)

    def obter_arquivo_mais_recente(self, diretorio, extensao=None):

        #útil para pegar o último arquivo baixado na pasta de Downloads.
        try:
            arquivos = self.listar_arquivos(diretorio, extensao)
            if not arquivos:
                return None
            
            #reconstrói os caminhos completos
            caminhos_completos = [os.path.join(diretorio, f) for f in arquivos]
            
            #retorna o arquivo com a data de modificação mais recente
            arquivo_recente = max(caminhos_completos, key=os.path.getmtime)
            return arquivo_recente
        except Exception as e:
            print(f"Erro ao buscar arquivo recente: {e}")
            return None