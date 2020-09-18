# © 2012 KMEE INFORMATICA LTDA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

NAO_EMITE_AVISO = ("0", "0 - Não Emite Aviso")
EMITE_AVISO_REMETENTE = ("2", "2 - Emite Aviso Somente para o Remetente")
EMITE_AVISO_FAVORECIDO = ("5", "5 - Emite Aviso Somente para o Favorecido")
EMITE_AVISO_REMETENTE_FAVORECIDO = (
    "6",
    "6 - Emite Aviso para o Remetente e Favorecido",
)
EMITE_AVISO_FAVORECIDO_2_VIAS_REMETENTE = (
    "7",
    "7 - Emite Aviso para o Favorecido e 2 Vias para o Remetente",
)

AVISO_FAVORECIDO = [
    NAO_EMITE_AVISO,
    EMITE_AVISO_REMETENTE,
    EMITE_AVISO_FAVORECIDO,
    EMITE_AVISO_REMETENTE_FAVORECIDO,
    EMITE_AVISO_FAVORECIDO_2_VIAS_REMETENTE,
]

INDICATIVO_FORMA_PAGAMENTO = [
    ("01", "01 - Débito em Conta Corrente"),
    ("02", "02 - Débito Empréstimo/Financiamento"),
    ("03", "03 - Débito Cartão de Crédito"),
]

TIPO_MOVIMENTO = [
    ("0", "0 - Indica INCLUSÃO"),
    ("1", "1 - Indica CONSULTA"),
    ("2", "2 - Indica SUSPENSÃO"),
    ("3", "3 - Indica ESTORNO (somente para retorno)"),
    ("4", "4 - Indica REATIVAÇÃO"),
    ("5", "5 - Indica ALTERAÇÃO"),
    ("7", "7 - Indica LIQUIDAÇAO"),
    ("9", "9 - Indica EXCLUSÃO"),
]

CODIGO_INSTRUCAO_MOVIMENTO = [
    ("00", "00 - Inclusão de Registro Detalhe Liberado"),
    ("09", "09 - Inclusão do Registro Detalhe Bloqueado"),
    ("10", "10 - Alteração do Pagamento Liberado para Bloqueado (Bloqueio)"),
    ("11", "11 - Alteração do Pagamento Bloqueado para Liberado (Liberação)"),
    ("17", "17 - Alteração do Valor do Título"),
    ("19", "19 - Alteração da Data de Pagamento"),
    ("23", "23 - Pagamento Direto ao Fornecedor - Baixar"),
    ("25", "25 - Manutenção em Carteira - Não Pagar"),
    ("27", "27 - Retirada de Carteira - Não Pagar"),
    (
        "33",
        "33 - Estorno por Devolução da Câmara Centralizadora "
        "(somente para Tipo de Movimento = '3')",
    ),
    ("40", "40 - Alegação do Pagador"),
    ("99", "99 - Exclusão do Registro Detalhe Incluído Anteriormente"),
]

