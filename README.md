# Projeto: Dashboard de Análise de Dados de Visualização (AV3)

Este projeto tem como objetivo criar um **dashboard interativo** utilizando **Streamlit** para analisar dados de visualização e acessos. O dashboard apresenta diversas análises, como:
- Total de horas assistidas.
- Acessos por tipo de título.
- Acessos por mês, dia e hora.
- Acessos por dia da semana (em português).

## Estrutura do Projeto

```plaintext
.
├── app.py                # Script principal do dashboard
├── data_processing.py    # Script para tratamento e processamento dos dados
├── data/
│   ├── raw/              # Diretório com os arquivos de dados brutos
│   └── processed/        # Diretório onde os arquivos processados serão salvos
├── requirements.txt      # Arquivo com as dependências do projeto
└── README.md             # Documentação do projeto
```

### Descrição dos Arquivos

1. **`app.py`**: Script principal do projeto. Executa o dashboard utilizando a biblioteca **Streamlit**.
2. **`data_processing.py`**: Script que processa os dados brutos do diretório `data/raw` e gera arquivos tratados no diretório `data/processed`.
3. **`data/raw/`**: Diretório onde devem ser colocados os arquivos brutos de entrada.
4. **`data/processed/`**: Diretório onde serão salvos os arquivos processados gerados pelo `data_processing.py`.
5. **`requirements.txt`**: Lista de dependências necessárias para o projeto.
6. **`README.md`**: Este arquivo, que explica como configurar, executar e utilizar o projeto.

---

## Preparação do Ambiente Virtual e Instalação das Dependências

1. **Criar o ambiente virtual**:
   ```bash
   python -m venv venv

2. **Ativar o ambiente virtual**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

3. **Instalar as dependências**:
   ```bash
   pip install -r requirements.txt

## Executando o Projeto

### 1. Processar os Dados

Certifique-se de que os arquivos brutos estejam no diretório `data/raw`. Execute o script `data_processing.py` para processar os dados:

```bash
python data_processing.py
```

Após a execução, os arquivos processados serão salvos em data/processed.

### 2. Rodar o Dashboard

Execute o script `app.py` para iniciar o dashboard:

```bash
streamlit run app.py
```

Abra o link gerado (geralmente http://localhost:8501) no navegador para acessar o dashboard.

## Funcionalidades do Dashboard

### **1. Visão Geral**
- Total de horas assistidas.
- Média de horas assistidas.
- Quantidade de títulos assistidos.
- Comparação de acessos por tipo de título e entre anos.

### **2. Detalhamento por Título**
- Total de acessos por título.
- Total de horas assistidas por título.
- Seleção de um título específico para análise detalhada.

### **3. Análise Temporal**
- Acessos por mês (gráfico de barras).
- Acessos por dia (gráfico de barras).
- Acessos por dia da semana (gráfico de barras em português).
- Acessos por hora (gráfico de barras).

---

## Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`. Certifique-se de instalá-las no ambiente virtual para garantir o funcionamento correto.

---

### Observação

Caso encontre problemas, certifique-se de que os arquivos de dados (`data/raw/`) estão no formato esperado e que o Python está atualizado para a versão 3.12 ou superior.

---

