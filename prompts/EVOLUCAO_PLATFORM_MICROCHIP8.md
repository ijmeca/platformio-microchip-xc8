Você está trabalhando em uma plataforma customizada do PlatformIO chamada:

platform-microchip8

Objetivo geral:
Criar uma plataforma PlatformIO funcional e profissional para microcontroladores Microchip PIC de 8 bits, inicialmente das famílias:

- PIC12F
- PIC16F
- PIC18F

A plataforma deve utilizar o compilador oficial MPLAB XC8 instalado na máquina do usuário e os Device Family Packs, DFPs, instalados pelo MPLAB X.

IMPORTANTE:
Não remova nem quebre a compilação que já está funcionando para o PIC12F675.

O comando abaixo já funciona dentro do exemplo:

pio run

O resultado atual é SUCCESS, utilizando:

XC8:
/Applications/microchip/xc8/v3.10/bin/xc8-cc

DFP do PIC12F675:
/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8

O PIC12F675 já compila corretamente com:

-mcpu=12F675
-mdfp=<caminho-do-dfp>

A implementação deve evoluir progressivamente, mantendo compatibilidade com esse funcionamento.

==================================================
1. ESTRUTURA ESPERADA
==================================================

Organize o repositório desta forma:

platform-microchip8/
├── boards/
├── builder/
│   ├── main.py
│   └── frameworks/
│       └── xc8.py
├── examples/
│   ├── pic12f675-blink/
│   │   ├── platformio.ini
│   │   └── src/
│   │       └── main.c
│   ├── pic16f877a-blink/
│   │   ├── platformio.ini
│   │   └── src/
│   │       └── main.c
│   └── pic18f4550-blink/
│       ├── platformio.ini
│       └── src/
│           └── main.c
├── scripts/
│   ├── detect_xc8.py
│   ├── detect_dfp.py
│   ├── generate_boards.py
│   └── validate_boards.py
├── tests/
│   ├── test_detection.py
│   ├── test_board_generation.py
│   └── test_manifests.py
├── platform.json
├── platform.py
├── README.md
├── LICENSE
└── .gitignore

Não crie um pacote separado framework-xc8 neste momento, salvo se for realmente necessário. Primeiro mantenha a integração XC8 dentro da própria plataforma.

==================================================
2. REQUISITOS FUNDAMENTAIS
==================================================

A plataforma deve:

1. Continuar compilando o PIC12F675 com pio run.
2. Localizar o XC8 automaticamente.
3. Permitir configurar manualmente o XC8.
4. Localizar automaticamente os DFPs instalados.
5. Permitir configurar manualmente o DFP.
6. selecionar o DFP correto de acordo com o microcontrolador.
7. Gerar firmware.elf e firmware.hex.
8. Fazer o PlatformIO reconhecer o firmware.hex como artefato.
9. Configurar corretamente o IntelliSense do VS Code.
10. Suportar arquivos .c, .h e bibliotecas do projeto.
11. Suportar múltiplos arquivos-fonte.
12. Gerar manifestos de placas automaticamente.
13. Implementar inicialmente as famílias PIC12F, PIC16F e PIC18F.
14. Não depender exclusivamente de caminhos fixos do macOS.
15. Retornar mensagens de erro claras e úteis.
16. Evitar comandos shell inseguros.
17. Usar subprocess com lista de argumentos, sem shell=True.
18. Ser compatível com Python 3.9 ou superior.

==================================================
3. DETECÇÃO DO XC8
==================================================

Implemente scripts/detect_xc8.py.

A resolução do XC8 deve respeitar esta prioridade:

1. Opção custom_xc8_path do platformio.ini.
2. Variável de ambiente XC8_PATH.
3. Comando xc8-cc disponível no PATH.
4. Busca nos diretórios conhecidos do sistema.

macOS:
- /Applications/microchip/xc8/v*/bin/xc8-cc

Linux:
- /opt/microchip/xc8/v*/bin/xc8-cc
- /usr/local/microchip/xc8/v*/bin/xc8-cc

Windows:
- C:\Program Files\Microchip\xc8\v*\bin\xc8-cc.exe
- C:\Program Files (x86)\Microchip\xc8\v*\bin\xc8-cc.exe

