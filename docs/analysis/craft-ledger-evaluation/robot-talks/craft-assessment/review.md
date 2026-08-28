# Review — Craft Ledger

## Escopo e conclusão

Esta primeira avaliação confronta o contrato público do Craft com seus schemas,
ledgers atuais e uma testemunha histórica de operação. O resultado é **FIX**:
o modelo conceitual é útil e a separação entre ledger-fonte e projeções derivadas
deve ser preservada, mas contratos que o Craft declara hoje não são aplicados por
um validator, reindexador ou atualizador determinístico empacotado. Além disso,
há divergências entre os métodos descritos, o schema canônico e o ledger vivo de
`spells/goal`.

O problema não é a ausência de `.craft/index.json`: esse arquivo é explicitamente
opcional e derivado. O problema é não haver, ainda, uma forma executável e
repetível de verificar o ledger-fonte e reconstruir com segurança seus índices.

## Tabela de cobertura

| Artefato | Superfície avaliada | Cobertura |
|---|---|---|
| `arcana/craft/SKILL.md` | Métodos, invariantes, validação e indexação | Completa para os achados abaixo |
| `arcana/craft/ARCHITECTURE.md` | Autoridade, limites atuais e superfícies ausentes | Completa para os achados abaixo |
| `arcana/craft/README.md` | Modelo de armazenamento e papel de `index.json` | Completa para os achados abaixo |
| `arcana/craft/templates/ledger.schema.yml` | Entrada de compatibilidade e contrato agregado | Completa para os achados abaixo |
| `arcana/craft/templates/schemas/ledger-core.schema.yml` | Linhas, campos, enums, identidade e regras | Completa para os achados abaixo |
| `arcana/craft/templates/schemas/index.schema.yml` | Índices embutidos e índice gerado | Completa para os achados abaixo |
| `.craft/ledger.yml` | Ledger raiz atual | Amostra atual; nenhum incidente de colisão observado |
| `spells/goal/.craft/ledger.yml` | Ledger compatível `0.2.0` e deriva corrente | Completa para as divergências identificadas |
| `development/craft/CRAFT-HANDOFF-AUTO-ARTIFACT-LIFECYCLE-2026-06-13.md` | Testemunha histórica de operação manual | Evidência histórica, não integralmente reproduzível |

## Achados

| # | Local do artefato | Evidência | Severidade | Consequência | Correção proposta |
|---|---|---|---|---|---|
| 1 | `arcana/craft/SKILL.md:215-227`; `arcana/craft/templates/schemas/ledger-core.schema.yml:670-724` | `open_decision` cria uma decisão ativa sem receber `selected` e `rationale`, mas ambos são obrigatórios no schema. Não há sentinel nem regra para representar “ainda não decidido”. | MAJOR | A operação documentada não possui uma tradução canônica inequívoca para uma linha válida. O modelo precisa inventar valores ou quebrar o schema. | Tornar os campos condicionais ao estado, ou definir explicitamente valores e invariantes de decisão aberta; adicionar fixtures de abertura e fechamento. |
| 2 | `arcana/craft/SKILL.md:229-238`; `arcana/craft/templates/schemas/ledger-core.schema.yml:421-497` | `add_gap` fala em `context_id` e `owner_route`; o schema exige `scope_id`, `owner` e `status`. `add_definition` fala em `context_id` e `meaning`; o schema exige `scope_id` e `statement`. | MAJOR | A escrita depende de tradução implícita pelo modelo e pode variar entre execuções ou produzir linhas incompletas. | Unificar o vocabulário dos métodos e do schema, documentar defaults e validar fixtures de cada método. |
| 3 | `arcana/craft/templates/ledger.schema.yml:10-12`; `spells/goal/.craft/ledger.yml:1-4,54,159-170,336-350`; `arcana/craft/templates/schemas/ledger-core.schema.yml:37-47,80-89,455-492` | O entrypoint declara `0.2.0` compatível sem perfil executável de compatibilidade. O ledger Goal usa estágio `registered`, blocker `closed` e gaps sem `status`, formas incompatíveis com o schema `0.3.0` referenciado. | MAJOR | Não é possível distinguir deterministicamente um ledger legado válido de um ledger atual inválido, nem migrá-lo com segurança. | Definir perfis versionados para `0.2.0` e `0.3.0`, com defaults/migração explícitos e fixtures; então corrigir ou migrar o ledger Goal. |
| 4 | `spells/goal/.craft/ledger.yml:9-35,125-156,159-170,336-365`; `arcana/craft/templates/schemas/index.schema.yml:26-42,82-86,111-118,157-175` | `active_blockers` inclui `BLK-GOAL-SUBMODULE-001`, cuja linha está `closed`; `active_gaps` inclui apenas uma de duas gaps que não têm `status`. O `by_id` omite a description, definitions e relations, mas o contrato atual não deixa claro se o índice embutido deve ser completo — a regra “every known row” pertence ao índice gerado. | MAJOR | Há deriva corrente entre linhas-fonte e índices derivados; parte do estado não pode ser reconstruída pela regra declarada. | Especificar a completude de `by_id`; criar `reindex(ledger)` determinístico; validar filtros dos índices e corrigir o ledger Goal. |
| 5 | `arcana/craft/templates/schemas/ledger-core.schema.yml:18-26,773-785`; `arcana/craft/templates/ledger.schema.yml:49-63` | IDs estáveis são exigidos, mas a única regra explícita de unicidade cobre `context_id`. Os demais IDs têm padrões, sem política geral de unicidade, alocação ou colisão. Nenhuma colisão atual foi observada. | MAJOR | Referências e `by_id` podem se tornar ambíguos; hoje a prevenção depende da disciplina de quem escreve. | Definir domínio de unicidade global ou por família, um alocador/convenção verificável e falha fechada para colisões. |
| 6 | `arcana/craft/ARCHITECTURE.md:18-21,248-260`; `arcana/craft/templates/schemas/index.schema.yml:177-186`; `development/craft/CRAFT-HANDOFF-AUTO-ARTIFACT-LIFECYCLE-2026-06-13.md:11-27,38-47` | A ausência de runner, validator, aplicador e index builder é um limite deliberado. A testemunha histórica registra 12 ledgers corrigidos manualmente, índices à deriva e corrupções de YAML. | MAJOR | Regras conceitualmente determinísticas continuam sendo executadas probabilisticamente pelo modelo, com custo e risco já observados. | Entregar primeiro validator somente leitura e reindexador; depois um aplicador com dry-run, idempotência, escrita atômica e proteção contra fonte obsoleta. |
| 7 | `arcana/craft/templates/schemas/ledger-core.schema.yml:194-223,831-836`; `arcana/craft/ARCHITECTURE.md:248-260` | Estados e transições proibidas são declarados, mas não há histórico de eventos, controle de concorrência, validator ou aplicador empacotado que prove a transição realizada. | MAJOR | O estado final pode ser inspecionado parcialmente, mas o Craft não consegue garantir que uma transição inválida não ocorreu. Não foi observada uma transição inválida específica no corpus. | Validar estados finais agora; antes de alegar enforcement de lifecycle, adicionar histórico/receipts e controle de fonte obsoleta ou compare-and-swap. |
| 8 | `arcana/craft/SKILL.md:74-88`; `arcana/craft/templates/schemas/ledger-core.schema.yml:18-26,735-768`; `arcana/craft/ARCHITECTURE.md:152-164` | O texto geral fala em ID estável para cada linha, enquanto recomposição usa deliberadamente a identidade composta `child_id + parent_id`. | MINOR | Leitores e ferramentas podem esperar um campo ID e uma âncora que não existem, apesar de a identidade estar definida. | Trocar a redação geral para “identidade estável” e definir seletor/âncora para a chave composta. |
| 9 | `development/craft/CRAFT-HANDOFF-AUTO-ARTIFACT-LIFECYCLE-2026-06-13.md:65-70` | A testemunha histórica omite os caminhos exatos do workspace privado. | MINOR | O incidente sustenta o risco operacional, mas não pode ser integralmente reproduzido apenas com este repositório. | Converter os casos descritos em fixtures públicas mínimas e sanitizadas. |

