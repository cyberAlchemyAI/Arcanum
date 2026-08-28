# Craft Ledger Analysis

## Objetivo

O objetivo deste documento é explicar o que o Craft representa hoje, qual papel
o ledger exerce dentro dele, por que parte de sua operação ainda depende de
julgamento interpretativo e qual é o menor próximo passo capaz de tornar suas
garantias verificáveis.

Esta não é uma proposta de substituir o Craft nem de transformar todo julgamento
em automação. A questão é mais específica: separar as escolhas que precisam de
interpretação das verificações que deveriam produzir sempre o mesmo resultado
diante do mesmo ledger.

## Contexto

Agentes conseguem produzir mudanças com velocidade, mas cada mudança altera o
estado a partir do qual o próximo trabalho será decidido. Um blocker pode ser
resolvido, uma decisão pode fechar uma alternativa, um artefato pode passar a
servir como evidência e uma unidade menor pode ser recomposta em seu contexto
pai. Se essas mudanças existirem apenas na conversa que as produziu, o projeto
perde memória quando a sessão termina.

O Craft existe para preservar essa memória como estado local do projeto. Sua
visão inicial era mais ampla: um método recursivo para transformar intenção em
artefato, observar o resíduo deixado pela tradução e decidir se o trabalho deve
ser reparado, dividido, encaminhado ou recomposto. O pacote atual formaliza essa
parte da visão como método, contrato de armazenamento e estado persistido: um
ledger recursivo que mantém contextos, decisões, blockers, gaps, evidências,
próximos movimentos e recomposição. Ele ainda não materializa esse método como
runner ou mecanismo geral de atualização.

Essa diferença importa. O Craft não é apenas o arquivo YAML, mas o ledger é a
superfície sobre a qual o Craft atual consegue preservar estado. Quando a
operação dessa superfície não é confiável, o método pode continuar conceitualmente
útil, mas sua memória deixa de ser uma base segura para a próxima ação.

## O que o Craft atual mantém

As coleções de linhas em `.craft/ledger.yml` são a autoridade sobre o estado
pertencente ao escopo Craft selecionado. O arquivo também contém a seção
`indexes`, mas ela é uma projeção reconstruível das linhas-fonte, mesmo estando
fisicamente no mesmo YAML. Ela não constitui uma segunda autoridade.

O ledger não se torna dono do código, dos relatórios ou dos receipts produzidos
por outras capacidades. Em vez disso, mantém linhas que identificam esses
objetos, relacionam evidências ao estado do projeto e deixam explícito o que
permanece aberto.

`CRAFT.md` e `.craft/index.json` têm outra função. São formas derivadas de
consultar o mesmo estado: a primeira para leitura humana e a segunda, quando
existe, para lookup por máquina. Nenhuma delas deve adquirir autoridade própria.
Se divergem do ledger, devem ser reconstruídas a partir dele.

Uma implementação capaz de aplicar essa separação com segurança deveria seguir
este fluxo-alvo:

```text
operação proposta sobre uma revisão conhecida da fonte
  -> construção de um estado candidato
  -> validação do candidato
  -> commit atômico das linhas-fonte
  -> derivação e publicação dos índices
  -> nova visão consultável do estado
```

Esse fluxo não existe hoje como runner empacotado; seus passos dependem de edição
disciplinada, frequentemente mediada pelo modelo. Ainda assim, a ordem importa.
Reconstruir índices não corrige uma linha inválida, e uma visão humana bem
formatada não prova que suas referências resolvem. Da mesma forma, o fato de um
receipt existir não autoriza por si só a mudança do ledger; um caller ainda
precisa selecionar o escopo e invocar a operação Craft apropriada.

## Onde há julgamento interpretativo e onde deveria haver enforcement mecânico

O Craft precisa de julgamento interpretativo onde o significado do trabalho
ainda está em aberto. Esse julgamento pode vir do modelo, de um humano ou de
ambos sob uma política e uma autoridade locais. Ele precisa de mecanismos
determinísticos quando a política e o significado relevantes já foram aceitos e
resta preservar integridade.

