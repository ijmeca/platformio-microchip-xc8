CLAUDE.md

Objetivo principal

Instruções específicas para Claude Code

Antes de qualquer alteração, leia também o AGENTS.md existente na raiz dorepositório. As regras dos dois arquivos são complementares.

Quando houver diferença entre CLAUDE.md e AGENTS.md:

siga a regra mais restritiva;

preserve funcionalidades já existentes;

não altere a arquitetura sem solicitação;

não use a pasta ~/.platformio/platforms/microchip8 como fonte de edição.

Para este repositório, trabalhe sempre na pasta-fonte aberta pelo usuário,normalmente localizada em Documentos. A pasta dentro de .platformio é apenasuma cópia instalada para execução e testes.

Contexto específico: PlatformIO Microchip8

Este repositório implementa uma plataforma customizada do PlatformIO paramicrocontroladores Microchip PIC de 8 bits usando o compilador MPLAB XC8.

Famílias inicialmente suportadas:

PIC12F;

PIC16F;

PIC18F.

O build do PIC12F675 já funcional é a referência mínima de regressão.

Preserve suporte a:

custom_xc8_path;

custom_dfp_path;

detecção automática do XC8;

seleção do DFP correto por MCU;

geração de firmware.elf;

geração de firmware.hex;

integração do IntelliSense via PlatformIO/SCons;

múltiplos arquivos .c;