Quando houver múltiplas versões, selecionar a mais recente semanticamente.

Não ordenar versões como texto simples.

Exemplo incorreto:
v3.9 maior que v3.10

Exemplo correto:
3.10 maior que 3.9

A opção custom_xc8_path pode apontar para:

- raiz da instalação;
- pasta bin;
- executável xc8-cc.

O script deve normalizar essas possibilidades.

Retornar uma estrutura como:

{
    "executable": ".../xc8-cc",
    "root": ".../xc8/v3.10",
    "version": "3.10"
}

Se não encontrar o XC8, apresentar uma mensagem indicando como definir:

custom_xc8_path = /caminho/para/xc8

ou:

export XC8_PATH=/caminho/para/xc8

==================================================
4. DETECÇÃO DOS DFPs
==================================================

Implemente scripts/detect_dfp.py.

Os DFPs podem estar em locais como:

macOS:
- /Applications/microchip/mplabx/v*/packs/Microchip/*_DFP/*/xc8
- ~/Library/microchip/packs/Microchip/*_DFP/*/xc8

Linux:
- /opt/microchip/mplabx/v*/packs/Microchip/*_DFP/*/xc8
- ~/.mchp_packs/Microchip/*_DFP/*/xc8

Windows:
- C:\Program Files\Microchip\MPLABX\v*\packs\Microchip\*_DFP\*\xc8
- %USERPROFILE%\.mchp_packs\Microchip\*_DFP\*\xc8

Também aceitar:

custom_dfp_path = /caminho/do/dfp/xc8

e:

custom_dfp_root = /diretorio/que/contem/os-packs

O valor passado para -mdfp deve ser a pasta xc8 do DFP, e não:

- xc8/pic/include
- xc8/pic/include/proc

Exemplo correto:

/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8

O detector deve inspecionar os headers existentes no DFP para determinar quais dispositivos são suportados.

Verificar principalmente:

<dfp>/pic/include/proc/

Exemplos de headers:

pic12f675.h
pic16f877a.h
pic18f4550.h

Normalizar os nomes dos dispositivos:

pic12f675.h -> 12F675
pic16f877a.h -> 16F877A
pic18f4550.h -> 18F4550

Não considerar arquivos genéricos que não representem um dispositivo.

Quando mais de um DFP suportar o mesmo dispositivo, usar a versão mais recente do pack.

A seleção deve ser feita pelo conteúdo real do pack, e não apenas pelo nome do diretório.

==================================================
5. BANCO/ÍNDICE DE DISPOSITIVOS
==================================================

Crie uma função que construa um índice em memória:

{
    "12F675": {
        "dfp_path": "...",
        "pack_name": "PIC10-12Fxxx_DFP",
        "pack_version": "1.3.46",
        "header": ".../pic12f675.h"
    },
    "16F877A": {
        ...
    },
    "18F4550": {
        ...
    }
}

Esse índice deve ser reutilizável pelo builder e pelo gerador de placas.

Opcionalmente, criar cache em:

~/.platformio/.cache/microchip8/

Mas a plataforma não deve falhar se o cache estiver ausente ou inválido.

==================================================
6. MANIFESTOS DAS PLACAS
==================================================

Implemente scripts/generate_boards.py.

O script deve percorrer todos os DFPs encontrados e criar arquivos JSON para dispositivos:

- PIC12F*
- PIC16F*
- PIC18F*

Ignorar, inicialmente:

- PIC10
- PIC24
- dsPIC
- PIC32
- AVR
- SAM
- dispositivos sem header XC8 válido

Nome dos arquivos:

boards/pic12f675.json
boards/pic16f877a.json
boards/pic18f4550.json

Todos em letras minúsculas.

Formato mínimo:

{
  "build": {
    "core": "pic8",
    "f_cpu": "4000000L",
    "mcu": "12F675"
  },
  "frameworks": [
    "xc8"
  ],
  "name": "Microchip PIC12F675",
  "upload": {
    "maximum_ram_size": 64,
    "maximum_size": 1024
  },
  "url": "https://www.microchip.com/en-us/product/PIC12F675",
  "vendor": "Microchip"
}