CODIGO_OCORRENCIAS = [
    ("00", "00 - Crédito ou Débito Efetivado"),
    ("01", "01 - Insuficiência de Fundos - Débito Não Efetuado"),
    ("02", "02 - Crédito ou Débito Cancelado pelo Pagador/Credor"),
    ("03", "03 - Débito Autorizado pela Agência - Efetuado"),
    ("AA", "AA - Controle Inválido"),
    ("AB", "AB - Tipo de Operação Inválido"),
    ("AC", "AC - Tipo de Serviço Inválido"),
    ("AD", "AD - Forma de Lançamento Inválida"),
    ("AE", "AE - Tipo/Número de Inscrição Inválido"),
    ("AF", "AF - Código de Convênio Inválido"),
    ("AG", "AG - Agência/Conta Corrente/DV Inválido"),
    ("AH", "AH - Nº Seqüencial do Registro no Lote Inválido"),
    ("AI", "AI - Código de Segmento de Detalhe Inválido"),
    ("AJ", "AJ - Tipo de Movimento Inválido"),
    (
        "AK",
        "AK - Código da Câmara de Compensação do Banco"
        " Favorecido/Depositário Inválido",
    ),
    (
        "AL",
        "AL - Código do Banco Favorecido, Instituição de Pagamento"
        " ou Depositário Inválido",
    ),
    ("AM", "AM - Agência Mantenedora da Conta Corrente do" " Favorecido Inválida"),
    ("AN", "AN - Conta Corrente/DV/Conta de Pagamento do" " Favorecido Inválido"),
    ("AO", "AO - Nome do Favorecido Não Informado"),
    ("AP", "AP - Data Lançamento Inválido"),
    ("AQ", "AQ - Tipo/Quantidade da Moeda Inválido"),
    ("AR", "AR - Valor do Lançamento Inválido"),
    ("AS", "AS - Aviso ao Favorecido - Identificação Inválida"),
    ("AT", "AT - Tipo/Número de Inscrição do Favorecido Inválido"),
    ("AU", "AU - Logradouro do Favorecido Não Informado"),
    ("AV", "AV - Nº do Local do Favorecido Não Informado"),
    ("AW", "AW - Cidade do Favorecido Não Informada"),
    ("AX", "AX - CEP/Complemento do Favorecido Inválido"),
    ("AY", "AY - Sigla do Estado do Favorecido Inválida"),
    ("AZ", "AZ - Código/Nome do Banco Depositário Inválido"),
    ("BA", "BA - Código/Nome da Agência Depositária Não Informado"),
    ("BB", "BB - Seu Número Inválido"),
    ("BC", "BC - Nosso Número Inválido"),
    ("BD", "BD - Inclusão Efetuada com Sucesso"),
    ("BE", "BE - Alteração Efetuada com Sucesso"),
    ("BF", "BF - Exclusão Efetuada com Sucesso"),
    ("BG", "BG - Agência/Conta Impedida Legalmente"),
    ("BH", "BH - Empresa não pagou salário"),
    ("BI", "BI - Falecimento do mutuário"),
    ("BJ", "BJ - Empresa não enviou remessa do mutuário"),
    ("BK", "BK - Empresa não enviou remessa no vencimento"),
    ("BL", "BL - Valor da parcela inválida"),
    ("BM", "BM - Identificação do contrato inválida"),
    ("BN", "BN - Operação de Consignação Incluída com Sucesso"),
    ("BO", "BO - Operação de Consignação Alterada com Sucesso"),
    ("BP", "BP - Operação de Consignação Excluída com Sucesso"),
    ("BQ", "BQ - Operação de Consignação Liquidada com Sucesso"),
    ("BR", "BR - Reativação Efetuada com Sucesso"),
    ("BS", "BS - Suspensão Efetuada com Sucesso"),
    ("CA", "CA - Código de Barras - Código do Banco Inválido"),
    ("CB", "CB - Código de Barras - Código da Moeda Inválido"),
    ("CC", "CC - Código de Barras - Dígito Verificador Geral Inválido"),
    ("CD", "CD - Código de Barras - Valor do Título Inválido"),
    ("CE", "CE - Código de Barras - Campo Livre Inválido"),
    ("CF", "CF - Valor do Documento Inválido"),
    ("CG", "CG - Valor do Abatimento Inválido"),
    ("CH", "CH - Valor do Desconto Inválido"),
    ("CI", "CI - Valor de Mora Inválido"),
    ("CJ", "CJ - Valor da Multa Inválido"),
    ("CK", "CK - Valor do IR Inválido"),
    ("CL", "CL - Valor do ISS Inválido"),
    ("CM", "CM - Valor do IOF Inválido"),
    ("CN", "CN - Valor de Outras Deduções Inválido"),
    ("CO", "CO - Valor de Outros Acréscimos Inválido"),
    ("CP", "CP - Valor do INSS Inválido"),
    ("HA", "HA - Lote Não Aceito"),
    ("HB", "HB - Inscrição da Empresa Inválida para o Contrato"),
    ("HC", "HC - Convênio com a Empresa Inexistente/Inválido" " para o Contrato"),
    (
        "HD",
        "HD - Agência/Conta Corrente da Empresa Inexistente/Inválido"
        " para o Contrato",
    ),
    ("HE", "HE - Tipo de Serviço Inválido para o Contrato"),
    ("HF", "HF - Conta Corrente da Empresa com Saldo Insuficiente"),
    ("HG", "HG - Lote de Serviço Fora de Seqüência"),
    ("HH", "HH - Lote de Serviço Inválido"),
    ("HI", "HI - Arquivo não aceito"),
    ("HJ", "HJ - Tipo de Registro Inválido"),
    ("HK", "HK - Código Remessa / Retorno Inválido"),
    ("HL", "HL - Versão de layout inválida"),
    ("HM", "HM - Mutuário não identificado"),
    ("HN", "HN - Tipo do beneficio não permite empréstimo"),
    ("HO", "HO - Beneficio cessado/suspenso"),
    ("HP", "HP - Beneficio possui representante legal"),
    ("HQ", "HQ - Beneficio é do tipo PA (Pensão alimentícia)"),
    ("HR", "HR - Quantidade de contratos permitida excedida"),
    ("HS", "HS - Beneficio não pertence ao Banco informado"),
    ("HT", "HT - Início do desconto informado já ultrapassado"),
    ("HU", "HU - Número da parcela inválida"),
    ("HV", "HV - Quantidade de parcela inválida"),
    (
        "HW",
        "HW - Margem consignável excedida para o mutuário dentro"
        " do prazo do contrato",
    ),
    ("HX", "HX - Empréstimo já cadastrado"),
    ("HY", "HY - Empréstimo inexistente"),
    ("HZ", "HZ - Empréstimo já encerrado"),
    ("H1", "H1 - Arquivo sem trailer"),
    ("H2", "H2 - Mutuário sem crédito na competência"),
    ("H3", "H3 - Não descontado – outros motivos"),
    ("H4", "H4 - Retorno de Crédito não pago"),
    ("H5", "H5 - Cancelamento de empréstimo retroativo"),
    ("H6", "H6 - Outros Motivos de Glosa"),
    (
        "H7",
        "H7 - Margem consignável excedida para o mutuário acima"
        " do prazo do contrato",
    ),
    ("H8", "H8 - Mutuário desligado do empregador"),
    ("H9", "H9 - Mutuário afastado por licença"),
    (
        "IA",
        "IA - Primeiro nome do mutuário diferente do primeiro nome"
        " do movimento do censo ou diferente da base de Titular"
        " do Benefício",
    ),
    ("IB", "IB - Benefício suspenso/cessado pela APS ou Sisobi"),
    ("IC", "IC - Benefício suspenso por dependência de cálculo"),
    ("ID", "ID - Benefício suspenso/cessado pela inspetoria/auditoria"),
    ("IE", "IE - Benefício bloqueado para empréstimo pelo beneficiário"),
    ("IF", "IF - Benefício bloqueado para empréstimo por TBM"),
    ("IG", "IG - Benefício está em fase de concessão de PA ou desdobramento"),
    ("IH", "IH - Benefício cessado por óbito"),
    ("II", "II - Benefício cessado por fraude"),
    ("IJ", "IJ - Benefício cessado por concessão de outro benefício"),
    ("IK", "IK - Benefício cessado: estatutário transferido" " para órgão de origem"),
    ("IL", "IL - Empréstimo suspenso pela APS"),
    ("IM", "IM - Empréstimo cancelado pelo banco"),
    ("IN", "IN - Crédito transformado em PAB"),
    ("IO", "IO - Término da consignação foi alterado"),
    (
        "IP",
        "IP - Fim do empréstimo ocorreu durante período" " de suspensão ou concessão",
    ),
    ("IQ", "IQ - Empréstimo suspenso pelo banco"),
    (
        "IR",
        "IR - Não averbação de contrato – quantidade de"
        " parcelas/competências informadas ultrapassou a data limite"
        " da extinção de cota do dependente titular de benefícios",
    ),
    ("TA", "TA - Lote Não Aceito - Totais do Lote com Diferença"),
    ("YA", "YA - Título Não Encontrado"),
    ("YB", "YB - Identificador Registro Opcional Inválido"),
    ("YC", "YC - Código Padrão Inválido"),
    ("YD", "YD - Código de Ocorrência Inválido"),
    ("YE", "YE - Complemento de Ocorrência Inválido"),
    ("YF", "YF - Alegação já Informada"),
    ("ZA", "ZA - Agência / Conta do Favorecido Substituída"),
    (
        "ZB",
        "ZB - Divergência entre o primeiro e último nome do beneficiário"
        " versus primeiro e último nome na Receita Federal",
    ),
    ("ZC", "ZC - Confirmação de Antecipação de Valor"),
    ("ZD", "ZD - Antecipação parcial de valor"),
    ("ZE", "ZE - Título bloqueado na base"),
    ("ZF", "ZF - Sistema em contingência" " – título valor maior que referência"),
    ("ZG", "ZG - Sistema em contingência – título vencido"),
    ("ZH", "ZH - Sistema em contingência – título indexado"),
    ("ZI", "ZI - Beneficiário divergente"),
    ("ZJ", "ZJ - Limite de pagamentos parciais excedido"),
    ("ZK", "ZK - Boleto já liquidado"),
]