manifestos em boards/*.json.

Nunca copie ou versione componentes proprietários da Microchip, incluindo:

xc.h;

headers de dispositivos;

executáveis do XC8;

bibliotecas do XC8;

Device Family Packs;

arquivos do MPLAB X.

O argumento -mdfp deve apontar para a pasta xc8 do DFP, nunca paraxc8/pic/include ou xc8/pic/include/proc.

Não invente valores de RAM, Flash ou EEPROM. Obtenha esses dados apenas demetadados confiáveis dos packs instalados.

Reduzir leitura desnecessária de arquivos, economizar contexto e realizaralterações mínimas, seguras e verificáveis.

O Graphify é obrigatório para navegar pela estrutura do projeto.

1. Inicialização obrigatória

Antes de analisar ou modificar qualquer arquivo:

Localize a raiz do repositório.

Leia este AGENTS.md.

Verifique se o comando graphify está disponível.

Caso não esteja, instale o Graphify.

Gere ou atualize o grafo do projeto.

Não inicie modificações antes de concluir essas etapas.

2. Instalação do Graphify

Arquivos Markdown permitidos automaticamente:

✓ CLAUDE.md
✓ AGENTS.md

Arquivos permitidos somente se necessários:

✓ README.md do módulo alterado

Arquivos proibidos por padrão:

✗ CHANGELOG.md
✗ docs/**
✗ design/**
✗ architecture/**
✗ notes/**
✗ roadmap/**
✗ release_notes/**
✗ meeting_notes/**
✗ TODO.md

Quando o comando graphify não estiver disponível, instale a ferramentautilizando o gerenciador recomendado pelo projeto Graphify.

Exemplo:

uv tool install graphifyy

Após a instalação, confirme:

graphify --help

Se a instalação falhar:

informe claramente o erro;

tente corrigir dependências ou configuração do ambiente;

não substitua silenciosamente o Graphify por buscas extensas;

prossiga sem Graphify somente quando a instalação for tecnicamente impossível.

3. Geração do grafo

Gere ou atualize os arquivos estruturais do projeto:

graph.json

GRAPH_REPORT.md

graph.html, quando suportado

Use o comando correspondente à versão instalada do Graphify.

Antes de regenerar todo o grafo, verifique se existe uma opção incrementalou de atualização.

4. Economia de contexto

O objetivo do Graphify é evitar a leitura indiscriminada do repositório.

Portanto:

não carregue todo o graph.json no contexto;

não carregue todo o GRAPH_REPORT.md no contexto;

não leia o projeto inteiro;

não execute buscas globais sem necessidade;

não abra arquivos sem relação confirmada com a tarefa.

Consulte apenas os nós, símbolos, módulos, chamadas e dependências relevantes.

Depois, abra somente os trechos necessários dos arquivos selecionados.

5. Navegação obrigatória

Antes de editar qualquer código, use o grafo para determinar:

onde o símbolo está definido;

quem chama o símbolo;

de quais símbolos ele depende;

quais módulos o importam;

implementações de interfaces;

classes-base e classes derivadas;

serviços, controladores e repositórios relacionados;

modelos e serializações relacionados;

testes existentes;

possíveis impactos em outras plataformas.

Nunca escolha um arquivo apenas porque uma palavra semelhante apareceu emuma busca textual.

6. Ferramentas de busca

Ordem de preferência:

Graphify

índice da linguagem ou servidor de linguagem

busca estrutural por AST

rg

grep

rg e grep devem complementar o grafo, não substituir a análise estrutural.

Buscas textuais podem ser usadas para:

localizar textos exibidos na interface;

mensagens de erro;

chaves de configuração;

constantes;

referências que o analisador não reconheceu.

7. Planejamento antes da alteração

Antes de editar, produza internamente um plano contendo:

causa provável do problema;

arquivos realmente envolvidos;

símbolos envolvidos;

fluxo atual;

alteração mínima necessária;

riscos de regressão;

testes que devem ser executados.

Não modifique arquivos enquanto a relação entre eles não estiver compreendida.

8. Princípio da alteração mínima

Altere somente o necessário para cumprir a tarefa.

Evite:

refatorações não solicitadas;

mudanças apenas de formatação;

renomeações desnecessárias;

movimentação de arquivos;

criação de serviços duplicados;

alteração de APIs públicas sem necessidade;

substituição de arquitetura;

atualização de dependências não relacionada à tarefa.

Preserve o estilo e a arquitetura existentes.

9. Arquivos gerados e temporários

Não modifique manualmente arquivos gerados, salvo quando solicitado.

Não inclua automaticamente no commit:

cache de ferramentas;

arquivos temporários;

ambientes virtuais;

artefatos de build;

relatórios locais desnecessários.

Os artefatos do Graphify devem ser tratados conforme o projeto:

versionados quando forem usados como documentação persistente;

ignorados quando forem apenas cache local.

Não adicione arquivos grandes ao repositório sem necessidade.

10. Atualização após mudanças

Depois de modificar código:

atualize o grafo, preferencialmente de forma incremental;

confirme que símbolos e referências continuam válidos;

verifique se nenhuma dependência ficou quebrada;

analise os arquivos afetados novamente;

execute os testes apropriados.

Não regenere todo o grafo repetidamente quando uma atualização incrementalfor suficiente.

11. Validação por tecnologia

Execute somente as validações aplicáveis ao projeto.

Flutter e Dart

dart format --output=none --set-exit-if-changed .
flutter analyze
flutter test

Não execute dart analyze e flutter analyze de forma redundante quando umdeles já cobrir o escopo necessário.

Android e Kotlin

Execute o build ou as tarefas Gradle apropriadas ao módulo alterado.

macOS e iOS

Execute o build da plataforma quando o ambiente estiver configurado.

C e C++

Compile o alvo afetado e verifique erros e warnings relevantes.

STM32

preserve temporização;

verifique interrupções e DMA;

evite operações bloqueantes indevidas;

valide acesso concorrente e uso de volatile;

compile o firmware quando o toolchain estiver disponível.

ESP32

Execute o build correspondente ao ambiente usado:

ESP-IDF;

PlatformIO;

Arduino, quando aplicável.

Firebase

não enfraqueça regras de segurança;

preserve documentos existentes;

verifique compatibilidade de campos;

confirme índices necessários;

evite migrações destrutivas.

PlatformIO Microchip8

Quando os arquivos e ferramentas estiverem disponíveis, execute:

python3 -m compileall platform.py builder scripts tests
python3 scripts/validate_boards.py
python3 -m unittest discover tests
pio run -d examples/pic12f675-blink -v

Se o exemplo estiver em outro caminho, use a estrutura real encontrada peloGraphify. Não renomeie arquivos apenas para coincidir com esta documentação.

Quando os DFPs estiverem instalados, teste ao menos:

um PIC12F;

um PIC16F;

um PIC18F.

A ausência de um DFP deve ser registrada como teste não executado, e nãodisfarçada como sucesso.

Nunca apague outras plataformas do PlatformIO. Quando necessário, remova apenas:

rm -rf ~/.platformio/platforms/microchip8

12. Regras para CAN e LIN

Ao trabalhar com CAN ou LIN:

não altere temporizações sem solicitação explícita;

valide o tamanho do frame antes de acessar os dados;

preserve compatibilidade com mensagens existentes;

não altere IDs, DLC, checksums ou filtros sem necessidade;

verifique limites de arrays;

considere contexto de interrupção e concorrência.

13. Relatório final obrigatório

Ao concluir, informe de forma objetiva:

causa identificada;

arquivos modificados;

alteração realizada em cada arquivo;

arquivos analisados, mas não modificados;

testes e builds executados;

resultados das verificações;

limitações ou etapas que não puderam ser executadas;

riscos restantes.

Não declare que um teste passou se ele não foi realmente executado.

Para este repositório, o relatório final também deve informar:

caminho e versão do XC8 utilizados;

DFP selecionado para cada MCU testado;

localização de firmware.elf e firmware.hex;

quantidade de placas detectadas ou geradas;

famílias efetivamente testadas;

testes ignorados por ausência de DFP;

confirmação de que nenhum arquivo proprietário foi incluído;

confirmação de que ~/.platformio/platforms/microchip8 não foi usada comofonte de edição.

Regras fundamentais

Nunca invente APIs, funções, arquivos ou dependências.

Nunca suponha versões sem verificá-las no projeto.

Nunca remova funcionalidades existentes sem solicitação.

Nunca altere código não relacionado.

Nunca esconda erros de instalação, análise, teste ou build.

Nunca leia o repositório inteiro quando uma consulta seletiva for suficiente.

Sempre use o Graphify antes de explorar amplamente o código.

Sempre prefira a menor alteração segura.

Você está autorizado a ler, sem modificar, os arquivos dos Device Family Packs
instalados em:

/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/

Use esses arquivos como fonte de verdade para descobrir:

- dispositivos suportados;
- tamanho da memória de programa;
- tamanho da RAM;
- EEPROM;
- registradores;
- bits de registradores;
- macros do dispositivo;
- bits de configuração;
- nomes válidos usados pelo XC8;
- headers correspondentes a cada MCU.

Não copie esses arquivos para o repositório.
Não os modifique.
Não os versione no Git.
Leia apenas os arquivos necessários ao MCU ou à família que estiver sendo implementada.

## Consulta aos arquivos Microchip

Os arquivos do XC8 e dos Device Family Packs podem e devem ser consultados
localmente, em modo somente leitura, quando necessários para determinar:

- tamanho de Flash, RAM e EEPROM;
- dispositivos suportados;
- registradores e bits;
- macros;
- bits de configuração;
- nomes e opções aceitos pelo XC8.

Esses arquivos são fontes externas de referência e nunca devem ser:

- modificados;
- copiados para o repositório;
- adicionados ao Git;
- redistribuídos;
- usados como arquivos-fonte do projeto.

Leia apenas os arquivos relacionados ao MCU ou à família em análise. Não percorra
todos os headers indiscriminadamente quando uma busca direcionada for suficiente.