| Situação | Responsabilidade apropriada | Estado atual |
|---|---|---|
| Interpretar se uma descoberta é informação, gap ou blocker | Modelo e/ou humano sob governança local | Depende legitimamente de contexto e julgamento. |
| Escolher severidade e tratamento de um gap, ou tipo e lane de um blocker | Modelo e/ou humano sob regras locais | Depende legitimamente de impacto, resposta e responsabilidade. |
| Propor um ID semanticamente útil | Caller interpretativo sob convenção local | Não há alocador geral definido. |
| Definir o namespace e o domínio de unicidade dos IDs | Autoridade responsável pelo contrato | A política geral permanece aberta. |
| Validar o padrão aceito e rejeitar colisões conforme uma política já definida | Validator determinístico | Há padrões e uma regra explícita para contextos, mas não enforcement empacotado geral. |
| Conferir campos, enums e referências de uma versão conhecida | Validator determinístico | As regras são declaradas; o runner não existe. |
| Reconstruir índices sob filtros e completude já definidos | Reindexador determinístico | O contrato é parcial e o builder não existe. |
| Impedir atualização sobre uma revisão obsoleta da fonte | Aplicador determinístico | O mecanismo de revisão ou compare-and-swap ainda não foi escolhido. |
| Reaplicar o mesmo receipt sem duplicar efeitos | Aplicador idempotente | É requisito futuro, não garantia atual. |

O sistema atual descreve grande parte dessas regras em skills, arquitetura e
schemas. Isso já é mais forte do que não possuir contrato algum: torna possível
inspecionar a forma esperada e discutir violações concretas. Mas uma regra
declarada não se aplica sozinha. Sem um programa que leia o ledger, interprete a
versão correta e falhe quando a regra é quebrada, quem edita o ledger continua
responsável tanto pela decisão semântica quanto pela mecânica que deveria apenas
preservar essa decisão.

## O principal problema atual

O problema central não é que parte do Craft seja probabilística. Interpretar
trabalho é justamente uma das razões para usar um modelo. O problema é permitir
que essa incerteza atravesse a fronteira e passe a controlar também a aplicação
de políticas já decididas sobre identidade, referências, índices e transições.

Isso ocorre hoje de três maneiras relacionadas.

Primeiro, algumas operações descritas pelo
[contrato do Craft](../../../arcana/craft/SKILL.md) não se traduzem de forma
inequívoca para o
[schema das linhas](../../../arcana/craft/templates/schemas/ledger-core.schema.yml).
`open_decision`, por exemplo, abre uma decisão sem receber `selected` e
`rationale`, embora o schema atual exija ambos. `add_gap` e `add_definition`
também usam nomes diferentes dos campos canônicos e não declaram todas as
informações obrigatórias. O modelo precisa inventar uma tradução que o contrato
deveria possuir.

Segundo, compatibilidade e identidade são declaradas sem garantia executável
suficiente. O [schema de entrada](../../../arcana/craft/templates/ledger.schema.yml)
afirma compatibilidade com ledgers `0.2.0`, mas não define um perfil capaz de
dizer quais defaults ou enums pertencem a essa versão. O
[ledger de `spells/goal`](../../../spells/goal/.craft/ledger.yml) torna a
ambiguidade concreta: ele declara `0.2.0`, usa formas ausentes no schema `0.3.0`
e contém gaps sem o `status` atualmente obrigatório. Isso demonstra divergência
em relação a `0.3.0`, mas a ausência de um perfil `0.2.0` impede determinar se o
ledger legado é válido em sua própria versão. IDs estáveis também são esperados,
mas a regra explícita de unicidade cobre apenas contextos; não há um alocador ou
uma política geral de colisão para todas as famílias.

Terceiro, as projeções podem se afastar silenciosamente das linhas-fonte. Se o
ledger de `spells/goal` for interpretado pelos filtros `0.3.0`,
`active_blockers` aponta para um blocker marcado como `closed`, enquanto
`active_gaps` tenta distinguir gaps que não possuem `status`. Sem um perfil
`0.2.0`, porém, o sistema não consegue determinar deterministicamente qual seria
a projeção correta. O `by_id` embutido omite algumas famílias, mas o contrato não
estabelece com clareza se esse índice compacto deve ser completo. Sem um
reindexador governado por regras versionadas, cada edição exige que o modelo
preserve manualmente representações duplicadas do mesmo estado.

Esses não são apenas riscos abstratos. Um
[handoff histórico](../../../development/craft/CRAFT-HANDOFF-AUTO-ARTIFACT-LIFECYCLE-2026-06-13.md)
registra uma operação sobre doze ledgers em que artefatos, índices e `next_move`
precisaram de correção manual, incluindo corrupção de YAML. A evidência é
limitada porque os fixtures privados não estão disponíveis neste repositório,
mas ela é suficiente para mostrar que a ausência de tooling não é
operacionalmente neutra.

## Por que `index.json` não é a correção

