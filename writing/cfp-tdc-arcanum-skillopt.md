# Proposta TDC: Arcanum + SkillOpt

## Título da apresentação

Nomear, validar e evoluir skills: Arcanum, SkillOpt e agentes de IA

## Resumo da sua apresentação, para o público

Em agentes de IA, a parte mais valiosa muitas vezes não é a resposta, mas o procedimento que funcionou. E se pudéssemos nomear esse comportamento, validá-lo e evoluí-lo como uma skill versionada? Nesta palestra conecto o paper SkillOpt, que trata skills como estado textual externo otimizado por feedback, ao Arcanum, um framework para governar sigils e spells de agentes. Mostro arquitetura, código e um fluxo mínimo para sair de prompt solto para capacidade auditável.

## Mensagem privada: conte-nos mais sobre a apresentação

Esta proposta nasce de um problema muito prático da engenharia de agentes: quando um agente resolve bem uma tarefa, quase sempre perdemos a parte mais valiosa do processo, que é o método reutilizável por trás da resposta. O histórico fica espalhado em prompts, logs, comentários, arquivos temporários e decisões implícitas. A próxima execução começa mais inteligente só se alguém souber reconstruir o caminho. Por isso, a palestra trata o ato de nomear como o primeiro passo de governança: se uma equipe não consegue nomear uma capacidade, também não consegue testá-la, delegá-la, observar sua evolução ou decidir quando ela deve ser bloqueada.

Quero apresentar o Arcanum como uma resposta experimental a esse problema: uma infraestrutura para transformar comportamento útil de agentes em capacidades governadas e nomeáveis. No Arcanum, sigils representam capacidades reutilizáveis, spells representam composições de workflow, validadores checam contratos, observabilidade registra sinais de execução e um experiment harness permite testar se uma capacidade realmente cumpre o que promete. A palestra não trata "skill" como uma instrução bonita, mas como artefato de engenharia: algo com nome, intenção, fronteiras, critérios de uso, modos de falha, exemplos, evidências, revisão e ciclo de vida definido.

A principal referência será o paper "SkillOpt: Executive Strategy for Self-Evolving Agent Skills" (arXiv:2605.23904, maio de 2026). O paper formula uma ideia importante para quem constrói agentes: a skill pode ser tratada como estado textual externo de um agente congelado. Em vez de mudar pesos do modelo, um otimizador propõe edições controladas na skill a partir de trajetórias; essas edições passam por limite textual de mudança, buffer de rejeições e gate de validação antes de serem aceitas. Minha proposta é conectar essa linha de pesquisa com a pergunta operacional que vem logo depois: se skills podem evoluir, que governança precisamos em volta delas para que uma equipe consiga auditar, validar, bloquear e reutilizar essa evolução?

A apresentação será avançada, mas prática. O público-alvo são pessoas que já constroem agentes, automações com LLMs, ferramentas de developer workflow, plataformas internas de IA ou sistemas multiagente. Pretendo mostrar slides e código em um fluxo pequeno: partir de um prompt ou skill inicial, explicitar o contrato da capacidade, adicionar fixture de validação, registrar evidência operacional e discutir como um loop inspirado em SkillOpt poderia propor mudanças controladas sem transformar o sistema em auto-reescrita sem freio.

O interesse vem do meu trabalho contínuo com agentes em repositórios longos, onde a pergunta central deixou de ser "o modelo respondeu bem?" e virou "conseguimos preservar, validar e melhorar o método que produziu uma boa resposta?". Depois de muitas iterações com prompts, skills locais, handoffs, validadores e workflows de código, ficou claro que a fronteira relevante está entre prompt engineering, engenharia de software, LLMOps e governança operacional. O Arcanum é o projeto concreto que estou usando para explorar essa fronteira.

Referências planejadas:
- SkillOpt: Executive Strategy for Self-Evolving Agent Skills, arXiv:2605.23904
- Artefatos do Arcanum sobre sigils, spells, invoke, observability e experiment harness
- Material já escrito em `writing/substack/introducing-arcanum.md`
- Exemplo de código local demonstrando contrato, validador e registro de evidência

## Idioma principal

Português

## Trilha da sua proposta

Trilha Agentic AI

## Tipo de palestra

Palestra (35 min)

## Nível da audiência

Para audiência avançada

## Que tipo de apresentação será?

Slides e código

## Confirmações

Política de privacidade: Sim, eu li e estou ciente da política de privacidade do evento.

Gravação e slides: Sim, autorizo a gravação da minha palestra e disponibilização dos slides da minha apresentação.

Presencialidade: Sim, eu estou ciente de que a palestra deve ser apresentada presencialmente quando a trilha não é digital.

## Fontes usadas

- https://arxiv.org/pdf/2605.23904
- https://thedevconf.com/tdc/2026/florianopolis/trilha-agentic-ai
- `writing/substack/introducing-arcanum.md`
