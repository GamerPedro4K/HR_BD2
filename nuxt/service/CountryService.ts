export interface Country {
  name: string;
  code: string;
}

export const CountryService = {
  getData(): Country[] {
    return [
      { name: 'Afeganistão', code: 'AF' },
      { name: 'Albânia', code: 'AL' },
      { name: 'Argélia', code: 'DZ' },
      { name: 'Samoa Americana', code: 'AS' },
      { name: 'Andorra', code: 'AD' },
      { name: 'Angola', code: 'AO' },
      { name: 'Anguila', code: 'AI' },
      { name: 'Antártica', code: 'AQ' },
      { name: 'Antígua e Barbuda', code: 'AG' },
      { name: 'Argentina', code: 'AR' },
      { name: 'Arménia', code: 'AM' },
      { name: 'Aruba', code: 'AW' },
      { name: 'Austrália', code: 'AU' },
      { name: 'Áustria', code: 'AT' },
      { name: 'Azerbaijão', code: 'AZ' },
      { name: 'Bahamas', code: 'BS' },
      { name: 'Barém', code: 'BH' },
      { name: 'Bangladeche', code: 'BD' },
      { name: 'Barbados', code: 'BB' },
      { name: 'Bielorrússia', code: 'BY' },
      { name: 'Bélgica', code: 'BE' },
      { name: 'Belize', code: 'BZ' },
      { name: 'Benim', code: 'BJ' },
      { name: 'Bermudas', code: 'BM' },
      { name: 'Butão', code: 'BT' },
      { name: 'Bolívia', code: 'BO' },
      { name: 'Bósnia e Herzegovina', code: 'BA' },
      { name: 'Botsuana', code: 'BW' },
      { name: 'Ilha Bouvet', code: 'BV' },
      { name: 'Brasil', code: 'BR' },
      { name: 'Território Britânico do Oceano Índico', code: 'IO' },
      { name: 'Brunei', code: 'BN' },
      { name: 'Bulgária', code: 'BG' },
      { name: 'Burquina Faso', code: 'BF' },
      { name: 'Burúndi', code: 'BI' },
      { name: 'Camboja', code: 'KH' },
      { name: 'Camarões', code: 'CM' },
      { name: 'Canadá', code: 'CA' },
      { name: 'Cabo Verde', code: 'CV' },
      { name: 'Ilhas Caimão', code: 'KY' },
      { name: 'República Centro-Africana', code: 'CF' },
      { name: 'Chade', code: 'TD' },
      { name: 'Chile', code: 'CL' },
      { name: 'China', code: 'CN' },
      { name: 'Ilha do Natal', code: 'CX' },
      { name: 'Ilhas Cocos (Keeling)', code: 'CC' },
      { name: 'Colômbia', code: 'CO' },
      { name: 'Comores', code: 'KM' },
      { name: 'Congo', code: 'CG' },
      { name: 'Congo, República Democrática do', code: 'CD' },
      { name: 'Ilhas Cook', code: 'CK' },
      { name: 'Costa Rica', code: 'CR' },
      { name: 'Costa do Marfim', code: 'CI' },
      { name: 'Croácia', code: 'HR' },
      { name: 'Cuba', code: 'CU' },
      { name: 'Chipre', code: 'CY' },
      { name: 'República Checa', code: 'CZ' },
      { name: 'Dinamarca', code: 'DK' },
      { name: 'Jibuti', code: 'DJ' },
      { name: 'Dominica', code: 'DM' },
      { name: 'República Dominicana', code: 'DO' },
      { name: 'Equador', code: 'EC' },
      { name: 'Egito', code: 'EG' },
      { name: 'El Salvador', code: 'SV' },
      { name: 'Guiné Equatorial', code: 'GQ' },
      { name: 'Eritreia', code: 'ER' },
      { name: 'Estónia', code: 'EE' },
      { name: 'Etiópia', code: 'ET' },
      { name: 'Ilhas Falkland (Malvinas)', code: 'FK' },
      { name: 'Ilhas Faroé', code: 'FO' },
      { name: 'Fiji', code: 'FJ' },
      { name: 'Finlândia', code: 'FI' },
      { name: 'França', code: 'FR' },
      { name: 'Guiana Francesa', code: 'GF' },
      { name: 'Polinésia Francesa', code: 'PF' },
      { name: 'Territórios Franceses do Sul', code: 'TF' },
      { name: 'Gabão', code: 'GA' },
      { name: 'Gâmbia', code: 'GM' },
      { name: 'Geórgia', code: 'GE' },
      { name: 'Alemanha', code: 'DE' },
      { name: 'Gana', code: 'GH' },
      { name: 'Gibraltar', code: 'GI' },
      { name: 'Grécia', code: 'GR' },
      { name: 'Gronelândia', code: 'GL' },
      { name: 'Granada', code: 'GD' },
      { name: 'Guadalupe', code: 'GP' },
      { name: 'Guão', code: 'GU' },
      { name: 'Guatemala', code: 'GT' },
      { name: 'Guernsey', code: 'GG' },
      { name: 'Guiné', code: 'GN' },
      { name: 'Guiné-Bissau', code: 'GW' },
      { name: 'Guiana', code: 'GY' },
      { name: 'Haiti', code: 'HT' },
      { name: 'Ilha Heard e Ilhas McDonald', code: 'HM' },
      { name: 'Vaticano', code: 'VA' },
      { name: 'Honduras', code: 'HN' },
      { name: 'Hong Kong', code: 'HK' },
      { name: 'Hungria', code: 'HU' },
      { name: 'Islândia', code: 'IS' },
      { name: 'Índia', code: 'IN' },
      { name: 'Indonésia', code: 'ID' },
      { name: 'Irão', code: 'IR' },
      { name: 'Iraque', code: 'IQ' },
      { name: 'Irlanda', code: 'IE' },
      { name: 'Ilha de Man', code: 'IM' },
      { name: 'Israel', code: 'IL' },
      { name: 'Itália', code: 'IT' },
      { name: 'Jamaica', code: 'JM' },
      { name: 'Japão', code: 'JP' },
      { name: 'Jersey', code: 'JE' },
      { name: 'Jordânia', code: 'JO' },
      { name: 'Cazaquistão', code: 'KZ' },
      { name: 'Quénia', code: 'KE' },
      { name: 'Quiribáti', code: 'KI' },
      { name: 'Coreia do Norte', code: 'KP' },
      { name: 'Coreia do Sul', code: 'KR' },
      { name: 'Kuwait', code: 'KW' },
      { name: 'Quirguizistão', code: 'KG' },
      { name: 'Laos', code: 'LA' },
      { name: 'Letónia', code: 'LV' },
      { name: 'Líbano', code: 'LB' },
      { name: 'Lesoto', code: 'LS' },
      { name: 'Libéria', code: 'LR' },
      { name: 'Líbia', code: 'LY' },
      { name: 'Listenstaine', code: 'LI' },
      { name: 'Lituânia', code: 'LT' },
      { name: 'Luxemburgo', code: 'LU' },
      { name: 'Macau', code: 'MO' },
      { name: 'Macedónia do Norte', code: 'MK' },
      { name: 'Madagáscar', code: 'MG' },
      { name: 'Maláui', code: 'MW' },
      { name: 'Malásia', code: 'MY' },
      { name: 'Maldivas', code: 'MV' },
      { name: 'Mali', code: 'ML' },
      { name: 'Malta', code: 'MT' },
      { name: 'Ilhas Marshall', code: 'MH' },
      { name: 'Martinica', code: 'MQ' },
      { name: 'Mauritânia', code: 'MR' },
      { name: 'Maurícia', code: 'MU' },
      { name: 'Mayotte', code: 'YT' },
      { name: 'México', code: 'MX' },
      { name: 'Micronésia', code: 'FM' },
      { name: 'Moldávia', code: 'MD' },
      { name: 'Mónaco', code: 'MC' },
      { name: 'Mongólia', code: 'MN' },
      { name: 'Montserrat', code: 'MS' },
      { name: 'Marrocos', code: 'MA' },
      { name: 'Moçambique', code: 'MZ' },
      { name: 'Mianmar', code: 'MM' },
      { name: 'Namíbia', code: 'NA' },
      { name: 'Nauru', code: 'NR' },
      { name: 'Nepal', code: 'NP' },
      { name: 'Países Baixos', code: 'NL' },
      { name: 'Antilhas Neerlandesas', code: 'AN' },
      { name: 'Nova Caledónia', code: 'NC' },
      { name: 'Nova Zelândia', code: 'NZ' },
      { name: 'Nicarágua', code: 'NI' },
      { name: 'Níger', code: 'NE' },
      { name: 'Nigéria', code: 'NG' },
      { name: 'Niue', code: 'NU' },
      { name: 'Ilha Norfolk', code: 'NF' },
      { name: 'Ilhas Marianas do Norte', code: 'MP' },
      { name: 'Noruega', code: 'NO' },
      { name: 'Omã', code: 'OM' },
      { name: 'Paquistão', code: 'PK' },
      { name: 'Palau', code: 'PW' },
      { name: 'Palestina', code: 'PS' },
      { name: 'Panamá', code: 'PA' },
      { name: 'Papua-Nova Guiné', code: 'PG' },
      { name: 'Paraguai', code: 'PY' },
      { name: 'Peru', code: 'PE' },
      { name: 'Filipinas', code: 'PH' },
      { name: 'Ilhas Pitcairn', code: 'PN' },
      { name: 'Polónia', code: 'PL' },
      { name: 'Portugal', code: 'PT' },
      { name: 'Porto Rico', code: 'PR' },
      { name: 'Catar', code: 'QA' },
      { name: 'Reunião', code: 'RE' },
      { name: 'Roménia', code: 'RO' },
      { name: 'Rússia', code: 'RU' },
      { name: 'Ruanda', code: 'RW' },
      { name: 'Santa Helena', code: 'SH' },
      { name: 'São Cristóvão e Neves', code: 'KN' },
      { name: 'Santa Lúcia', code: 'LC' },
      { name: 'Saint-Pierre e Miquelon', code: 'PM' },
      { name: 'São Vicente e Granadinas', code: 'VC' },
      { name: 'Samoa', code: 'WS' },
      { name: 'São Marino', code: 'SM' },
      { name: 'São Tomé e Príncipe', code: 'ST' },
      { name: 'Arábia Saudita', code: 'SA' },
      { name: 'Senegal', code: 'SN' },
      { name: 'Sérvia e Montenegro', code: 'CS' },
      { name: 'Seicheles', code: 'SC' },
      { name: 'Serra Leoa', code: 'SL' },
      { name: 'Singapura', code: 'SG' },
      { name: 'Eslováquia', code: 'SK' },
      { name: 'Eslovénia', code: 'SI' },
      { name: 'Ilhas Salomão', code: 'SB' },
      { name: 'Somália', code: 'SO' },
      { name: 'África do Sul', code: 'ZA' },
      { name: 'Geórgia do Sul e Ilhas Sandwich do Sul', code: 'GS' },
      { name: 'Espanha', code: 'ES' },
      { name: 'Sri Lanca', code: 'LK' },
      { name: 'Sudão', code: 'SD' },
      { name: 'Suriname', code: 'SR' },
      { name: 'Svalbard e Jan Mayen', code: 'SJ' },
      { name: 'Essuatíni', code: 'SZ' },
      { name: 'Suécia', code: 'SE' },
      { name: 'Suíça', code: 'CH' },
      { name: 'Síria', code: 'SY' },
      { name: 'Taiwan', code: 'TW' },
      { name: 'Tajiquistão', code: 'TJ' },
      { name: 'Tanzânia', code: 'TZ' },
      { name: 'Tailândia', code: 'TH' },
      { name: 'Timor-Leste', code: 'TL' },
      { name: 'Togo', code: 'TG' },
      { name: 'Toquelau', code: 'TK' },
      { name: 'Tonga', code: 'TO' },
      { name: 'Trindade e Tobago', code: 'TT' },
      { name: 'Tunísia', code: 'TN' },
      { name: 'Turquia', code: 'TR' },
      { name: 'Turquemenistão', code: 'TM' },
      { name: 'Ilhas Turcas e Caicos', code: 'TC' },
      { name: 'Tuvalu', code: 'TV' },
      { name: 'Uganda', code: 'UG' },
      { name: 'Ucrânia', code: 'UA' },
      { name: 'Emirados Árabes Unidos', code: 'AE' },
      { name: 'Reino Unido', code: 'GB' },
      { name: 'Estados Unidos', code: 'US' },
      { name: 'Ilhas Menores Distantes dos EUA', code: 'UM' },
      { name: 'Uruguai', code: 'UY' },
      { name: 'Uzbequistão', code: 'UZ' },
      { name: 'Vanuatu', code: 'VU' },
      { name: 'Venezuela', code: 'VE' },
      { name: 'Vietname', code: 'VN' },
      { name: 'Ilhas Virgens Britânicas', code: 'VG' },
      { name: 'Ilhas Virgens dos EUA', code: 'VI' },
      { name: 'Wallis e Futuna', code: 'WF' },
      { name: 'Saara Ocidental', code: 'EH' },
      { name: 'Iémen', code: 'YE' },
      { name: 'Zâmbia', code: 'ZM' },
      { name: 'Zimbabué', code: 'ZW' }
    ];
  },

  getCountries(): Promise<Country[]> {
    return Promise.resolve(this.getData());
  }
};
