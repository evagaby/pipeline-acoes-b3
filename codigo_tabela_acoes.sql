CREATE TABLE acoes (
id  SERIAL PRIMARY KEY ,
symbol_empresa VARCHAR(10),
nome_da_empresa VARCHAR(50),
moeda VARCHAR (4),
preco_regular DECIMAL(7,2),
preco_mais_alto DECIMAL(7,2),
preco_mais_baixo DECIMAL(7,2),
variacao_de_preco DECIMAL(7,2),
perceNtual_variacao_de_preco DECIMAL(7,2),
hora_coleta TIMESTAMP,
UNIQUE (symbol_empresa, hora_coleta)
);