ESTADOS_CNAB = [
    ("draft", "Inicial"),
    ("added", "Adicionada à ordem de pagamento"),
    ("added_paid", "Adicionada para Baixa"),
    ("exported", "Exportada"),
    ("exporting_error", "Erro ao exportar"),
    ("accepted", "Aceita"),
    ("accepted_hml", "Aceita em Homologação"),
    ("not_accepted", "Não aceita pelo banco"),
    ("done", "Concluído"),
]

SITUACAO_PAGAMENTO = [
    ("inicial", "Inicial"),
    ("aberta", "Aberta"),
    ("paga", "Paga"),
    ("liquidada", "Liquidada"),
    ("baixa", "Baixa Simples"),
    ("baixa_liquidacao", "Baixa por Liquidação em Dinheiro"),
]

BOLETO_ESPECIE = [
    ("01", "DUPLICATA MERCANTIL"),
    ("02", "NOTA PROMISSÓRIA"),
    ("03", "NOTA DE SEGURO"),
    ("04", "MENSALIDADE ESCOLAR"),
    ("05", "RECIBO"),
    ("06", "CONTRATO"),
    ("07", "COSSEGUROS"),
    ("08", "DUPLICATA DE SERVIÇO"),
    ("09", "LETRA DE CÂMBIO"),
    ("13", "NOTA DE DÉBITOS"),
    ("15", "DOCUMENTO DE DÍVIDA"),
    ("16", "ENCARGOS CONDOMINIAIS"),
    ("17", "CONTA DE PRESTAÇÃO DE SERVIÇOS"),
    ("99", "DIVERSOS"),
]

