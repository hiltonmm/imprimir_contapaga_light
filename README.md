# ⚡ Automação de Faturas Light (RPA)

Este projeto foi desenvolvido com o objetivo de **facilitar e acelerar a rotina administrativa** de pessoas e empresas que precisam lidar mensalmente com o download, a organização e a impressão de múltiplas faturas de energia da concessionária Light. 

Através de um robô de automação (RPA) construído em Python, o sistema acessa a Agência Virtual da Light, supera a lentidão nativa do portal, extrai os PDFs e os envia automaticamente para a impressora padrão do computador, eliminando horas de trabalho manual, cliques repetitivos e tempo de espera.

## ✨ Principais Funcionalidades

* **Execução "Plug and Play":** Scripts `.bat` inclusos para instalação de dependências e execução do robô com apenas dois cliques.
* **Interface Gráfica (UI):** Permite ao usuário selecionar rapidamente os meses e anos de referência antes de iniciar a extração.
* **Processamento em Lote (JSON):** Suporte para rodar dezenas de códigos de instalação diferentes de uma só vez, centralizados em um arquivo de configuração simples.
* **Download Silencioso e Controle de Abas:** Burla o visualizador nativo de PDF do navegador, forçando o download em segundo plano e lidando perfeitamente com "abas fantasmas".
* **Resiliência e Retentativas:** O robô identifica falhas de carregamento do portal (comuns em sistemas ASP.NET) e oferece a opção de tentar baixar apenas as faturas que falharam.
* **Impressão Automática:** Integração direta com o Spooler do Windows, enviando o lote de PDFs baixados para a impressora configurada no sistema.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Selenium WebDriver** (Navegação assíncrona e injeção de JavaScript)
* **Webdriver Manager** (Gerenciamento automático do ChromeDriver)
* **Tkinter** (Interface de usuário nativa)
* **Dotenv** (Segurança e gestão de credenciais)

---

## ⚙️ Configuração e Instalação

O projeto foi estruturado para ser configurado facilmente no Windows.

### 1. Preparando o ambiente
1. Clone este repositório ou baixe o arquivo `.zip` e extraia em uma pasta no seu computador.
2. Dê um duplo clique no arquivo **`install.bat`**.
   * *O script criará o ambiente virtual, instalará todas as bibliotecas necessárias e gerará um arquivo `.env` automaticamente.*

### 2. Configurando suas Credenciais
Abra o arquivo recém-criado chamado `.env` (na raiz do projeto) com o Bloco de Notas ou seu editor de código preferido e insira seus dados de acesso da Light:
```env
LOGIN_LIGHT=seu_cpf_ou_email_aqui
SENHA_LIGHT=sua_senha_aqui
```
### 3. Como configurar Múltiplas Instalações (O arquivo JSON)
A grande vantagem deste robô é buscar dezenas de contas de uma vez. Para isso, você deve listar os códigos das unidades consumidoras no arquivo instalacoes.json.

Abra o arquivo e adicione as instalações dentro dos colchetes [ ], separadas por vírgula.
Atenção: É obrigatório manter os códigos entre aspas duplas " " para que o sistema não corte os zeros à esquerda.

Exemplo de configuração:
```
JSON
{
  "instalacoes": [
    "0412980302",
    "0413053377",
    "0413219107",
    "0420060631"
  ]
}
```

## 🚀 Como Usar no Dia a Dia
Após a instalação e configuração inicial, a execução é extremamente simples:

Dê um duplo clique no arquivo run.bat.

A interface gráfica abrirá. Selecione o(s) mês(es) e ano(s) de referência que deseja baixar e clique em "Adicionar".

Clique em "Iniciar Automação".

Tire as mãos do teclado e do mouse. O navegador abrirá de forma automatizada e o console informará o andamento de cada instalação e mês.

Ao final, caso ocorram falhas devido à lentidão do site, o sistema perguntará se você deseja tentar novamente apenas os erros.

Uma última janela perguntará se você deseja imprimir as faturas. Clicando em "Sim", os arquivos serão enviados para a sua impressora padrão.

## 📂 Estrutura de Arquivos
run.bat / install.bat: Scripts de facilitação para Windows.

main.py: Orquestrador principal.

faturas_light.py: Motor de extração e navegação do portal.

interface.py: Código da interface de seleção de meses.

instalacoes.json: Seu banco de dados local com as instalações.

## ⚠️ Avisos Legais e Isenção de Responsabilidade

Este script foi desenvolvido exclusivamente para otimização de rotinas administrativas próprias e não possui nenhum tipo de vínculo, afiliação ou endosso com a concessionária Light. 

* **Uso Livre:** O uso deste programa é totalmente livre e gratuito para execução, distribuição ou adaptação de rotinas próprias.
* **Homologação:** O sistema foi testado e homologado para a versão atual do portal `light.com.br` na data de **07/07/2026**.
* **Instabilidade de Web Scraping:** O funcionamento deste robô depende diretamente da estrutura atual do código fonte (HTML/Classes) da Agência Virtual da Light. Qualquer atualização, mudança de layout ou alteração nos sistemas da concessionária pode fazer com que o programa deixe de funcionar completamente.
* **Isenção de Responsabilidade:** O autor **não se responsabiliza** por qualquer mau funcionamento, travamentos, falhas de download, bloqueios de acesso ou qualquer outro problema direto ou indireto decorrente do uso deste script. 
* **Uso por Conta e Risco:** O uso desta ferramenta é inteiramente por sua conta e risco, e não há nenhuma garantia de manutenção, suporte ou funcionamento futuro.