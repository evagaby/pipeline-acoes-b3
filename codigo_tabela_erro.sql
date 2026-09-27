CREATE TABLE tabela_erros (
id SERIAL PRIMARY KEY, 
codigo_erro VARCHAR(5),
mensagem_erro TEXT, 
task_origem VARCHAR(30),
hora_erro TIMESTAMP
);