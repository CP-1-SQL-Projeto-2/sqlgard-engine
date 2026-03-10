# 🛡️ SQLgard Engine: O Despertar do Kernel Ancestral

Um projeto full-stack focado em integração de banco de dados, desenvolvido para processar a "física" e regras de negócio de um RPG diretamente no servidor de banco de dados Oracle.

## 📖 O Projeto
O mundo de SQLgard está sob ataque de uma névoa venenosa. Este sistema atua como o "Mestre do Jogo", onde a interface web exibe o status dos heróis e envia requisições para o banco de dados. O motor atômico (PL/SQL) no Oracle processa a passagem de tempo e a dedução de danos de todos os heróis simultaneamente.

## Integrantes
João Pedro Pereira Camilo | RM 562005
Pamella Christiny Chaves Brito | RM 565206

## 🛠️ Tecnologias Utilizadas
* **Frontend:** HTML5, CSS3 integrado com Jinja2.
* **Backend:** Python com o microframework Flask.
* **Banco de Dados:** Oracle SQL & PL/SQL.
* **Integração:** Biblioteca `python-oracledb`.
* **Deploy:** Vercel (Serverless).

## ⚙️ Arquitetura e Lógica de Negócio
A principal regra de negócio não reside no Python, mas sim no banco de dados. Quando o botão "Próximo Turno" é acionado:
1. O Flask envia uma instrução para o Oracle.
2. Um **Bloco Anônimo PL/SQL** é executado.
3. Um **Cursor (`FOR LOOP`)** varre a tabela selecionando apenas heróis com status `'ATIVO'`.
4. Variáveis locais calculam o dano da névoa.
5. Se o HP chega a zero, o status do herói é alterado automaticamente para `'CAÍDO'`.

## 🚀 Como testar localmente
1. Clone o repositório.
2. Crie um ambiente virtual e instale as dependências: `pip install -r requirements.txt`
3. Configure suas variáveis de ambiente: `DB_USER`, `DB_PASSWORD`, `DB_DSN`.
4. Rode a aplicação: `python app.py`