## Vereditos por artefato

| Artefato | Veredito | Motivo |
|---|---|---|
| `arcana/craft/SKILL.md` | FIX | Métodos e schemas divergem; a redação de identidade precisa de ajuste. |
| `arcana/craft/ARCHITECTURE.md` | KEEP | Expõe honestamente os limites; deve ser atualizado quando houver enforcement. |
| `arcana/craft/README.md` | KEEP | Descreve corretamente `index.json` como opcional e derivado. |
| `arcana/craft/templates/ledger.schema.yml` | FIX | Compatibilidade `0.2.0` carece de semântica verificável. |
| `arcana/craft/templates/schemas/ledger-core.schema.yml` | FIX | Lifecycle de decisão, unicidade geral e compatibilidade precisam ser formalizados. |
| `arcana/craft/templates/schemas/index.schema.yml` | FIX | Falta decidir a completude do índice embutido e fornecer enforcement. |
| `.craft/ledger.yml` | KEEP | Não apresentou os incidentes concretos identificados no ledger Goal. |
| `spells/goal/.craft/ledger.yml` | FIX | Possui divergências de schema e deriva de índices correntes. |
| Handoff histórico de 2026-06-13 | KEEP | É evidência útil, com limite de reprodutibilidade explicitado. |

## Solicitações de mudança

1. Implementar um validator somente leitura e sensível à versão, cobrindo campos
   obrigatórios, enums, referências, unicidade e coerência dos índices.
2. Definir a semântica de compatibilidade `0.2.0`/`0.3.0` e migrar ou corrigir o
   ledger Goal conforme essa decisão.
3. Especificar a completude dos índices embutidos e implementar um reindexador
   determinístico a partir das linhas-fonte.
4. Alinhar `open_decision`, `add_gap` e `add_definition` aos schemas e criar
   fixtures de operação.
5. Formalizar geração e unicidade de IDs, com rejeição determinística de colisões.
6. Adicionar histórico e controle de transições antes de alegar enforcement de
   lifecycle.
7. Somente depois introduzir um aplicador mutável de receipts/patches, com
   dry-run, idempotência, escrita atômica e proteção contra fonte obsoleta.

## Limite da evidência

Esta é uma revisão estática e adversarial do corpus listado, não uma execução de
um validator Craft — esse validator ainda não existe no pacote. “Deriva corrente”
é usado apenas onde as linhas e índices do ledger Goal se contradizem diretamente.
“Risco ativo” é usado onde o contrato não especifica ou não aplica uma garantia,
sem alegar um incidente que não foi observado. A testemunha histórica comprova
custo operacional relatado, mas seus fixtures privados não estão disponíveis para
reprodução integral.