Entretanto, não invente valores de RAM e Flash.

Para os dispositivos em que os valores de memória não puderem ser obtidos de forma confiável, usar temporariamente:

"upload": {
    "maximum_ram_size": 0,
    "maximum_size": 0
}

Adicionar um campo próprio para indicar que o valor não foi determinado:

"microchip8": {
    "memory_detected": false,
    "family": "PIC12F"
}

Quando os dados forem encontrados no DFP, nos arquivos ATDF, XML ou metadata do pack, preencher os valores reais e definir:

"memory_detected": true

Não estimar memória com base apenas no nome do dispositivo.

O gerador não deve sobrescrever silenciosamente manifestos personalizados.

Adicionar opções:

python3 scripts/generate_boards.py --all
python3 scripts/generate_boards.py --family 12F
python3 scripts/generate_boards.py --family 16F
python3 scripts/generate_boards.py --family 18F
python3 scripts/generate_boards.py --device 16F877A
python3 scripts/generate_boards.py --force
python3 scripts/generate_boards.py --dry-run

O script deve informar:

- número de DFPs encontrados;
- número de dispositivos identificados;
- número de placas criadas;
- número de placas atualizadas;
- número de placas ignoradas;
- erros encontrados.

==================================================
7. VALIDAÇÃO DAS PLACAS
==================================================

Implemente scripts/validate_boards.py.

O script deve:

1. Abrir todos os arquivos boards/*.json.
2. Validar JSON.
3. Validar campos obrigatórios.
4. Garantir que build.mcu exista.
5. Garantir que frameworks contenha xc8.
6. Garantir que o nome do arquivo corresponda ao MCU.
7. Detectar MCUs duplicados.
8. Detectar manifestos vazios.
9. Retornar código diferente de zero em caso de erro.

Uso:

python3 scripts/validate_boards.py

==================================================
8. BUILDER PRINCIPAL
==================================================

Refatore builder/main.py.

Não mantenha toda a lógica no mesmo arquivo.

O builder deve:

1. Obter a placa com env.BoardConfig().
2. Ler build.mcu.
3. Encontrar o XC8.
4. Encontrar o DFP correto para o MCU.
5. Reunir todos os arquivos-fonte.
6. Construir o comando do XC8.
7. Gerar firmware.elf.
8. Confirmar que firmware.hex foi gerado.
9. Registrar os artefatos no PlatformIO.
10. Configurar as informações usadas pelo IntelliSense.

O builder deve encontrar fontes recursivamente:

src/**/*.c
lib/**/src/**/*.c
lib/**/*.c

Também incluir headers:

include/
src/
lib/**/include/
lib/**/src/

Não compilar arquivos duplicados.

Usar caminhos absolutos ou corretamente normalizados.

O comando deve seguir o princípio:

xc8-cc
-mcpu=<MCU>
-mdfp=<DFP>
-O1
-o <BUILD_DIR>/firmware.elf
<fontes>

Aceitar flags adicionais definidas pelo usuário:

build_flags =
    -DDEBUG
    -O2

Separar corretamente:

- defines;
- include paths;
- flags do compilador;
- flags do linker.

Não adicionar simultaneamente -O1 e -O2.

Se o usuário fornecer uma flag de otimização, ela deve substituir a otimização padrão.

Criar opção:

custom_xc8_optimization = 1

Valores permitidos inicialmente:

0
1
2
3
s

Converter para:

-O0
-O1
-O2
-O3
-Os

Se build_flags já contiver uma opção -O, ela tem prioridade.

==================================================
9. GERAÇÃO DO HEX
==================================================

O XC8 pode gerar o .hex como efeito da linkedição.

Após executar o compilador:

1. Procurar firmware.hex no BUILD_DIR.
2. Procurar também possíveis variantes produzidas pelo XC8.
3. Se necessário, usar a ferramenta apropriada fornecida pelo XC8 para converter o ELF em HEX.
4. Não usar ferramentas GNU incompatíveis com PIC sem verificar.
5. Falhar com mensagem clara caso o ELF exista, mas o HEX não seja gerado.

