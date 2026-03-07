BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "aux_categoria" (
	"id_categoria"	INTEGER,
	"nome_categoria"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_categoria" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "aux_centro_custo" (
	"id_centro"	INTEGER,
	"nome_centro"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_centro" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "aux_doc_fiscal_tipo" (
	"id_doc"	INTEGER,
	"nome_doc"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_doc" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "aux_historico_tipo" (
	"id_historico"	INTEGER,
	"nome_historico"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_historico" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "aux_natureza_custo" (
	"id_natureza"	INTEGER,
	"nome_natureza"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_natureza" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "aux_recpag_condicao" (
	"id_condicao"	INTEGER,
	"nome_condicao"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_condicao" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "aux_recpag_metodos" (
	"id_metodo"	INTEGER,
	"nome_metodo"	TEXT NOT NULL,
	PRIMARY KEY("id_metodo")
);
CREATE TABLE IF NOT EXISTS "aux_recpag_status" (
	"id_status"	INTEGER,
	"nome_status"	TEXT NOT NULL UNIQUE,
	"descricao_status"	TEXT,
	PRIMARY KEY("id_status" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "cad_clifor" (
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
	FOREIGN KEY("id_clifor") REFERENCES "cad_clifor_tipo"("Id_clifor"),
	FOREIGN KEY("id_pessoa") REFERENCES "cad_clifor_pessoa"("id_pessoa"),
	FOREIGN KEY("id_unifed") REFERENCES "cad_uf"("id_unifed")
);
CREATE TABLE IF NOT EXISTS "cad_clifor_pessoa" (
	"id_pessoa"	INTEGER,
	"tipo_pessoa"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_pessoa" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "cad_clifor_tipo" (
	"Id_clifor"	INTEGER,
	"tipo_clifor"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Id_clifor" AUTOINCREMENT)
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
CREATE TABLE IF NOT EXISTS "cad_uf" (
	"id_unifed"	INTEGER,
	"estado"	TEXT NOT NULL UNIQUE,
	"sigla"	TEXT NOT NULL UNIQUE,
	"regiao"	TEXT NOT NULL,
	PRIMARY KEY("id_unifed" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "fin_banco" (
	"id_conta"	INTEGER,
	"nome_conta"	TEXT NOT NULL,
	"tipo_conta"	TEXT,
	"saldo_inicial"	DECIMAL(10, 2) DEFAULT 0,
	"num_banco"	TEXT,
	"agencia"	TEXT,
	"codigo"	TEXT,
	PRIMARY KEY("id_conta" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "fin_combustivel_abast" (
	"id_abastec"	INTEGER,
	"id_mov"	INTEGER,
	"fornecedor"	TEXT,
	"valor"	DECIMAL(10, 2) NOT NULL,
	"data_abastec"	DATE DEFAULT CURRENT_DATE,
	"litros"	DECIMAL(10, 2),
	"preco_unit_comb"	DECIMAL(10, 3),
	"km_init"	DECIMAL(10, 2),
	"km_fim"	DECIMAL(10, 2),
	"id_motorista"	INTEGER,
	PRIMARY KEY("id_abastec" AUTOINCREMENT),
	FOREIGN KEY("id_mov") REFERENCES "fin_mov_operacional"("id_mov")
);
CREATE TABLE IF NOT EXISTS "fin_fluxo_cxbc" (
	"id_conta"	INTEGER,
	"nome_conta"	TEXT NOT NULL,
	"tipo_conta"	TEXT,
	"saldo_inicial"	DECIMAL(15, 2) DEFAULT 0.00,
	"saldo_atual"	DECIMAL(15, 2) DEFAULT 0.00,
	"banco_nome"	TEXT,
	"agencia"	TEXT,
	"numero_conta"	TEXT,
	PRIMARY KEY("id_conta" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "fin_frete_status" (
	"id_status_frete"	INTEGER,
	"nome_status"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_status_frete" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "fin_mov_operacional" (
	"id_mov"	INTEGER,
	"num_ctrc"	TEXT,
	"data_init"	DATE,
	"data_fim"	DATE,
	"valor"	DECIMAL(10, 2),
	"origem_frete"	TEXT,
	"destino_frete"	TEXT,
	"distancia"	DECIMAL(10, 2),
	"num_nf_emitida"	TEXT,
	"id_veiculo"	INTEGER,
	"peso_carga"	DECIMAL(10, 2),
	"peso_tara"	DECIMAL(10, 2),
	"id_motorista"	INTEGER,
	"id_cliente"	INTEGER,
	"qtd_parcela"	INTEGER DEFAULT 1,
	"dta_vencimento"	DATE,
	PRIMARY KEY("id_mov" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "fin_mov_recpag" (
	"id_financeiro"	INTEGER,
	"tipo_lancamento"	TEXT CHECK("tipo_lancamento" IN ('Receita', 'Despesa')),
	"descricao"	TEXT NOT NULL,
	"id_conta"	INTEGER NOT NULL,
	"id_clifor"	INTEGER,
	"id_mov"	INTEGER,
	"id_veiculo"	INTEGER,
	"id_conta_bancaria"	INTEGER,
	"valor_original"	DECIMAL(10, 2) NOT NULL,
	"valor_pago"	DECIMAL(10, 2) DEFAULT 0.00,
	"data_competencia"	DATE NOT NULL,
	"data_vencimento"	DATE NOT NULL,
	"data_pagamento"	DATE,
	"status_pagamento"	TEXT DEFAULT 'Aberto' CHECK("status_pagamento" IN ('Aberto', 'Pago', 'Atrasado', 'Cancelado')),
	"observacoes"	TEXT,
	PRIMARY KEY("id_financeiro" AUTOINCREMENT),
	FOREIGN KEY("id_clifor") REFERENCES "cad_clifor"("id_colaborador"),
	FOREIGN KEY("id_conta") REFERENCES "fin_plano_contas"("id_conta"),
	FOREIGN KEY("id_conta_bancaria") REFERENCES "fin_banco"("id_conta"),
	FOREIGN KEY("id_mov") REFERENCES "fin_mov_operacional"("id_mov"),
	FOREIGN KEY("id_veiculo") REFERENCES "veiculo_ativo_imobilizado"("id_veiculo")
);
CREATE TABLE IF NOT EXISTS "fin_plano_contas" (
	"id_conta"	INTEGER,
	"codigo"	TEXT NOT NULL UNIQUE,
	"tipo_movimento"	TEXT NOT NULL,
	"categoria"	TEXT NOT NULL,
	"descricao"	TEXT NOT NULL,
	PRIMARY KEY("id_conta" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "login_usuarios" (
	"id"	INTEGER,
	"nome"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"senha"	TEXT NOT NULL,
	"cnpj"	TEXT,
	"created_at"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_combustivel" (
	"id_tipo_combustivel"	INTEGER,
	"nome_combustivel"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_tipo_combustivel" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_doc_status" (
	"id_status_doc"	INTEGER,
	"nome_status_doc"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_status_doc" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_doc_tipo" (
	"id_tipo_doc_veiculo"	INTEGER,
	"nome_documento"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_tipo_doc_veiculo" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_imobilizado" (
	"id_veiculo"	INTEGER,
	"id_unifed"	INTEGER,
	"id_clifor"	INTEGER,
	"placa"	TEXT NOT NULL UNIQUE,
	"id_modelo"	INTEGER,
	"id_tipo"	INTEGER,
	"id_combustivel"	INTEGER,
	"ano_fabricacao"	INTEGER,
	"ano_modelo"	INTEGER,
	"cor"	TEXT,
	"renavam"	TEXT,
	"chassi_veiculo"	TEXT UNIQUE,
	"tara_kg"	DECIMAL(10, 2),
	"capacidade_kg"	DECIMAL(10, 2),
	"num_bem"	TEXT UNIQUE,
	"descricao_bem"	TEXT,
	"num_doc_fiscal"	TEXT,
	"data_aquisicao"	DATE,
	"valor_aquisicao"	DECIMAL(15, 2),
	"valor_residual"	DECIMAL(15, 2),
	"taxa_depreciacao_anual"	DECIMAL(5, 2) DEFAULT 20.00,
	"vida_util"	INTEGER,
	"km_compra"	DECIMAL(10, 2),
	"km_inicial"	DECIMAL(10, 2),
	"km_atual"	DECIMAL(10, 2),
	"status_veiculo"	TEXT DEFAULT 'ATIVO' CHECK("status_veiculo" IN ('ATIVO', 'VENDIDO', 'INATIVO', 'MANUTENCAO')),
	"observacoes"	TEXT,
	PRIMARY KEY("id_veiculo" AUTOINCREMENT),
	FOREIGN KEY("id_clifor") REFERENCES "cad_clifor"("id_clifor"),
	FOREIGN KEY("id_combustivel") REFERENCES "vei_combustivel"("id_tipo_combustivel"),
	FOREIGN KEY("id_modelo") REFERENCES "vei_modelo"("id_modelo"),
	FOREIGN KEY("id_tipo") REFERENCES "vei_tipo"("id_tipo"),
	FOREIGN KEY("id_unifed") REFERENCES "cad_uf"("id_unifed")
);
CREATE TABLE IF NOT EXISTS "vei_manut_status" (
	"id_status_manutencao"	INTEGER,
	"nome_status"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_status_manutencao" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_manut_tipo" (
	"id_tipo_manutencao"	INTEGER,
	"nome_tipo"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_tipo_manutencao" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_marca" (
	"id_marca"	INTEGER,
	"nome_marca"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_marca" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_modelo" (
	"id_modelo"	INTEGER,
	"nome_modelo"	TEXT NOT NULL UNIQUE,
	"id_marca"	INTEGER,
	PRIMARY KEY("id_modelo" AUTOINCREMENT),
	FOREIGN KEY("id_marca") REFERENCES "vei_marca"("id_marca")
);
CREATE TABLE IF NOT EXISTS "vei_multa_gravidade" (
	"id_gravidade"	INTEGER,
	"nome_gravidade"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_gravidade" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_orgao_emissor" (
	"id_orgao"	INTEGER,
	"nome_orgao"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_orgao" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_pneu_marca" (
	"id_marca_pneu"	INTEGER,
	"nome_marca_pneu"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_marca_pneu" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_pneu_servico" (
	"id_servico_pneu"	INTEGER,
	"nome_servico"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_servico_pneu" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_pneu_situacao" (
	"id_situacao"	INTEGER,
	"nome_situacao"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_situacao" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_servico_tipo" (
	"id_servico"	INTEGER,
	"nome_servico"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_servico" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "vei_tipo" (
	"id_tipo"	INTEGER,
	"nome_tipo"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_tipo" AUTOINCREMENT)
);
INSERT INTO "aux_categoria" VALUES (1,'Receitas');
INSERT INTO "aux_categoria" VALUES (2,'Despesas');
INSERT INTO "aux_categoria" VALUES (3,'Ativo');
INSERT INTO "aux_categoria" VALUES (4,'Passivo');
INSERT INTO "aux_centro_custo" VALUES (1,'Operacional');
INSERT INTO "aux_centro_custo" VALUES (2,'Administração');
INSERT INTO "aux_centro_custo" VALUES (3,'Financeiro');
INSERT INTO "aux_centro_custo" VALUES (4,'Diretoria');
INSERT INTO "aux_centro_custo" VALUES (5,'Estoques');
INSERT INTO "aux_centro_custo" VALUES (6,'Investimentos');
INSERT INTO "aux_centro_custo" VALUES (7,'Impostos');
INSERT INTO "aux_centro_custo" VALUES (8,'Frotas');
INSERT INTO "aux_centro_custo" VALUES (9,'Geral');
INSERT INTO "aux_doc_fiscal_tipo" VALUES (1,'NFSE');
INSERT INTO "aux_doc_fiscal_tipo" VALUES (2,'NFE');
INSERT INTO "aux_doc_fiscal_tipo" VALUES (3,'Sem NF');
INSERT INTO "aux_doc_fiscal_tipo" VALUES (4,'Recibo');
INSERT INTO "aux_doc_fiscal_tipo" VALUES (5,'Fatura');
INSERT INTO "aux_historico_tipo" VALUES (1,'Entrada_Recebimento_Débito_Haver');
INSERT INTO "aux_historico_tipo" VALUES (2,'Saída_Pagamento_Crédito_Deve');
INSERT INTO "aux_natureza_custo" VALUES (1,'Custo Fixo');
INSERT INTO "aux_natureza_custo" VALUES (2,'Custo Variável');
INSERT INTO "aux_natureza_custo" VALUES (3,'Geral');
INSERT INTO "aux_recpag_condicao" VALUES (1,'A vista');
INSERT INTO "aux_recpag_condicao" VALUES (2,'Parcelado');
INSERT INTO "aux_recpag_condicao" VALUES (3,'Permuta');
INSERT INTO "aux_recpag_metodos" VALUES (1,'Dinheiro');
INSERT INTO "aux_recpag_metodos" VALUES (2,'Pix');
INSERT INTO "aux_recpag_metodos" VALUES (3,'Transferências');
INSERT INTO "aux_recpag_metodos" VALUES (4,'Cheque');
INSERT INTO "aux_recpag_metodos" VALUES (5,'Boleto');
INSERT INTO "aux_recpag_metodos" VALUES (6,'Fatura');
INSERT INTO "aux_recpag_metodos" VALUES (7,'Débito em Conta');
INSERT INTO "aux_recpag_metodos" VALUES (8,'Crédito em Conta');
INSERT INTO "aux_recpag_metodos" VALUES (9,'Cartão de Crédito');
INSERT INTO "aux_recpag_metodos" VALUES (10,'Cartão de Débito');
INSERT INTO "aux_recpag_metodos" VALUES (11,'Ted');
INSERT INTO "aux_recpag_status" VALUES (1,'Aberto','Documento ainda não iniciado');
INSERT INTO "aux_recpag_status" VALUES (2,'À vencer','Documento/obrigação próximo do vencimento');
INSERT INTO "aux_recpag_status" VALUES (3,'Liquidado','Documento/obrigação pago/concluído');
INSERT INTO "cad_clifor" VALUES (1,NULL,NULL,NULL,'239.720.929-20','Israel Augusto',NULL,'Rua Guarujá','191','Jardim Maria Helena','Barueri','06445070','11992574664','israelbizzarri@gmail.com','FORNECEDOR','JURIDICA');
INSERT INTO "cad_clifor" VALUES (2,2,1,25,'17.968.335/0001-09','Bruno Augusto de Matos da Silva','Maria','Rua Guarujá','191','Jardim Maria Helena','Barueri','06445-070','11992574664','gbizz.idi@gmail.com','FORNECEDOR','JURIDICA');
INSERT INTO "cad_clifor" VALUES (3,NULL,NULL,NULL,'50.118.354/0001-03','Gbizz Incubadora de ideias','Maria','Rua Guarujá','191','Jardim Maria Helena','Barueri','06445070','11992574664','gbizz.idi@gmail.com','FORNECEDOR','JURIDICA');
INSERT INTO "cad_clifor_pessoa" VALUES (1,'Pessoa Física');
INSERT INTO "cad_clifor_pessoa" VALUES (2,'Pessoa Jurídica');
INSERT INTO "cad_clifor_pessoa" VALUES (3,'Governos');
INSERT INTO "cad_clifor_tipo" VALUES (1,'Cliente');
INSERT INTO "cad_clifor_tipo" VALUES (2,'Fornecedor');
INSERT INTO "cad_clifor_tipo" VALUES (3,'Funcionário');
INSERT INTO "cad_clifor_tipo" VALUES (4,'Motorista');
INSERT INTO "cad_empresa" VALUES (1,'Israel Augusto','54.653.131/0001-05','06445-070','Rua Guarujá','191','Jardim Maria Helena','Barueri','SP','11992574664','gbizz.idi@gmail.com','2025-01-01',3000,'2699-9-99','Assessoria',25);
INSERT INTO "cad_uf" VALUES (1,'Acre','AC','Norte');
INSERT INTO "cad_uf" VALUES (2,'Alagoas','AL','Nordeste');
INSERT INTO "cad_uf" VALUES (3,'Amapá','AP','Norte');
INSERT INTO "cad_uf" VALUES (4,'Amazonas','AM','Norte');
INSERT INTO "cad_uf" VALUES (5,'Bahia','BA','Nordeste');
INSERT INTO "cad_uf" VALUES (6,'Ceará','CE','Nordeste');
INSERT INTO "cad_uf" VALUES (7,'Distrito Federal','DF','Centro-Oeste');
INSERT INTO "cad_uf" VALUES (8,'Espírito Santo','ES','Sudeste');
INSERT INTO "cad_uf" VALUES (9,'Goiás','GO','Centro-Oeste');
INSERT INTO "cad_uf" VALUES (10,'Maranhão','MA','Nordeste');
INSERT INTO "cad_uf" VALUES (11,'Mato Grosso','MT','Centro-Oeste');
INSERT INTO "cad_uf" VALUES (12,'Mato Grosso do Sul','MS','Centro-Oeste');
INSERT INTO "cad_uf" VALUES (13,'Minas Gerais','MG','Sudeste');
INSERT INTO "cad_uf" VALUES (14,'Pará','PA','Norte');
INSERT INTO "cad_uf" VALUES (15,'Paraíba','PB','Nordeste');
INSERT INTO "cad_uf" VALUES (16,'Paraná','PR','Sul');
INSERT INTO "cad_uf" VALUES (17,'Pernambuco','PE','Nordeste');
INSERT INTO "cad_uf" VALUES (18,'Piauí','PI','Nordeste');
INSERT INTO "cad_uf" VALUES (19,'Rio de Janeiro','RJ','Sudeste');
INSERT INTO "cad_uf" VALUES (20,'Rio Grande do Norte','RN','Nordeste');
INSERT INTO "cad_uf" VALUES (21,'Rio Grande do Sul','RS','Sul');
INSERT INTO "cad_uf" VALUES (22,'Rondônia','RO','Norte');
INSERT INTO "cad_uf" VALUES (23,'Roraima','RR','Norte');
INSERT INTO "cad_uf" VALUES (24,'Santa Catarina','SC','Sul');
INSERT INTO "cad_uf" VALUES (25,'São Paulo','SP','Sudeste');
INSERT INTO "cad_uf" VALUES (26,'Sergipe','SE','Nordeste');
INSERT INTO "cad_uf" VALUES (27,'Tocantins','TO','Norte');
INSERT INTO "fin_frete_status" VALUES (1,'Pendente');
INSERT INTO "fin_frete_status" VALUES (2,'Em Transito');
INSERT INTO "fin_frete_status" VALUES (3,'Concluido');
INSERT INTO "fin_frete_status" VALUES (4,'Cancelado');
INSERT INTO "fin_plano_contas" VALUES (1,'1.1.1','Receita','Receitas Operacionais','Fretes');
INSERT INTO "fin_plano_contas" VALUES (2,'1.1.2','Receita','Receitas Operacionais','Serviços');
INSERT INTO "fin_plano_contas" VALUES (3,'1.2.1','Receita','Receitas Não Operacionais','Aportes');
INSERT INTO "fin_plano_contas" VALUES (4,'1.2.2','Receita','Receitas Não Operacionais','Empréstimos');
INSERT INTO "fin_plano_contas" VALUES (5,'1.2.3','Receita','Receitas Não Operacionais','Venda de Veículos');
INSERT INTO "fin_plano_contas" VALUES (6,'2.1.1','Despesa','Com Veículos','Combustíveis');
INSERT INTO "fin_plano_contas" VALUES (7,'2.1.2','Despesa','Com Veículos','Arla - Agente Redutor Liquido');
INSERT INTO "fin_plano_contas" VALUES (8,'2.1.3','Despesa','Com Veículos','Óleos Lubrificantes');
INSERT INTO "fin_plano_contas" VALUES (9,'2.1.4','Despesa','Com Veículos','Manutenção');
INSERT INTO "fin_plano_contas" VALUES (10,'2.1.5','Despesa','Com Veículos','Pneus, Câmaras e Recapagens');
INSERT INTO "fin_plano_contas" VALUES (11,'2.1.6','Despesa','Com Veículos','Lavagem');
INSERT INTO "fin_plano_contas" VALUES (12,'2.1.7','Despesa','Com Veículos','Seguro da Carga');
INSERT INTO "fin_plano_contas" VALUES (13,'2.2.1','Despesa','Na Estrada','Frete de Terceiros');
INSERT INTO "fin_plano_contas" VALUES (14,'2.2.2','Despesa','Na Estrada','Chapas');
INSERT INTO "fin_plano_contas" VALUES (15,'2.2.3','Despesa','Na Estrada','Pedágios');
INSERT INTO "fin_plano_contas" VALUES (16,'3.1.1.1','Despesa','Operacionais - Com o Imóvel','Aluguel');
INSERT INTO "fin_plano_contas" VALUES (17,'3.1.1.2','Despesa','Operacionais - Com o Imóvel','Energia Elétrica');
INSERT INTO "fin_plano_contas" VALUES (18,'3.1.1.3','Despesa','Operacionais - Com o Imóvel','Água');
INSERT INTO "fin_plano_contas" VALUES (19,'3.1.1.4','Despesa','Operacionais - Com o Imóvel','Materiais de Limpeza');
INSERT INTO "fin_plano_contas" VALUES (20,'3.1.1.5','Despesa','Operacionais - Com o Imóvel','Segurança e Monitoramento');
INSERT INTO "fin_plano_contas" VALUES (21,'3.1.2.1','Despesa','Operacionais - Com a Administração','Materiais de Escritório');
INSERT INTO "fin_plano_contas" VALUES (22,'3.1.2.2','Despesa','Operacionais - Com a Administração','Telefonia');
INSERT INTO "fin_plano_contas" VALUES (23,'3.1.2.3','Despesa','Operacionais - Com a Administração','Marketing');
INSERT INTO "fin_plano_contas" VALUES (24,'3.1.2.4','Despesa','Operacionais - Com a Administração','Informática');
INSERT INTO "fin_plano_contas" VALUES (25,'3.1.2.5','Despesa','Operacionais - Com a Administração','Contabilidade');
INSERT INTO "fin_plano_contas" VALUES (26,'3.1.2.6','Despesa','Operacionais - Com a Administração','Seguro dos Veículos');
INSERT INTO "fin_plano_contas" VALUES (27,'3.1.2.7','Despesa','Operacionais - Com a Administração','Monitoramento Rodoviário');
INSERT INTO "fin_plano_contas" VALUES (28,'3.1.2.8','Despesa','Operacionais - Com a Administração','Despesas Bancárias');
INSERT INTO "fin_plano_contas" VALUES (29,'3.1.3.1','Despesa','Operacionais - Recursos Humanos','Salários e Adiantamentos');
INSERT INTO "fin_plano_contas" VALUES (30,'3.1.3.2','Despesa','Operacionais - Recursos Humanos','Pró-Labore');
INSERT INTO "fin_plano_contas" VALUES (31,'3.1.3.3','Despesa','Operacionais - Recursos Humanos','Vale Transporte');
INSERT INTO "fin_plano_contas" VALUES (32,'3.1.3.4','Despesa','Operacionais - Recursos Humanos','Vale Refeição');
INSERT INTO "fin_plano_contas" VALUES (33,'3.1.3.5','Despesa','Operacionais - Recursos Humanos','Gratificações');
INSERT INTO "fin_plano_contas" VALUES (34,'3.1.3.6','Despesa','Operacionais - Recursos Humanos','Horas Extras');
INSERT INTO "fin_plano_contas" VALUES (35,'3.1.3.7','Despesa','Operacionais - Recursos Humanos','Rescisões');
INSERT INTO "fin_plano_contas" VALUES (36,'3.1.3.8','Despesa','Operacionais - Recursos Humanos','Férias');
INSERT INTO "fin_plano_contas" VALUES (37,'3.1.3.9','Despesa','Operacionais - Recursos Humanos','13º Salário');
INSERT INTO "fin_plano_contas" VALUES (38,'3.1.3.10','Despesa','Operacionais - Recursos Humanos','Plano de Saúde');
INSERT INTO "fin_plano_contas" VALUES (39,'3.1.3.11','Despesa','Operacionais - Recursos Humanos','Encargos');
INSERT INTO "fin_plano_contas" VALUES (40,'3.1.3.12','Despesa','Operacionais - Recursos Humanos','FGTS');
INSERT INTO "fin_plano_contas" VALUES (41,'3.1.3.13','Despesa','Operacionais - Recursos Humanos','GPS');
INSERT INTO "fin_plano_contas" VALUES (42,'3.1.3.14','Despesa','Operacionais - Recursos Humanos','IR Funcionários');
INSERT INTO "fin_plano_contas" VALUES (43,'3.1.3.15','Despesa','Operacionais - Recursos Humanos','Sindicato');
INSERT INTO "fin_plano_contas" VALUES (44,'3.1.4.1','Despesa','Impostos','Simples Federal');
INSERT INTO "fin_plano_contas" VALUES (45,'3.1.4.2','Despesa','Impostos','ISS');
INSERT INTO "fin_plano_contas" VALUES (46,'3.1.4.3','Despesa','Impostos','ICMS');
INSERT INTO "fin_plano_contas" VALUES (47,'3.1.4.4','Despesa','Impostos','PIS');
INSERT INTO "fin_plano_contas" VALUES (48,'3.1.4.5','Despesa','Impostos','COFINS');
INSERT INTO "fin_plano_contas" VALUES (49,'3.1.4.6','Despesa','Impostos','CSLL');
INSERT INTO "fin_plano_contas" VALUES (50,'3.1.4.7','Despesa','Impostos','IRPJ');
INSERT INTO "fin_plano_contas" VALUES (51,'3.1.4.8','Despesa','Impostos','INSS');
INSERT INTO "fin_plano_contas" VALUES (52,'3.2.1','Despesa','Não Operacionais','Financiamento de Veículos');
INSERT INTO "fin_plano_contas" VALUES (53,'3.2.2','Despesa','Não Operacionais','Depreciações dos Veículos');
INSERT INTO "fin_plano_contas" VALUES (54,'3.2.3','Despesa','Não Operacionais','Móveis e Equipamentos do Escritório');
INSERT INTO "fin_plano_contas" VALUES (55,'3.2.4','Despesa','Não Operacionais','Reformas no Imóvel do Escritório');
INSERT INTO "login_usuarios" VALUES (1,'Nonato','jna@gmail.com','$2b$12$jCqj8EWum/AQgE4bAdWGSODZH9emeeRL1/YQ6ieD9.9mjGag2DMDW','','2026-03-06 23:11:58');
INSERT INTO "login_usuarios" VALUES (2,'jna','jna_novo@gmail.com','$2b$12$eStCh5Avo.3jSx67ZT3Ok.c/4yW6DLi9otmrQBV5dKxhWllfCT3ye','','2026-03-06 23:20:14');
INSERT INTO "login_usuarios" VALUES (3,'Israel Augusto','gbizz.idi@gmail.com','$2b$12$ZyU2BpVyOFx9HOVzzY/5auk93yoK2lUPfX3jdb15oeRyoCNnjjxvm','','2026-03-07 18:45:40');
INSERT INTO "vei_combustivel" VALUES (1,'Gasolina Comum');
INSERT INTO "vei_combustivel" VALUES (2,'Gasolina Aditivada');
INSERT INTO "vei_combustivel" VALUES (3,'Gasolina Premium');
INSERT INTO "vei_combustivel" VALUES (4,'Etanol Hidratado');
INSERT INTO "vei_combustivel" VALUES (5,'Etanol Aditivado');
INSERT INTO "vei_combustivel" VALUES (6,'Diesel S10');
INSERT INTO "vei_combustivel" VALUES (7,'Diesel S500');
INSERT INTO "vei_combustivel" VALUES (8,'Biodiesel	');
INSERT INTO "vei_combustivel" VALUES (9,'Eletricidade');
INSERT INTO "vei_combustivel" VALUES (10,'Gás Natural Veicular');
INSERT INTO "vei_doc_status" VALUES (1,'Regularizado');
INSERT INTO "vei_doc_status" VALUES (2,'Atrasado');
INSERT INTO "vei_doc_status" VALUES (3,'Vencido');
INSERT INTO "vei_doc_tipo" VALUES (1,'CRLV');
INSERT INTO "vei_doc_tipo" VALUES (2,'CNH');
INSERT INTO "vei_doc_tipo" VALUES (3,'ANTT');
INSERT INTO "vei_doc_tipo" VALUES (4,'IPVA');
INSERT INTO "vei_doc_tipo" VALUES (5,'licenciamento');
INSERT INTO "vei_doc_tipo" VALUES (6,'seguro_obrigatorio');
INSERT INTO "vei_doc_tipo" VALUES (7,'seguro_carga');
INSERT INTO "vei_doc_tipo" VALUES (8,'seguro_veiculo');
INSERT INTO "vei_manut_status" VALUES (1,'Agendada');
INSERT INTO "vei_manut_status" VALUES (2,'Em Andamento');
INSERT INTO "vei_manut_status" VALUES (3,'Concluida');
INSERT INTO "vei_manut_status" VALUES (4,'Cancelada');
INSERT INTO "vei_manut_tipo" VALUES (1,'Preventiva');
INSERT INTO "vei_manut_tipo" VALUES (2,'Corretiva');
INSERT INTO "vei_manut_tipo" VALUES (3,'Revisão');
INSERT INTO "vei_marca" VALUES (1,'Nissan');
INSERT INTO "vei_marca" VALUES (2,'Chevrolet');
INSERT INTO "vei_marca" VALUES (3,'Scania');
INSERT INTO "vei_marca" VALUES (4,'Volvo');
INSERT INTO "vei_marca" VALUES (5,'Mercedes');
INSERT INTO "vei_marca" VALUES (6,'Vw');
INSERT INTO "vei_marca" VALUES (7,'Ford');
INSERT INTO "vei_marca" VALUES (8,'Fiat');
INSERT INTO "vei_modelo" VALUES (1,'COBALT',2);
INSERT INTO "vei_modelo" VALUES (2,'M2323',4);
INSERT INTO "vei_modelo" VALUES (3,'MB-3569',5);
INSERT INTO "vei_modelo" VALUES (4,'BYD234',6);
INSERT INTO "vei_multa_gravidade" VALUES (1,'Leve');
INSERT INTO "vei_multa_gravidade" VALUES (2,'Média');
INSERT INTO "vei_multa_gravidade" VALUES (3,'Grave');
INSERT INTO "vei_multa_gravidade" VALUES (4,'Gravíssima');
INSERT INTO "vei_multa_gravidade" VALUES (5,'Não possui multa');
INSERT INTO "vei_orgao_emissor" VALUES (1,'Detran-SP');
INSERT INTO "vei_pneu_marca" VALUES (1,'Bridgestone');
INSERT INTO "vei_pneu_marca" VALUES (2,'Goodyear');
INSERT INTO "vei_pneu_marca" VALUES (3,'Michelin');
INSERT INTO "vei_pneu_marca" VALUES (4,'Pirelli');
INSERT INTO "vei_pneu_servico" VALUES (1,'Recapagem');
INSERT INTO "vei_pneu_servico" VALUES (2,'Balanceamento');
INSERT INTO "vei_pneu_servico" VALUES (3,'Remoldagem');
INSERT INTO "vei_pneu_servico" VALUES (4,'Rodízio');
INSERT INTO "vei_pneu_situacao" VALUES (1,'Em uso');
INSERT INTO "vei_pneu_situacao" VALUES (2,'Recapado');
INSERT INTO "vei_pneu_situacao" VALUES (3,'Em estoque');
INSERT INTO "vei_pneu_situacao" VALUES (4,'Descartado');
INSERT INTO "vei_servico_tipo" VALUES (1,'Bateria');
INSERT INTO "vei_servico_tipo" VALUES (2,'Tacografo');
INSERT INTO "vei_servico_tipo" VALUES (3,'Cambio');
INSERT INTO "vei_servico_tipo" VALUES (4,'Motor');
INSERT INTO "vei_servico_tipo" VALUES (5,'Cabine');
INSERT INTO "vei_servico_tipo" VALUES (6,'Porta');
INSERT INTO "vei_servico_tipo" VALUES (7,'Bau');
INSERT INTO "vei_servico_tipo" VALUES (8,'Km_atual');
INSERT INTO "vei_servico_tipo" VALUES (9,'Peca trocada');
INSERT INTO "vei_tipo" VALUES (1,'Automóvel');
INSERT INTO "vei_tipo" VALUES (2,'Caminhão');
INSERT INTO "vei_tipo" VALUES (3,'Empilhadeira');
INSERT INTO "vei_tipo" VALUES (4,'Trator');
INSERT INTO "vei_tipo" VALUES (5,'Bi-Trem');
INSERT INTO "vei_tipo" VALUES (6,'Fora de Estrada');
INSERT INTO "vei_tipo" VALUES (7,'Patrola');
INSERT INTO "vei_tipo" VALUES (8,'Baú');
INSERT INTO "vei_tipo" VALUES (9,'Cavalo');
INSERT INTO "vei_tipo" VALUES (10,'Reboque');
INSERT INTO "vei_tipo" VALUES (11,'Utilitario');
INSERT INTO "vei_tipo" VALUES (12,'Van');
COMMIT;