STATE_CNAB = [
    ("draft", "Novo"),
    ("done", "Processado"),
    ("error", "Erro no Processamento")
]

TIPO_OPERACAO_CNAB = {
    "C": "Lançamento a Crédito",
    "D": "Lançamento a Débito",
    "E": "Extrato para Conciliação",
    "G": "Extrato para Gestão de Caixa",
    "I": "Informações de Títulos Capturados do Próprio Banco",
    "R": "Arquivo Remessa",
    "T": "Arquivo Retorno",
}
RETORNO_400_CONFIRMADA = [2]

RETORNO_400_REJEITADA = [3]

RETORNO_400_LIQUIDACAO = [
    6,
    # 7, TODO: Implementar a baixa parcial;
    8,
]

RETORNO_400_BAIXA = [9, 10]

RETORNOS_TRATADOS = [
    RETORNO_400_CONFIRMADA,
    RETORNO_400_REJEITADA,
    RETORNO_400_LIQUIDACAO,
    RETORNO_400_BAIXA,
]

# COD_REGISTROS_REJEITADOS_CNAB400 -> USADO QUANDO HA CODIGO DE OCORRENCIA 03
# NA POSIÇÃO 109-110
COD_REGISTROS_REJEITADOS_CNAB400 = {
    3: "AG. COBRADORA - CEP SEM ATENDIMENTO DE PROTESTO NO MOMENTO",
    4: "ESTADO - SIGLA DO ESTADO INVÁLIDA",
    5: "DATA VENCIMENTO - PRAZO DA OPERAÇÃO MENOR QUE PRAZO MÍNIMO OU MAIOR QUE O MÁXIMO",  # noqa
    7: "VALOR DO TÍTULO - VALOR DO TÍTULO MAIOR QUE 10.000.000,00",
    8: "NOME DO PAGADOR - NÃO INFORMADO OU DESLOCADO",
    9: "AGENCIA/CONTA - AGÊNCIA ENCERRADA",
    10: "LOGRADOURO - NÃO INFORMADO OU DESLOCADO",
    11: "CEP - CEP NÃO NUMÉRICO OU CEP INVÁLIDO",
    12: "SACADOR / AVALISTA - NOME NÃO INFORMADO OU DESLOCADO (BANCOS CORRESPONDENTES)",  # noqa
    13: "ESTADO/CEP - CEP INCOMPATÍVEL COM A SIGLA DO ESTADO",
    14: "NOSSO NÚMERO - NOSSO NÚMERO JÁ REGISTRADO NO CADASTRO DO BANCO OU FORA DA FAIXA",  # noqa
    15: "NOSSO NÚMERO - NOSSO NÚMERO EM DUPLICIDADE NO MESMO MOVIMENTO",
    18: "DATA DE ENTRADA - DATA DE ENTRADA INVÁLIDA PARA OPERAR COM ESTA CARTEIRA",
    19: "OCORRÊNCIA - OCORRÊNCIA INVÁLIDA",
    21: "AG. COBRADORA - CARTEIRA NÃO ACEITA DEPOSITÁRIA CORRESPONDENTE ESTADO DA AGÊNCIA DIFERENTE DO ESTADO DO PAGADOR AG. COBRADORA NÃO CONSTA NO CADASTRO OU ENCERRANDO",  # noqa
    22: "CARTEIRA - CARTEIRA NÃO PERMITIDA (NECESSÁRIO CADASTRAR FAIXA LIVRE)",
    26: "AGÊNCIA/CONTA - AGÊNCIA/CONTA NÃO LIBERADA PARA OPERAR COM COBRANÇA",
    27: "CNPJ INAPTO - CNPJ DO BENEFICIÁRIO INAPTO DEVOLUÇÃO DE TÍTULO EM GARANTIA",
    29: "CÓDIGO EMPRESA - CATEGORIA DA CONTA INVÁLIDA",
    30: "ENTRADA BLOQUEADA - ENTRADAS BLOQUEADAS, CONTA SUSPENSA EM COBRANÇA",
    31: "AGÊNCIA/CONTA - CONTA NÃO TEM PERMISSÃO PARA PROTESTAR (CONTATE SEU GERENTE)",
    35: "VALOR DO IOF - IOF MAIOR QUE 5%",
    36: "QTDADE DE MOEDA - QUANTIDADE DE MOEDA INCOMPATÍVEL COM VALOR DO TÍTULO",
    37: "CNPJ/CPF DO PAGADOR - NÃO NUMÉRICO OU IGUAL A ZEROS",
    42: "NOSSO NÚMERO - NOSSO NÚMERO FORA DE FAIXA",
    52: "AG. COBRADORA - EMPRESA NÃO ACEITA BANCO CORRESPONDENTE",
    53: "AG. COBRADORA - EMPRESA NÃO ACEITA BANCO CORRESPONDENTE - COBRANÇA MENSAGEM",
    54: "DATA DE VENCTO - BANCO CORRESPONDENTE - TÍTULO COM VENCIMENTO INFERIOR A 15 DIAS",  # noqa
    55: "DEP/BCO CORRESP - CEP NÃO PERTENCE À DEPOSITÁRIA INFORMADA",
    56: "DT VENCTO/BCO CORRESP - VENCTO SUPERIOR A 180 DIAS DA DATA DE ENTRADA",
    57: "DATA DE VENCTO - CEP SÓ DEPOSITÁRIA BCO DO BRASIL COM VENCTO INFERIOR A 8 DIAS",  # noqa
    60: "ABATIMENTO - VALOR DO ABATIMENTO INVÁLIDO",
    61: "JUROS DE MORA - JUROS DE MORA MAIOR QUE O PERMITIDO",
    62: "DESCONTO - VALOR DO DESCONTO MAIOR QUE VALOR DO TÍTULO",
    63: "DESCONTO DE ANTECIPAÇÃO - VALOR DA IMPORTÂNCIA POR DIA DE DESCONTO (IDD) NÃO PERMITIDO",  # noqa
    64: "DATA DE EMISSÃO - DATA DE EMISSÃO DO TÍTULO INVÁLIDA",
    65: "TAXA FINANCTO - TAXA INVÁLIDA (VENDOR)",
    66: "DATA DE VENCTO - INVALIDA/FORA DE PRAZO DE OPERAÇÃO (MÍNIMO OU MÁXIMO)",
    67: "VALOR/QTIDADE - VALOR DO TÍTULO/QUANTIDADE DE MOEDA INVÁLIDO",
    68: "CARTEIRA - CARTEIRA INVÁLIDA OU NÃO CADASTRADA NO INTERCÂMBIO DA COBRANÇA",
    69: "CARTEIRA - CARTEIRA INVÁLIDA PARA TÍTULOS COM RATEIO DE CRÉDITO",
    70: "AGÊNCIA/CONTA - BENEFICIÁRIO NÃO CADASTRADO PARA FAZER RATEIO DE CRÉDITO",
    78: "AGÊNCIA/CONTA - DUPLICIDADE DE AGÊNCIA/CONTA BENEFICIÁRIA DO RATEIO DE CRÉDITO",  # noqa
    80: "AGÊNCIA/CONTA - QUANTIDADE DE CONTAS BENEFICIÁRIAS DO RATEIO MAIOR DO QUE O PERMITIDO (MÁXIMO DE 30 CONTAS POR TÍTULO)",  # noqa
    81: "AGÊNCIA/CONTA - CONTA PARA RATEIO DE CRÉDITO INVÁLIDA / NÃO PERTENCE AO ITAÚ",
    82: "DESCONTO/ABATI-MENTO - DESCONTO/ABATIMENTO NÃO PERMITIDO PARA TÍTULOS COM RATEIO DE CRÉDITO",  # noqa
    83: "VALOR DO TÍTULO - VALOR DO TÍTULO MENOR QUE A SOMA DOS VALORES ESTIPULADOS PARA RATEIO",  # noqa
    84: "AGÊNCIA/CONTA - AGÊNCIA/CONTA BENEFICIÁRIA DO RATEIO É A CENTRALIZADORA DE CRÉDITO DO BENEFICIÁRIO",  # noqa
    85: "AGÊNCIA/CONTA - AGÊNCIA/CONTA DO BENEFICIÁRIO É CONTRATUAL / RATEIO DE CRÉDITO NÃO PERMITIDO",  # noqa
    86: "TIPO DE VALOR - CÓDIGO DO TIPO DE VALOR INVÁLIDO / NÃO PREVISTO PARA TÍTULOS COM RATEIO DE CRÉDITO",  # noqa
    87: "AGÊNCIA/CONTA - REGISTRO TIPO 4 SEM INFORMAÇÃO DE AGÊNCIAS/CONTAS BENEFICIÁRIAS DO RATEIO",  # noqa
    90: "NRO DA LINHA - COBRANÇA MENSAGEM - NÚMERO DA LINHA DA MENSAGEM INVÁLIDO OU QUANTIDADE DE LINHAS EXCEDIDAS",  # noqa
    97: "SEM MENSAGEM - COBRANÇA MENSAGEM SEM MENSAGEM (SÓ DE CAMPOS FIXOS), PORÉM COM REGISTRO DO TIPO 7 OU 8",  # noqa
    98: "FLASH INVÁLIDO - REGISTRO MENSAGEM SEM FLASH CADASTRADO OU FLASH INFORMADO DIFERENTE DO CADASTRADO",  # noqa
    99: "FLASH INVÁLIDO - CONTA DE COBRANÇA COM FLASH CADASTRADO E SEM REGISTRO DE MENSAGEM CORRESPONDENTE",  # noqa
}


