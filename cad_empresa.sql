BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "aux_categoria" (
	"id_categoria"	INTEGER,
	"nome_categoria"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_categoria" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "cad_empresa" (
	"id_empresa"	INTEGER,
	"razao_social"	TEXT NOT NULL,
	"CNPJ"	TEXT NOT NULL,
	"Cep"	TEXT,
	"logradouro"	TEXT,
	"numero"	TEXT,
	"bairro"	TEXT,
	"municipio"	TEXT,
	"uf"	TEXT,
	"telefone"	TEXT,
	"email"	TEXT,
	"data_abertura"	DATE,
	"capital_social"	DECIMAL(15, 2),
	"cnae_principal"	TEXT,
	"ocupacao_principal"	TEXT,
	"id_unifed"	INTEGER,
	PRIMARY KEY("id_empresa" AUTOINCREMENT),
	FOREIGN KEY("id_unifed") REFERENCES "cad_uf"("id_unifed")
);
INSERT INTO "aux_categoria" VALUES (1,'Receitas');
INSERT INTO "aux_categoria" VALUES (2,'Despesas');
INSERT INTO "aux_categoria" VALUES (3,'Ativo');
INSERT INTO "aux_categoria" VALUES (4,'Passivo');
INSERT INTO "cad_empresa" VALUES (1,'Israel Augusto','54.653.131/0001-05','06445-070','Rua Guarujá','191','Jardim Maria Helena','Barueri','SP','11992574664','gbizz.idi@gmail.com','2025-01-01',3000,'2699-9-99','Assessoria',25);
COMMIT;