O artefato final esperado é:

.pio/build/<environment>/firmware.hex

Também manter:

.pio/build/<environment>/firmware.elf

Registrar firmware.hex como alvo de upload.

No fim de pio run, mostrar:

Firmware ELF: ...
Firmware HEX: ...

==================================================
10. INTELLISENSE E VS CODE
==================================================

Corrigir o alerta vermelho em:

#include <xc.h>

A solução principal não deve depender de o usuário criar manualmente:

.vscode/c_cpp_properties.json

Configure o ambiente SCons/PlatformIO com:

env.Append(
    CPPPATH=[...],
    CPPDEFINES=[...]
)

Adicionar aos include paths:

- <xc8_root>/pic/include
- <dfp_path>/pic/include
- <dfp_path>/pic/include/proc
- <project>/include
- <project>/src
- includes das bibliotecas

Adicionar defines compatíveis com o XC8 e o MCU.

Não inventar defines sem verificar os headers.

O define do dispositivo deve ser determinado de acordo com o padrão real esperado pelo XC8.

Exemplos que devem ser investigados:

__XC8
__XC
__12F675
_PIC12F675

O compilador deve continuar sendo a fonte de verdade.

Se necessário, executar um comando controlado de preprocessamento para descobrir os defines internos do XC8.

A integração deve permitir que o comando:

pio project init --ide vscode

ou a atualização do projeto PlatformIO gere configurações com os caminhos de include corretos.

Também disponibilizar um script opcional:

scripts/generate_vscode_config.py

Esse script poderá gerar:

.vscode/c_cpp_properties.json

apenas como fallback.

Ele não deve ser a única solução.

O arquivo fallback deve conter:

- compilerPath apontando para xc8-cc;
- includePath do XC8;
- includePath do DFP;
- includePath do projeto;
- defines detectados;
- cStandard c99.

Nunca gravar caminhos de um usuário específico diretamente no repositório.

==================================================
11. FRAMEWORK XC8
==================================================

Crie builder/frameworks/xc8.py.

Esse arquivo deve configurar:

- includes do XC8;
- includes do DFP;
- defines;
- flags padrão;
- integração de bibliotecas;
- dependências do framework.

O framework xc8 é apenas uma integração do compilador e dos headers oficiais.

Não copiar arquivos proprietários do XC8 ou dos DFPs para dentro do repositório.

Não redistribuir:

- xc.h;
- headers da Microchip;
- bibliotecas do XC8;
- executáveis do XC8;
- arquivos dos packs.

A plataforma deve apenas detectar instalações existentes.

==================================================
12. PLATFORM.JSON
==================================================

Atualize platform.json com uma estrutura válida.

Manter:

"name": "microchip8"

A classe em platform.py deve continuar sendo:

Microchip8Platform

Adicionar campos necessários para uma plataforma PlatformIO válida.

Exemplo de base:

{
  "name": "microchip8",
  "title": "Microchip PIC8",
  "description": "PlatformIO platform for Microchip PIC12F, PIC16F and PIC18F microcontrollers using MPLAB XC8.",
  "version": "0.2.0",
  "homepage": "https://github.com/ijmeca/platform-microchip8",
  "license": "MIT",
  "keywords": [
    "microchip",
    "pic",
    "pic8",
    "pic12",
    "pic16",
    "pic18",
    "xc8",
    "embedded"
  ],
  "engines": {
    "platformio": ">=6.1.0"
  }
}

Não declarar pacotes inexistentes.

Como o XC8 é instalado externamente, não adicioná-lo como pacote baixável da PlatformIO.

==================================================
13. PLATFORM.PY
==================================================

Manter a classe pública correta:

from platformio.public import PlatformBase

class Microchip8Platform(PlatformBase):
    ...

Adicionar apenas a lógica realmente necessária.

Não chamar super().configure_default_packages de forma que tente instalar pacotes inexistentes.

Como o XC8 e os DFPs são externos, a configuração padrão não deve exigir download de toolchains.

==================================================
14. CONFIGURAÇÕES DO PLATFORMIO.INI
==================================================

Suportar:

[env:pic12f675]
platform = file:///caminho/para/platform-microchip8
board = pic12f675
framework = xc8

