import os
import oracledb
import json
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)

# Lógica de conexão com o banco
def get_db_connection():
    try:
        with open("secret.txt", "r", encoding="utf-8") as f:
            creds = json.load(f)
        return oracledb.connect(user=creds["user"], password=creds["password"], dsn=creds["dsn"])
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

# Template HTML com a interface do jogo e os dois botões
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SQLgard - O Despertar do Kernel</title>
    <style>
        body { font-family: sans-serif; background-color: #1e1e1e; color: #fff; text-align: center; padding: 50px; }
        table { margin: 0 auto; border-collapse: collapse; width: 60%; background-color: #2d2d2d; box-shadow: 0 4px 8px rgba(0,0,0,0.5); }
        th, td { padding: 15px; border: 1px solid #444; }
        th { background-color: #333; }
        
        /* Estilos dos Botões */
        .btn { padding: 15px 30px; text-decoration: none; font-size: 18px; border-radius: 5px; border: none; cursor: pointer; transition: 0.3s; font-weight: bold; }
        .btn-dano { background-color: #8b0000; color: white; }
        .btn-dano:hover { background-color: #ff0000; transform: scale(1.05); }
        .btn-cura { background-color: #228B22; color: white; }
        .btn-cura:hover { background-color: #32CD32; transform: scale(1.05); }
        
        /* Estilos de Status */
        .caido { color: #ff4c4c; font-weight: bold; }
        .ativo { color: #4cff4c; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🛡️ Status dos Heróis em SQLgard</h1>
    
    <table>
        <tr><th>ID</th><th>Nome</th><th>Classe</th><th>HP</th><th>Status</th></tr>
        {% for heroi in herois %}
        <tr>
            <td>{{ heroi[0] }}</td>
            <td>{{ heroi[1] }}</td>
            <td>{{ heroi[2] }}</td>
            <td>{{ heroi[3] }} / {{ heroi[4] }}</td>
            <td class="{{ 'ativo' if heroi[5] == 'ATIVO' else 'caido' }}">{{ heroi[5] }}</td>
        </tr>
        {% endfor %}
    </table>
    
    <div style="margin-top: 30px;">
        <form action="/processar" method="POST" style="display: inline-block; margin-right: 15px;">
            <button type="submit" class="btn btn-dano">Processar Próximo Turno da Névoa ☠️</button>
        </form>
        
        <form action="/resetar" method="POST" style="display: inline-block;">
            <button type="submit" class="btn btn-cura">Restaurar Heróis ♻️</button>
        </form>
    </div>
</body>
</html>
"""

# Rota principal: Exibe a tabela
@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        return "<h1>Erro de conexão!</h1><p>Verifique as variáveis de ambiente (DB_USER, DB_PASSWORD, DB_DSN).</p>"
    
    cursor = conn.cursor()
    cursor.execute("SELECT id_heroi, nome, classe, hp_atual, hp_max, status FROM TB_HEROIS ORDER BY id_heroi")
    herois = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template_string(HTML_TEMPLATE, herois=herois)

# Rota 1: Processar o turno (A Lógica exigida em PL/SQL)
@app.route('/processar', methods=['POST'])
def processar_turno():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # O Bloco PL/SQL processado no Oracle
        plsql_block = """
        DECLARE
            v_dano_nevoa NUMBER := 15;
            v_novo_hp NUMBER;
        BEGIN
            FOR r_heroi IN (SELECT id_heroi, hp_atual FROM TB_HEROIS WHERE status = 'ATIVO') LOOP
                v_novo_hp := r_heroi.hp_atual - v_dano_nevoa;
                
                IF v_novo_hp <= 0 THEN
                    UPDATE TB_HEROIS SET hp_atual = 0, status = 'CAÍDO' WHERE id_heroi = r_heroi.id_heroi;
                ELSE
                    UPDATE TB_HEROIS SET hp_atual = v_novo_hp WHERE id_heroi = r_heroi.id_heroi;
                END IF;
            END LOOP;
            COMMIT;
        END;
        """
        cursor.execute(plsql_block)
        cursor.close()
        conn.close()
        
    return redirect(url_for('index'))

# Rota 2: Resetar os heróis (Respawn)
@app.route('/resetar', methods=['POST'])
def resetar_herois():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # Cura todo mundo e volta o status para ATIVO
        comando_sql = "UPDATE TB_HEROIS SET hp_atual = hp_max, status = 'ATIVO'"
        cursor.execute(comando_sql)
        conn.commit() 
        
        cursor.close()
        conn.close()
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    # use_reloader=False evita aquele erro SystemExit caso você ainda rode por Notebook/Células no VS Code
    app.run(debug=True, use_reloader=False)