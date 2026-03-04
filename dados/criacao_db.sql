BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "clifor_motorista" (
	"id_colaborador"	INTEGER,
	"id_pessoa"	INTEGER,
	"id_clifor"	INTEGER,
	"id_unifed"	INTEGER,
	"cpf_cnpj"	TEXT NOT NULL UNIQUE,
	"nome_colaborador"	TEXT NOT NULL,
	"contato_responsavel"	TEXT,
	"logradouro"	TEXT,
	"numero"	TEXT,
	"bairro"	TEXT,
	"municipio"	TEXT,
	"cep"	TEXT,
	"telefone"	TEXT,
	"email"	TEXT,
	"tipo_clifor"	TEXT DEFAULT 'FORNECEDOR',
	"tipo_pessoa"	TEXT DEFAULT 'JURIDICA',
	PRIMARY KEY("id_colaborador" AUTOINCREMENT),
	FOREIGN KEY("id_clifor") REFERENCES "tipo_clifor"("Id_clifor"),
	FOREIGN KEY("id_pessoa") REFERENCES "tipo_pessoa"("id_pessoa"),
	FOREIGN KEY("id_unifed") REFERENCES "uf_estado"("id_unifed")
);
CREATE TABLE IF NOT EXISTS "tipo_clifor" (
	"Id_clifor"	INTEGER,
	"tipo_clifor"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Id_clifor" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "tipo_pessoa" (
	"id_pessoa"	INTEGER,
	"tipo_pessoa"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_pessoa" AUTOINCREMENT)
);
INSERT INTO "clifor_motorista" VALUES (1,NULL,NULL,NULL,'239.720.929-20','Israel Augusto',NULL,'Rua Guarujá','191','Jardim Maria Helena','Barueri','06445070','11992574664','israelbizzarri@gmail.com','FORNECEDOR','JURIDICA');
INSERT INTO "clifor_motorista" VALUES (2,2,1,25,'17.968.335/0001-09','Bruno Augusto de Matos da Silva','Maria','Rua Guarujá','191','Jardim Maria Helena','Barueri','06445-070','11992574664','gbizz.idi@gmail.com','FORNECEDOR','JURIDICA');
INSERT INTO "clifor_motorista" VALUES (3,NULL,NULL,NULL,'50.118.354/0001-03','Gbizz Incubadora de ideias','Maria','Rua Guarujá','191','Jardim Maria Helena','Barueri','06445070','11992574664','gbizz.idi@gmail.com','FORNECEDOR','JURIDICA');
INSERT INTO "tipo_clifor" VALUES (1,'Cliente');
INSERT INTO "tipo_clifor" VALUES (2,'Fornecedor');
INSERT INTO "tipo_clifor" VALUES (3,'Funcionário');
INSERT INTO "tipo_clifor" VALUES (4,'Motorista');
INSERT INTO "tipo_pessoa" VALUES (1,'Pessoa Física');
INSERT INTO "tipo_pessoa" VALUES (2,'Pessoa Jurídica');
INSERT INTO "tipo_pessoa" VALUES (3,'Governos');
COMMIT;
