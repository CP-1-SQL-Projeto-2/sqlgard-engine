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

# Frontend
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
        .btn { background-color: #8b0000; color: white; padding: 15px 30px; text-decoration: none; font-size: 18px; border-radius: 5px; border: none; cursor: pointer; display: inline-block; margin-top: 20px; transition: 0.3s;}
        .btn:hover { background-color: #ff0000; transform: scale(1.05); }
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
    <form action="/processar" method="POST">
        <button type="submit" class="btn">Processar Próximo Turno da Névoa ☠️</button>
    </form>
</body>
</html>
"""

# Rota principal
@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        return "<h1>Erro de conexão!</h1><p>Verifique as variáveis de ambiente (DB_USER, DB_PASSWORD, DB_DSN) no Vercel.</p>"
    
    cursor = conn.cursor()
    cursor.execute("SELECT id_heroi, nome, classe, hp_atual, hp_max, status FROM TB_HEROIS ORDER BY id_heroi")
    herois = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template_string(HTML_TEMPLATE, herois=herois)

# Rota de processamento
@app.route('/processar', methods=['POST'])
def processar_turno():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
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

if __name__ == '__main__':
    app.run(debug=True)