`.craft/index.json` é opcional por contrato. Sua ausência não significa que o
ledger esteja incompleto, porque ele é apenas uma superfície reconstruível de
lookup. Criá-lo manualmente acrescentaria outra cópia que também poderia ficar
obsoleta.

O que falta é uma transformação confiável, depois que a versão e as regras de
projeção aplicáveis estiverem definidas:

```text
ledger válido na versão conhecida
  -> função de reindexação
  -> índices embutidos coerentes
  -> index.json opcional com hash da fonte
```

O valor do índice gerado aparece somente quando sua proveniência e atualização
são verificáveis. Portanto, a ordem responsável não começa pela presença do
arquivo; começa pela validade da fonte e pela decisão das regras que tornarão a
derivação determinística.

## O próximo passo responsável

O primeiro incremento sustentado pelo contrato atual deveria ser um parser com
validator parcial, somente leitura e fail-closed. Ele não decidiria se algo é um
blocker nem escolheria o tratamento de um gap. Também não inventaria semântica
para `0.2.0` ou uma política geral de unicidade. Seu limite inicial seria:

- reconhecer `0.3.0` e validar somente suas invariantes inequívocas;
- responder `unsupported` ou `unknown` para versões e políticas sem perfil;
- conferir campos, enums e referências cobertos pelo contrato reconhecido;
- aplicar as regras de unicidade já explícitas e reportar, sem resolver, os
  demais possíveis conflitos de identidade;
- detectar incoerências de índices apenas quando os filtros da versão forem
  conhecidos;
- produzir diagnósticos estáveis sem alterar nenhum byte do ledger.

Esse validator torna violações observáveis; ele ainda não as impede. Uma falha
encerra a tentativa e devolve um diagnóstico ao caller, que pode corrigir a
proposta ou encaminhar a política ausente à autoridade responsável antes de
revalidar.

O reindexador canônico vem depois de decidir, por versão, quais famílias os
índices embutidos cobrem e quais filtros definem itens ativos. Sua aceitação deve
provar que as linhas-fonte permanecem idênticas, que a mesma entrada produz os
mesmos índices e que uma segunda execução é um no-op. Um ledger legado deve ser
aceito por um perfil conhecido ou recusado com diagnóstico estável; nunca
normalizado por adivinhação.

Somente após essas superfícies estarem cobertas por fixtures faz sentido
introduzir um aplicador mutável de patches ou receipts. Esse aplicador deverá
comparar uma revisão ou hash da instância-fonte — diferente de `schema_version`
—, validar o candidato antes do commit, aplicar a mudança atomicamente, ser
idempotente e falhar fechado diante de colisão, referência quebrada ou transição
inválida. O mecanismo exato de revisão ou compare-and-swap ainda precisa ser
decidido.

Essa ordem é uma recomendação desta análise para reduzir risco, não uma
capacidade que a arquitetura atual já forneça. Ela preserva a divisão necessária:
modelo e humano continuam propondo significado sob governança; o runtime passa,
em etapas, a verificar e depois aplicar a representação aceita desse significado.

## Limite da análise

Esta análise se apoia no [contrato atual do Craft](../../../arcana/craft/SKILL.md),
nos [schemas `0.3.0`](../../../arcana/craft/templates/ledger.schema.yml), nos
ledgers raiz e de [`spells/goal`](../../../spells/goal/.craft/ledger.yml), no
[handoff histórico](../../../development/craft/CRAFT-HANDOFF-AUTO-ARTIFACT-LIFECYCLE-2026-06-13.md)
e na [avaliação adversarial](robot-talks/craft-assessment/review.md). Ela
distingue contrato declarado, estado observado e mecanismo implementado; não
presume que um schema seja um validator executável nem que um incidente
histórico represente todos os ledgers.

Também não decide ainda:

- se a unicidade deve ser global ou apenas interna a cada família;
- qual é a semântica definitiva de compatibilidade com `0.2.0`;
- se a prova de lifecycle exigirá histórico completo de eventos ou apenas
  receipts de transição;
- qual autoridade fechará as políticas de compatibilidade, unicidade e
  completude dos índices;
- qual componente deverá possuir o futuro aplicador mutável.

Essas decisões bloqueiam um validator completo e um reindexador canônico, mas não
bloqueiam o primeiro slice fail-closed. Já existe evidência suficiente para
construir um parser e um validator parcial, somente leitura, que reconheça as
invariantes inequívocas de `0.3.0` e recuse explicitamente o que ainda não possui
semântica aceita. O passo seguinte não é automatizar a incerteza: é transformar
cada política aberta em uma decisão verificável antes de conceder ao runtime
autoridade de escrita.
