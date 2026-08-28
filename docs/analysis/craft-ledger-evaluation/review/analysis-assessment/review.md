# Review — Craft Ledger Analysis

## Coverage

| Superfície | O que foi verificado | Resultado |
|---|---|---|
| `docs/analysis/craft-ledger-evaluation/analysis.md` | Objetivo, progressão explicativa, modelo operacional e recomendação | Cobertura completa |
| Resolução medium | Capacidade de prever, distinguir, decidir e avaliar o próximo incremento | Boa orientação; operação e critérios de fechamento ainda incompletos |
| Fronteira epistemológica | Separação entre contrato declarado, estado observado, mecanismo existente e recomendação | Parcial; há sobreposições materiais |
| Relações sistêmicas | Autoridade, fluxo de mutação, projeções, feedback e fechamento | Parcial; fluxo-alvo e feedback precisam de correção |
| Separações categóricas | Craft versus ledger; fonte versus projeção; julgamento versus enforcement; famílias de linhas | Parcial; há fusões que podem ensinar ações incorretas |
| Fidelidade ao corpus | `arcana/craft`, schemas, ledger Goal, handoff histórico e review anterior | O núcleo sobrevive; alguns claims precisam ser estreitados |
| Tom de `docs/analysis/arcanum-migration/analysis.md` | Contexto, exemplo, explicação progressiva, limites e próximos passos | Compatível |

## Findings

| # | Local do artefato | Evidência | Severidade | Consequência | Correção proposta |
|---|---|---|---|---|---|
| 1 | `analysis.md:5-7,174-194` | O objetivo promete “tornar suas garantias confiáveis”, mas o primeiro incremento proposto é somente leitura. Um validator torna violações observáveis; ele não impede futuras escritas inválidas. | MINOR | A promessa inicial é mais ampla do que a capacidade imediata proposta. | Trocar a promessa por “tornar suas garantias verificáveis” e explicar que o enforcement só começa com um aplicador fail-closed. |
| 2 | `analysis.md:23-28,72-80`; `arcana/craft/ARCHITECTURE.md:18-21,248-260` | “O pacote atual materializa uma parte operacional” e “essa separação produz uma regra estrutural” apresentam como operação existente um pacote que declara não possuir runner, row updater, validator ou index builder. | MAJOR | Contrato declarado, comportamento atual e arquitetura-alvo ficam epistemologicamente confundidos; o leitor pode prever capacidades que o Craft não possui. | Dizer que o pacote atual **formaliza** a visão como método, contrato e estado persistido. Rotular o pipeline como fluxo-alvo e explicitar que hoje seus passos dependem de execução manual ou mediada por modelo. |
| 3 | `analysis.md:72-80,191-194` | O fluxo altera as linhas-fonte antes de validar as invariantes, enquanto o aplicador futuro deve falhar fechado e publicar atomicamente. | MAJOR | Uma implementação literal poderia tornar estado inválido visível antes de descobrir a falha. | Substituir por: operação proposta → construir estado candidato → validar candidato → commit atômico das linhas-fonte → derivar e publicar índices. |
| 4 | `analysis.md:37-55,94-103`; `arcana/craft/templates/schemas/ledger-core.schema.yml:372-497,498-669` | O exemplo pergunta simultaneamente por severidade, tratamento e lane. No contrato atual, `severity` e `treatment` pertencem a gaps; `primary_lane`, `base_type` e `closure_condition` pertencem a blockers ou typed items. | MAJOR | A explicação pode ensinar o leitor ou o modelo a produzir uma linha híbrida que não corresponde a nenhuma família do ledger. | Transformar o exemplo em bifurcação: primeiro decidir se a descoberta é informação, gap ou blocker; para gap escolher severidade, tratamento e owner; para blocker escolher tipo, lane e condição de fechamento. |
| 5 | `analysis.md:61-70`; `arcana/craft/templates/schemas/index.schema.yml:26-42,45-76` | O documento diz que `.craft/ledger.yml` é a autoridade e o contrasta com `CRAFT.md` e `.craft/index.json`, mas não esclarece que o próprio ledger contém a seção derivada `indexes`. | MINOR | Um leitor pode não perceber que fonte e projeção compartilham o mesmo arquivo físico. | Explicitar que as coleções de linhas são a fonte autoritativa e que `indexes`, mesmo dentro do ledger, são projeções reconstruíveis. |
| 6 | `analysis.md:90-103,196-198,209-215` | “O Craft precisa do modelo” reduz o lado interpretativo ao modelo, embora humano, owner, política e decisão também possam possuir autoridade. A tabela ainda funde alocar ou formar um ID com validar padrão e rejeitar colisão, enquanto o domínio de unicidade permanece aberto. | MAJOR | A separação atribui autoridade ao ator errado e apresenta como mecanismo determinado uma política de identidade ainda inexistente. | Renomear a fronteira para “julgamento interpretativo versus enforcement mecânico”. Separar proposição do ID, definição do namespace e validação ou rejeição de colisão; apenas a última é inequivocamente determinística antes de fechar a política. |
| 7 | `analysis.md:129-144`; `spells/goal/.craft/ledger.yml`; `arcana/craft/templates/ledger.schema.yml:10-12` | O texto reconhece que não existe perfil executável para `0.2.0`, mas conclui que há deriva corrente porque `active_blockers` e `active_gaps` não obedecem aos filtros de `0.3.0`. A ausência de semântica que demonstra a ambiguidade também impede concluir qual projeção é correta para 0.2. | MAJOR | Uma incompatibilidade demonstrada com 0.3 é apresentada como corrupção comprovada de um ledger 0.2. | Reformular: sob os filtros declarados em 0.3, os índices seriam incoerentes; sem um perfil 0.2, a validade e a projeção correta do ledger Goal não podem ser determinadas deterministicamente. Manter `by_id` apenas como contrato de completude em aberto. |
| 8 | `analysis.md:174-183,209-220` | O validator deve verificar versão conhecida, unicidade no namespace e reindexação sem ambiguidade, mas o documento mantém abertas a semântica 0.2, o domínio de unicidade e a completude dos índices. Mesmo assim, autoriza validator e reindexador como se ambos já fossem especificáveis por inteiro. | MAJOR | O próximo passo pode incorporar decisões de contrato não autorizadas ou alegar suporte sem base suficiente. | Limitar o primeiro slice a parser e validator parcial, somente leitura e fail-closed: validar apenas invariantes inequívocas de 0.3 e responder `unsupported/unknown` para versões ou políticas sem perfil. Autorizar o reindexador canônico somente depois de definir completude e filtros por versão. |
| 9 | `analysis.md:50-55,102,191-194` | “Versão do ledger”, versão contratual `0.2.0` ou `0.3.0` e proteção contra fonte obsoleta aparecem como se fossem a mesma identidade. `schema_version` não é token de revisão de uma instância. | MAJOR | Um aplicador poderia preservar a versão do formato e ainda sobrescrever uma edição concorrente. | Separar versão de schema de revisão ou frescor da instância. Manter hash da fonte, contador de revisão ou compare-and-swap como requisito futuro ainda não decidido. |
| 10 | `analysis.md:172-198` | A sequência validator → reindexador → aplicador é inteligível, mas “cobertas por fixtures” não define condições observáveis de conclusão nem o ciclo diagnóstico → correção → revalidação. | MINOR | O leitor entende a direção, mas não consegue aprovar ou encerrar cada estágio de modo repetível. | Acrescentar critérios mínimos: validação não altera bytes; versão sem perfil falha fechada; diagnósticos são estáveis; reindexação preserva linhas-fonte; duas execuções são idênticas; o ledger Goal é aceito por perfil conhecido ou recusado com diagnóstico estável. |
| 11 | `analysis.md:200-220` | O limite cita a avaliação adversarial, mas claims centrais não possuem links diretos para contrato canônico, schemas, ledger Goal e testemunha histórica. | MINOR | A análise é menos autônoma para verificação e obriga o leitor a usar o review intermediário como índice de evidência. | Incluir links diretos mínimos para as quatro fontes no ponto em que sustentam os claims, sem transformar a análise em relatório de evidências. |