CODIGO_OCORRENCIAS_CNAB200 = {
    2: "ENTRADA CONFIRMADA COM POSSIBILIDADE DE MENSAGEM (NOTA 20 – TABELA 10)",  # noqa
    3: "ENTRADA REJEITADA (NOTA 20 – TABELA 1)",  # noqa
    4: "ALTERAÇÃO DE DADOS – NOVA ENTRADA OU ALTERAÇÃO/EXCLUSÃO DE DADOS ACATADA",  # noqa
    5: "ALTERAÇÃO DE DADOS – BAIXA",
    6: "LIQUIDAÇÃO NORMAL",
    7: "LIQUIDAÇÃO PARCIAL – COBRANÇA INTELIGENTE (B2B)",
    8: "LIQUIDAÇÃO EM CARTÓRIO",
    9: "BAIXA SIMPLES",
    10: "BAIXA POR TER SIDO LIQUIDADO",
    11: "EM SER (SÓ NO RETORNO MENSAL)",
    12: "ABATIMENTO CONCEDIDO",
    13: "ABATIMENTO CANCELADO",
    14: "VENCIMENTO ALTERADO",
    15: "BAIXAS REJEITADAS (NOTA 20 – TABELA 4)",
    16: "INSTRUÇÕES REJEITADAS (NOTA 20 – TABELA 3)",
    17: "ALTERAÇÃO/EXCLUSÃO DE DADOS REJEITADOS (NOTA 20 – TABELA 2)",
    18: "COBRANÇA CONTRATUAL – INSTRUÇÕES/ALTERAÇÕES REJEITADAS/PENDENTES (NOTA 20 – TABELA 5)",  # noqa
    19: "CONFIRMA RECEBIMENTO DE INSTRUÇÃO DE PROTESTO",
    20: "CONFIRMA RECEBIMENTO DE INSTRUÇÃO DE SUSTAÇÃO DE PROTESTO /TARIFA",
    21: "CONFIRMA RECEBIMENTO DE INSTRUÇÃO DE NÃO PROTESTAR",
    23: "TÍTULO ENVIADO A CARTÓRIO/TARIFA",
    24: "INSTRUÇÃO DE PROTESTO REJEITADA / SUSTADA / PENDENTE (NOTA 20 – TABELA 7)",  # noqa
    25: "ALEGAÇÕES DO PAGADOR (NOTA 20 – TABELA 6)",
    26: "TARIFA DE AVISO DE COBRANÇA",
    27: "TARIFA DE EXTRATO POSIÇÃO (B40X)",
    28: "TARIFA DE RELAÇÃO DAS LIQUIDAÇÕES",
    29: "TARIFA DE MANUTENÇÃO DE TÍTULOS VENCIDOS",
    30: "DÉBITO MENSAL DE TARIFAS (PARA ENTRADAS E BAIXAS)",
    32: "BAIXA POR TER SIDO PROTESTADO",
    33: "CUSTAS DE PROTESTO",
    34: "CUSTAS DE SUSTAÇÃO",
    35: "CUSTAS DE CARTÓRIO DISTRIBUIDOR",
    36: "CUSTAS DE EDITAL",
    37: "TARIFA DE EMISSÃO DE BOLETO/TARIFA DE ENVIO DE DUPLICATA",
    38: "TARIFA DE INSTRUÇÃO",
    39: "TARIFA DE OCORRÊNCIAS",
    40: "TARIFA MENSAL DE EMISSÃO DE BOLETO/TARIFA MENSAL DE ENVIO DE DUPLICATA",  # noqa
    41: "DÉBITO MENSAL DE TARIFAS – EXTRATO DE POSIÇÃO (B4EP/B4OX)",
    42: "DÉBITO MENSAL DE TARIFAS – OUTRAS INSTRUÇÕES",
    43: "DÉBITO MENSAL DE TARIFAS – MANUTENÇÃO DE TÍTULOS VENCIDOS",
    44: "DÉBITO MENSAL DE TARIFAS – OUTRAS OCORRÊNCIAS",
    45: "DÉBITO MENSAL DE TARIFAS – PROTESTO",
    46: "DÉBITO MENSAL DE TARIFAS – SUSTAÇÃO DE PROTESTO",
    47: "BAIXA COM TRANSFERÊNCIA PARA DESCONTO",
    48: "CUSTAS DE SUSTAÇÃO JUDICIAL",
    51: "TARIFA MENSAL REF A ENTRADAS BANCOS CORRESPONDENTES NA CARTEIRA",
    52: "TARIFA MENSAL BAIXAS NA CARTEIRA",
    53: "TARIFA MENSAL BAIXAS EM BANCOS CORRESPONDENTES NA CARTEIRA",
    54: "TARIFA MENSAL DE LIQUIDAÇÕES NA CARTEIRA",
    55: "TARIFA MENSAL DE LIQUIDAÇÕES EM BANCOS CORRESPONDENTES NA CARTEIRA",
    56: "CUSTAS DE IRREGULARIDADE",
    57: "INSTRUÇÃO CANCELADA (NOTA 20 – TABELA 8)",
    59: "BAIXA POR CRÉDITO EM C/C ATRAVÉS DO SISPAG",
    60: "ENTRADA REJEITADA CARNÊ (NOTA 20 – TABELA 1)",
    61: "TARIFA EMISSÃO AVISO DE MOVIMENTAÇÃO DE TÍTULOS (2154)",
    62: "DÉBITO MENSAL DE TARIFA – AVISO DE MOVIMENTAÇÃO DE TÍTULOS (2154)",
    63: "TÍTULO SUSTADO JUDICIALMENTE",
    64: "ENTRADA CONFIRMADA COM RATEIO DE CRÉDITO",
    65: "PAGAMENTO COM CHEQUE – AGUARDANDO COMPENSAÇÃO",
    69: "CHEQUE DEVOLVIDO (NOTA 20 – TABELA 9)",
    71: "ENTRADA REGISTRADA, AGUARDANDO AVALIAÇÃO",
    72: "BAIXA POR CRÉDITO EM C/C ATRAVÉS DO SISPAG SEM TÍTULO CORRESPONDENTE",
    73: "CONFIRMAÇÃO DE ENTRADA NA COBRANÇA SIMPLES – ENTRADA NÃO ACEITA NA COBRANÇA CONTRATUAL",  # noqa
    74: "INSTRUÇÃO DE NEGATIVAÇÃO EXPRESSA REJEITADA (NOTA 20 – TABELA 11)",
    75: "CONFIRMAÇÃO DE RECEBIMENTO DE INSTRUÇÃO DE ENTRADA EM NEGATIVAÇÃO EXPRESSA",  # noqa
    76: "CHEQUE COMPENSADO",
    77: "CONFIRMAÇÃO DE RECEBIMENTO DE INSTRUÇÃO DE EXCLUSÃO DE ENTRADA EM NEGATIVAÇÃO EXPRESSA",  # noqa
    78: "CONFIRMAÇÃO DE RECEBIMENTO DE INSTRUÇÃO DE CANCELAMENTO DE NEGATIVAÇÃO EXPRESSA",  # noqa
    79: "NEGATIVAÇÃO EXPRESSA INFORMACIONAL (NOTA 20 – TABELA 12)",
    80: "CONFIRMAÇÃO DE ENTRADA EM NEGATIVAÇÃO EXPRESSA – TARIFA",
    82: "CONFIRMAÇÃO DO CANCELAMENTO DE NEGATIVAÇÃO EXPRESSA – TARIFA",
    83: "CONFIRMAÇÃO DE EXCLUSÃO DE ENTRADA EM NEGATIVAÇÃO EXPRESSA POR LIQUIDAÇÃO – TARIFA",  # noqa
    85: "TARIFA POR BOLETO (ATÉ 03 ENVIOS) COBRANÇA ATIVA ELETRÔNICA",
    86: "TARIFA EMAIL COBRANÇA ATIVA ELETRÔNICA",
    87: "TARIFA SMS COBRANÇA ATIVA ELETRÔNICA",
    88: "TARIFA MENSAL POR BOLETO (ATÉ 03 ENVIOS) COBRANÇA ATIVA ELETRÔNICA",
    89: "TARIFA MENSAL EMAIL COBRANÇA ATIVA ELETRÔNICA",
    90: "TARIFA MENSAL SMS COBRANÇA ATIVA ELETRÔNICA",
    91: "TARIFA MENSAL DE EXCLUSÃO DE ENTRADA DE NEGATIVAÇÃO EXPRESSA",
    92: "TARIFA MENSAL DE CANCELAMENTO DE NEGATIVAÇÃO EXPRESSA",
    93: "TARIFA MENSAL DE EXCLUSÃO DE NEGATIVAÇÃO EXPRESSA POR LIQUIDAÇÃO",
}

STR_EVENTO_FORMAT = "%d%m%y"
