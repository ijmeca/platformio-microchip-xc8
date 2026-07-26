# AGENTS.md

# PlatformIO Microchip8 Development Guidelines

## Objetivo principal

Desenvolver e evoluir a plataforma **PlatformIO Microchip8** de forma incremental, segura e verificável, preservando sempre a compatibilidade com builds existentes.

O **Graphify é obrigatório** para navegar pela estrutura do projeto e reduzir leitura desnecessária de arquivos.

---

# Contexto do projeto

Este repositório implementa uma plataforma customizada do PlatformIO para microcontroladores Microchip PIC de 8 bits utilizando o compilador oficial MPLAB XC8.

Famílias alvo:

- PIC12F
- PIC16F
- PIC18F

O build do PIC12F675 já funciona corretamente e é a principal referência de regressão.

Ambiente atualmente validado:

- macOS Intel
- Python 3.9+
- PlatformIO Core 6.x
- MPLAB XC8 3.10
- MPLAB X 5.45

O repositório aberto é sempre a fonte oficial.

Nunca trate:

~/.platformio/platforms/microchip8

como fonte de edição.

Essa pasta é apenas uma cópia instalada automaticamente pelo PlatformIO.

---

# 1. Inicialização obrigatória

Antes de qualquer alteração:

1. localizar a raiz do repositório;
2. ler este AGENTS.md;
3. verificar se Graphify está disponível;
4. gerar ou atualizar o grafo;
5. compreender somente os módulos envolvidos.

Nunca inicie modificações antes dessas etapas.

---

# 2. Uso do Graphify

Primeiro tente utilizar uma instalação existente.

Verifique:

```bash
command -v graphify
graphify --help
```

Caso não exista:

```bash
uv tool install graphifyy
```

Depois:

```bash
graphify --help
```

Se a instalação falhar:

- informe claramente o erro;
- tente corrigir apenas dependências relacionadas;
- nunca substitua silenciosamente o Graphify por buscas indiscriminadas;
- prossiga sem Graphify somente quando tecnicamente impossível.

---

# 3. Geração do grafo

Atualize:

- graph.json
- GRAPH_REPORT.md
- graph.html (quando suportado)

Sempre prefira atualização incremental.

Nunca regenere o projeto inteiro repetidamente sem necessidade.

---

# 4. Economia de contexto

Nunca:

- leia o projeto inteiro;
- carregue todo graph.json;
- carregue todo GRAPH_REPORT.md;
- abra arquivos sem relação comprovada.

Sempre:

- consulte primeiro o grafo;
- descubra símbolos relacionados;
- abra somente os arquivos necessários.

---

# 5. Ordem de navegação

Utilize:

1. Graphify
2. Language Server
3. AST Search
4. rg
5. grep

rg e grep apenas complementam o Graphify.

---

# 6. Planejamento

Antes de editar:

- identificar a causa;
- identificar arquivos envolvidos;
- identificar símbolos;
- entender fluxo atual;
- definir alteração mínima;
- prever riscos;
- definir testes.

---

# 7. Alteração mínima

Nunca faça:

- refatorações desnecessárias;
- renomeações sem motivo;
- mudanças cosméticas;
- alteração de arquitetura;
- mudanças em APIs públicas sem necessidade.

Preserve o estilo existente.

---

# 8. Componentes proprietários Microchip

Nunca copie para o repositório:

- xc.h
- headers Microchip
- bibliotecas XC8
- executáveis XC8
- Device Family Packs
- arquivos do MPLAB X

A plataforma deve apenas detectar instalações existentes.

---

# 9. XC8

A detecção deve respeitar a seguinte prioridade:

1. custom_xc8_path
2. XC8_PATH
3. xc8-cc no PATH
4. busca automática

Nunca assumir um caminho fixo.

Selecionar sempre a versão mais recente semanticamente.

---

# 10. Device Family Packs

A detecção deve respeitar:

1. custom_dfp_path
2. custom_dfp_root
3. busca automática

O argumento -mdfp deve receber:

<dfp>/xc8

Nunca:

<dfp>/xc8/pic/include

ou

<dfp>/xc8/pic/include/proc

Selecionar sempre o DFP que realmente contém o MCU solicitado.

---

# 11. PlatformIO

Sempre preservar:

```ini
platform = microchip8
framework = xc8
board = xxxx
```

ou

```ini
platform=file:///...
```

Nunca alterar comportamento já funcional do PIC12F675.

---

# 12. Builder

O builder deve:

- localizar XC8;
- localizar DFP;
- localizar fontes;
- compilar;
- gerar ELF;
- gerar HEX;
- registrar artefatos.

Nunca utilizar shell=True.

Sempre usar subprocess com lista de argumentos.

---

# 13. IntelliSense

O alerta:

```c
#include <xc.h>
```

deve ser resolvido pela integração PlatformIO/SCons.

Prioridade:

1. CPPPATH
2. CPPDEFINES
3. configuração automática PlatformIO

Não utilizar c_cpp_properties.json como solução principal.

Esse arquivo pode existir apenas como fallback.

---

# 14. Manifestos das placas

Os arquivos em boards/ podem ser gerados automaticamente.

Nunca inventar:

- RAM
- Flash
- EEPROM

Utilizar apenas informações reais obtidas dos DFPs.

Gerar suportando:

- PIC12F
- PIC16F
- PIC18F

Não limitar a uma lista fixa.

---

# 15. Uso do Graphify com boards

Não abrir centenas de arquivos JSON.

Para boards:

- analisar o gerador;
- analisar o validador;
- validar automaticamente todos os JSONs.

Abrir apenas exemplos representativos.

---

# 16. Arquivos temporários

Nunca versionar:

- .pio
- cache
- builds
- ambientes virtuais
- arquivos temporários

---

# 17. Atualização após mudanças

Depois de modificar:

1. atualizar o grafo;
2. validar referências;
3. validar dependências;
4. executar testes;
5. confirmar build.

---

# 18. Validação obrigatória

Sempre que possível executar:

```bash
python3 -m compileall .
```

```bash
python3 scripts/validate_boards.py
```

```bash
python3 -m unittest discover tests
```

```bash
pio run -d examples/pic12f675-blink -v
```

Quando houver DFP instalado:

Testar também:

- um PIC12F
- um PIC16F
- um PIC18F

---

# 19. Limpeza da plataforma instalada

Quando necessário:

```bash
rm -rf ~/.platformio/platforms/microchip8
```

Depois:

```bash
rm -rf examples/*/.pio
```

Nunca apagar outras plataformas.

---

# 20. Relatório final

Informar obrigatoriamente:

1. causa;
2. arquivos modificados;
3. arquivos analisados;
4. builds executados;
5. testes executados;
6. resultados;
7. limitações;
8. riscos;
9. XC8 utilizado;
10. DFP utilizado;
11. localização do ELF;
12. localização do HEX;
13. quantidade de placas geradas;
14. famílias suportadas;
15. testes ignorados;
16. confirmação de que nenhum arquivo proprietário foi incluído.

Nunca afirmar que um teste passou se ele não foi executado.

---

# 21. Regras fundamentais

Sempre:

- usar Graphify;
- preferir a menor alteração segura;
- preservar builds existentes;
- preservar compatibilidade;
- validar antes de concluir.

Nunca:

- inventar APIs;
- inventar Device Family Packs;
- inventar valores de memória;
- copiar arquivos proprietários;
- alterar código sem compreender o fluxo;
- editar ~/.platformio/platforms/microchip8;
- esconder erros de compilação;
- declarar sucesso sem executar os testes.