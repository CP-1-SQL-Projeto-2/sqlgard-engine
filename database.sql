
-- 1. CRIAÇÃO DA TABELA E DADOS INICIAIS

CREATE TABLE TB_HEROIS (
    id_heroi NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(50),
    classe VARCHAR2(20),
    hp_atual NUMBER,
    hp_max NUMBER,
    status VARCHAR2(20) DEFAULT 'ATIVO'
);

INSERT INTO TB_HEROIS (nome, classe, hp_atual, hp_max) VALUES ('Artorias', 'GUERREIRO', 100, 100);
INSERT INTO TB_HEROIS (nome, classe, hp_atual, hp_max) VALUES ('Sif', 'LADRÃO', 80, 80);
INSERT INTO TB_HEROIS (nome, classe, hp_atual, hp_max) VALUES ('Gwyn', 'MAGO', 60, 60);

COMMIT;



-- 2. CÓDIGOS EXECUTADOS PELO APP.PY

/*
Rota Principal:
SELECT id_heroi, nome, classe, hp_atual, hp_max, status 
FROM TB_HEROIS 
ORDER BY id_heroi;


Rota Processar Turno:
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


Rota Resetar:
UPDATE TB_HEROIS 
SET hp_atual = hp_max, status = 'ATIVO';
COMMIT;
*/