custom_xc8_path = /Applications/microchip/xc8/v3.10
custom_dfp_path = /Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8

Também permitir omitir os dois caminhos quando a detecção automática funcionar:

[env:pic12f675]
platform = microchip8
board = pic12f675
framework = xc8

Adicionar suporte opcional:

custom_dfp_root =
custom_xc8_optimization = 1
custom_xc8_verbose = yes

Todas as opções customizadas devem ser lidas com:

env.GetProjectOption(...)

Não acessar diretamente configurações internas frágeis do PlatformIO.

==================================================
15. EXEMPLOS
==================================================

Manter ou criar exemplos para:

1. PIC12F675
2. PIC16F877A
3. PIC18F4550

Os códigos devem ser específicos para cada MCU.

Não reutilizar registradores de um MCU em outro sem verificar.

Cada exemplo deve:

- incluir <xc.h>;
- definir _XTAL_FREQ;
- possuir bits de configuração válidos;
- configurar os pinos corretamente;
- piscar um LED;
- compilar com o XC8 e DFP correspondentes.

O exemplo PIC12F675 já está funcional e deve permanecer equivalente ao atual.

Não inventar configurações dos exemplos PIC16F877A e PIC18F4550. Validar os nomes das configurações nos headers/DFPs instalados.

Se o DFP de um exemplo não estiver instalado, o script de teste deve marcar o exemplo como SKIPPED, não como falha geral.

==================================================
16. SUPORTE ÀS FAMÍLIAS
==================================================

A plataforma deve considerar suportados todos os dispositivos encontrados nos DFPs instalados cujos headers correspondam a:

pic12f*.h
pic16f*.h
pic18f*.h

Incluir variantes com letras e sufixos, por exemplo:

PIC12F675
PIC12F1840
PIC16F877A
PIC16F18855
PIC18F2550
PIC18F4550
PIC18F26K22
PIC18F47Q10

Não limitar a uma lista fixa.

O conjunto real de dispositivos será determinado pelos DFPs instalados na máquina.

O gerador deve ser capaz de criar centenas de manifestos sem precisar alterar o código para cada PIC.

==================================================
17. MENSAGENS DE ERRO
==================================================

Criar mensagens claras.

Exemplos:

XC8 não encontrado:
"MPLAB XC8 não encontrado. Instale o XC8 ou defina custom_xc8_path no platformio.ini."

DFP não encontrado:
"Nenhum DFP instalado oferece suporte ao MCU 16F877A. Instale o Device Family Pack correspondente no MPLAB X ou defina custom_dfp_path."

DFP incorreto:
"O DFP configurado não contém o header do MCU 18F4550."

MCU ausente:
"O manifesto da placa não definiu build.mcu."

HEX ausente:
"O XC8 gerou o ELF, mas o firmware.hex não foi encontrado."

Fonte ausente:
"Nenhum arquivo .c foi encontrado no diretório src ou nas bibliotecas."

==================================================
18. TESTES
==================================================

Criar testes para:

- ordenação semântica de versões;
- localização do XC8;
- normalização de caminhos;
- descoberta de DFPs;
- identificação do MCU por header;
- seleção do DFP mais recente;
- geração de board JSON;
- validação de manifestos;
- detecção de arquivos-fonte;
- não duplicação de fontes;
- comportamento quando XC8 não está instalado;
- comportamento quando o DFP não está instalado.

Os testes que não precisam do XC8 real devem usar diretórios temporários e dados simulados.

Não exigir instalação do XC8 para executar todos os testes unitários.

==================================================
19. README
==================================================

Atualize o README com:

- objetivo da plataforma;
- estado atual;
- famílias suportadas;
- pré-requisitos;
- instalação do XC8;
- instalação dos DFPs;
- configuração manual;
- detecção automática;
- geração das placas;
- compilação;
- localização do HEX;
- IntelliSense;
- problemas conhecidos;
- exemplos;
- limitações;
- próximos passos.

Explicar que a plataforma não redistribui componentes proprietários da Microchip.

Adicionar comandos reais:

python3 scripts/generate_boards.py --all
python3 scripts/validate_boards.py
pio run
pio run -v

