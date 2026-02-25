# 🌵 Mandacaru.AI

Um sistema inteligente de apoio à agricultura irrigada, combinando machine learning com uma interface web intuitiva para ajudar produtores rurais a otimizar o cultivo e irrigação.

## 📋 Sobre o Projeto

**Mandacaru.AI** é uma aplicação web que utiliza inteligência artificial para:
- 📊 Análise e diagnóstico do solo
- 🌧️ Previsão de chuva com NDVI (Índice de Vegetação por Diferença Normalizada)
- 🌾 Dashboard de monitoramento climático
- 🏠 Gerenciamento de propriedades rurais

## 🏗️ Arquitetura do Projeto

```
mandacaru.ai/
├── Backend/              # API FastAPI e autenticação
│   ├── main.py          # Servidor FastAPI com SQLite
│   └── requirements.txt
├── FrontEnd/            # Interface Streamlit
│   ├── app.py           # Aplicação principal
│   ├── tela_inicial.py
│   ├── tela_login.py
│   ├── tela_dashboard.py
│   ├── tela_clima.py
│   ├── tela_propriedade.py
│   ├── telaDiagnostico.py
│   └── TelaPrediçãoChuva.py
├── Modelos/             # Notebooks de machine learning
│   └── criaModel.ipynb
├── Dados/               # Datasets de exemplo
│   ├── dataCanudos.csv
│   ├── propriedades.csv
│   └── train.csv
└── requirements.txt     # Dependências gerais
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- pip ou conda

### Instalação

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd mandacaru.ai
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executar a Aplicação

#### Backend (API FastAPI)
```bash
cd Backend
python main.py
```
A API estará disponível em `http://localhost:8000`

#### Frontend (Streamlit)
```bash
cd FrontEnd
streamlit run app.py
```
A aplicação web abrirá em `http://localhost:8501`

## 📦 Dependências Principais

- **Streamlit** - Framework para interface web
- **FastAPI** - Framework para API REST
- **SQLAlchemy** - ORM para banco de dados
- **scikit-learn** - Machine Learning
- **pandas** - Manipulação de dados
- **plotly** - Visualizações interativas
- **passlib + argon2** - Hashing de senhas

Veja `requirements.txt` para a lista completa.

## 🔐 Autenticação

O sistema utiliza:
- **Hashing Argon2** para senhas
- **SQLite** como banco de dados local
- **FastAPI + Pydantic** para validação

## 📝 Licença

Projeto realizado durante um Hackathon na Universidade Federal de Sergipe