## Artifact verdict

| Artefato | Veredito | Motivo |
|---|---|---|
| `docs/analysis/craft-ledger-evaluation/analysis.md` | FIX | A estrutura need-driven, o exemplo e a tese central são fortes, mas o documento mistura estado atual com arquitetura desejada, ensina uma classificação híbrida e autoriza validator e reindexador além das políticas já fechadas. |
| Estrutura e tom | KEEP | A progressão objetivo → contexto → exemplo → explicação → problema → recomendação → limite acompanha adequadamente o outro `analysis.md`. |
| Tese “julgamento interpretativo versus integridade mecânica” | KEEP WITH REWORDING | A distinção sobrevive, desde que inclua humano e política no lado interpretativo e separe alocação de validação de identidade. |
| Recomendação validator → reindexador → aplicador | FIX | A direção é defensável, mas o primeiro validator precisa ser parcial e fail-closed; o reindexador depende de políticas ainda abertas. |

## Change requests

1. Corrigir a promessa do documento e distinguir explicitamente contrato declarado, comportamento garantido hoje e arquitetura recomendada.
2. Reescrever o fluxo-alvo para validar o estado candidato antes do commit.
3. Corrigir o exemplo prático e a tabela para preservar as categorias gap, blocker, ator interpretativo, política de identidade e validação mecânica.
4. Tornar explícita a divisão entre linhas-fonte e índices embutidos dentro do mesmo `.craft/ledger.yml`.
5. Estreitar o claim sobre o ledger Goal: demonstrar ambiguidade de compatibilidade, não deriva conclusiva sob semântica 0.3.
6. Definir o primeiro incremento como validator parcial, read-only e fail-closed; condicionar o reindexador ao fechamento das políticas por versão.
7. Separar schema version de revisão da fonte e acrescentar critérios de aceitação para cada estágio.
8. Adicionar links diretos para as evidências canônicas.

## Evidence boundary

Esta revisão confrontou o texto literal do `analysis.md` com dois ataques
independentes e com os contratos e exemplos citados. Ela não executou um
validator Craft, porque essa superfície não existe atualmente. A revisão
confirma a divergência entre operações e schemas e a ausência de enforcement
empacotado; não confirma que um ledger `0.2.0` seja inválido sob uma semântica
que o repositório ainda não definiu.

Ela também não escolhe o namespace de IDs, o perfil legado, a completude de
`by_id` nem o mecanismo de concorrência. Essas decisões são necessárias antes
de uma implementação completa. O primeiro incremento sustentado pela evidência
é apenas um validator parcial, somente leitura e fail-closed para invariantes
já inequívocas; o reindexador canônico permanece condicionado ao fechamento das
regras que determinam sua saída.