==================================================
20. NÃO IMPLEMENTAR AINDA
==================================================

Não implementar nesta entrega, salvo se já houver infraestrutura segura e testada:

- upload com PICkit;
- IPE command line;
- MDB;
- debug;
- suporte a PIC10;
- suporte a AVR;
- suporte a PIC24;
- suporte a dsPIC;
- suporte a PIC32;
- instalação automática do XC8;
- download automático de DFPs;
- redistribuição de arquivos da Microchip.

Entretanto, deixar a arquitetura preparada para futura implementação de:

pio run -t upload

==================================================
21. CRITÉRIOS DE ACEITAÇÃO
==================================================

A entrega só será considerada concluída quando:

1. O projeto PIC12F675 atual continuar compilando com pio run.
2. O arquivo .pio/build/pic12f675/firmware.elf existir.
3. O arquivo .pio/build/pic12f675/firmware.hex existir.
4. #include <xc.h> deixar de aparecer como header ausente após atualização do projeto PlatformIO/VS Code.
5. O autocomplete conseguir localizar registradores do PIC12F675.
6. O gerador identificar PIC12F, PIC16F e PIC18F nos DFPs instalados.
7. Os manifestos gerados forem JSON válidos.
8. O script de validação retornar sucesso.
9. O código não possuir caminhos fixos para o usuário ijmeca.
10. Os caminhos atuais do usuário continuarem aceitos através do platformio.ini.
11. O código funcionar com múltiplos arquivos .c.
12. A compilação continuar usando o XC8 oficial.
13. Nenhum arquivo proprietário da Microchip for adicionado ao Git.
14. Os erros de XC8 e DFP ausentes forem legíveis.
15. A documentação explicar o processo completo.

==================================================
22. FORMA DA ENTREGA
==================================================

Antes de alterar arquivos:

1. Analise a estrutura atual do repositório.
2. Mostre quais arquivos já existem.
3. Identifique o que já funciona.
4. Não remova funcionalidades operacionais.
5. Crie um plano curto de implementação.

Depois implemente as alterações diretamente no repositório.

Ao terminar, entregue:

1. Resumo das mudanças.
2. Lista de arquivos criados.
3. Lista de arquivos alterados.
4. Comandos exatos para testar.
5. Resultado dos testes executados.
6. Dispositivos encontrados nos DFPs locais.
7. Quantidade de manifests gerados.
8. Limitações restantes.
9. Próxima etapa recomendada.

Execute, quando possível:

python3 -m compileall .
python3 scripts/validate_boards.py
python3 -m unittest discover tests
pio run -d examples/pic12f675-blink -v

Também teste os exemplos PIC16F877A e PIC18F4550 somente se seus DFPs estiverem instalados.

Não afirme que algo funciona sem executar o teste correspondente.

==================================================
23. CUIDADO COM A INSTALAÇÃO LOCAL DO PLATFORMIO
==================================================

A plataforma local é copiada para:

~/.platformio/platforms/microchip8

Ao testar alterações, pode ser necessário remover a cópia instalada:

rm -rf ~/.platformio/platforms/microchip8

E limpar o projeto:

rm -rf examples/pic12f675-blink/.pio

Não apague outras plataformas ou pacotes do PlatformIO.

==================================================
24. CONTEXTO DO AMBIENTE ATUAL
==================================================

Ambiente atualmente validado:

macOS Intel
Python 3.9
PlatformIO Core 6.x
XC8 3.10
MPLAB X 5.45

XC8:
/Applications/microchip/xc8/v3.10/bin/xc8-cc

Exemplo de DFP:
/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8

O seguinte comando já foi validado:

/Applications/microchip/xc8/v3.10/bin/xc8-cc \
  -mcpu=12F675 \
  -mdfp="/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8" \
  -O1 \
  -o build/firmware.elf \
  main.c

Resultado validado:

12F675 Memory Summary:
Program space: 46 de 1024 words
Data space: 5 de 64 bytes
Compilação concluída com sucesso.

Comece analisando os arquivos existentes e implemente a evolução de forma incremental, preservando o build já funcional do PIC12F675.