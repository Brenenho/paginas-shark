---
name: paginas-shark
description: Cria e implementa páginas de resposta direta em HTML/CSS real no padrão Shark a partir de copy, PDFs, imagens, assets e especificações aprovadas. Use somente quando o usuário invocar explicitamente $paginas-shark ou pedir pela skill Paginas Shark.
metadata:
  short-description: Cria páginas de resposta direta no padrão Shark
---

# Páginas Shark

Crie páginas de funil em HTML/CSS real, visualmente fiéis, prontas para integração e rápidas na prática. Esta skill é de invocação explícita: não a aplique silenciosamente a pedidos comuns de frontend.

## Leia o padrão antes de agir

Leia sempre [references/padrao-shark.md](references/padrao-shark.md) antes de criar ou alterar uma página. O arquivo contém o contrato visual, responsivo, transacional e de entrega derivado das páginas aprovadas.

## Determine a fonte de verdade

Antes de implementar:

1. Leia as instruções locais, especialmente `AGENTS.md`, e preserve regras mais específicas do projeto.
2. Inventarie copy, PDFs, screenshots, imagens, fontes, HTML existente e shortcodes fornecidos.
3. Identifique o tipo de página: landing page, TSL/VSL, advertorial, checkout, upsell, downsell ou etapa híbrida.
4. Registre internamente o que está aprovado versus o que é apenas inferência.

Use esta precedência quando houver conflito:

1. pedido explícito mais recente do usuário;
2. comportamento de conversão e integrações já aprovados no código;
3. referência visual aprovada para o viewport correspondente;
4. copy ou roteiro aprovado;
5. inferência conservadora.

Não invente preço, quantidade, economia, frete, garantia, alegação, depoimento, URL ou shortcode. Quando faltar um dado transacional indispensável, use um placeholder inequívoco somente se isso permitir continuar e informe que a integração ainda não está pronta.

## Implemente a página

- Implemente o [contrato de HTML/CSS real](references/padrao-shark.md#implementação-real-obrigatória) em toda página, inclusive upsells e variantes. PDF e screenshots são referências de comparação, não a página entregue. Fidelidade 1:1 não autoriza substituir seções por imagens, SVGs de texto ou recortes com hotspots.
- Preserve a copy aprovada literalmente, salvo pedido explícito de edição. Corrija apenas erros técnicos que prejudiquem a renderização.
- Reproduza hierarquia, ordem, ritmo, proporções, cores e componentes da referência; não transforme a página em um template genérico de SaaS.
- Adote por padrão um `index.html` autocontido, com CSS e JavaScript mínimos, quando o projeto não exigir framework ou estrutura diferente.
- Trate a página como mobile-first. A referência de 390–402 px é a base comum do padrão; no desktop, preserve a coluna estreita central e deixe o frame, fundos e faixas de status, progresso e marca ocuparem toda a largura da viewport. Uma especificação desktop aprovada sempre substitui esse padrão.
- Aplique este frame global salvo especificação mais recente em contrário: `html`, `body`, shell, fundos, cabeçalho, progresso e faixa de marca usam 100% da largura; somente o conteúdo narrativo/transacional fica em `width: min(100%, 402px)` com `margin-inline: auto`. Em 2048 px, a superfície do cabeçalho e do fundo deve chegar às duas bordas da viewport, enquanto a coluna continua com aproximadamente 402 px.
- Quando houver o cabeçalho Shark de três faixas, use como padrão global 40 px para o status, 26 px para o progresso e 74 px para a faixa de marca (140 px no total), com logo de aproximadamente 152 px. Na variante de upsell com somente marca e alerta, use 67 px para a faixa de marca e 35 px para o alerta (102 px no total), com logo de aproximadamente 149 × 28 px. Ajuste apenas para evitar recorte em telas muito estreitas ou quando um protótipo aprovado exigir outra proporção.
- Trate o kicker vermelho em caixa alta acima da headline como subtítulo editorial, não como microcopy: use aproximadamente 13 px e peso 800–900 na referência móvel de 390–402 px, salvo medida diferente no protótipo aprovado.
- Use Barlow como fonte padrão da página, incluindo corpo, títulos, barras, ofertas e CTAs. Barlow deve ser sempre carregada pelo Google Fonts (`fonts.googleapis.com`/`fonts.gstatic.com`) com `display=swap` e fallback seguro; não empacote WOFF2 local para substituir essa origem. Uma fonte diferente só pode substituir Barlow por pedido explícito mais recente ou referência aprovada que a exija.
- Fixe a fonte aprovada no shell e em todo o conteúdo textual (inclusive FAQ e footer); carregue os pesos realmente usados. Ao adicionar componentes do Elastic ou otimizar a página, confira a fonte efetivamente renderizada após `document.fonts.ready`, não apenas a declaração CSS. Compare novamente com o último modelo aprovado. Estilos do builder/footer ficam escopados e não mudam a tipografia da página. Reconstrua a copy da referência em elementos HTML visíveis; a aparência de texto dentro de uma imagem não comprova o uso da fonte aprovada.
- Crie ajustes reais para telas estreitas e largas, sem overflow horizontal, recortes, texto ilegível ou CTAs difíceis de tocar.
- Use componentes de oferta claros e consistentes. Se o mesmo bloco reaparecer, derive as cópias de uma única fonte no DOM, como `<template>`, sem duplicar IDs nem reexecutar efeitos indevidos.
- Preserve shortcodes da plataforma exatamente como foram aprovados (`[BUY=CODE]`, `[UPSELL=CODE]`, `[UPSELL_DECLINE=CODE]`, `[DOWNSELL=CODE]`). Não os reescreva, codifique ou substitua por links imaginados.
- Use JavaScript apenas para comportamento necessário. Prefira HTML/CSS nativos e JavaScript vanilla quando suficientes.
- Mantenha seletores de componentes sensíveis escopados para reduzir colisões com page builders.
- No Elastic, aplique variantes, tokens de cor e fonte em um wrapper HTML explícito preservado dentro do conteúdo, conforme o [contrato de integração](references/padrao-shark.md#8-html-css-javascript-e-acessibilidade). Valide no preview e na URL pública também peso, tamanho e cores dos componentes; a família correta sozinha não comprova que o estilo aprovado sobreviveu ao builder.

## Footer obrigatório em todas as páginas

Leia [references/footer-universal.md](references/footer-universal.md) e incorpore [assets/footer-universal.html](assets/footer-universal.html) uma única vez no HTML de toda página feita com esta skill. Configure a brand e os merchants/domínios reais do destino. O fragmento inclui HTML, CSS escopado e adaptador vanilla, funciona no Elastic e fora dele e não depende de um componente remoto. A configuração Oilbase em `assets/footer-oilbase20.config.json` é um exemplo operacional exclusivo dessa brand, não um fallback global. Confira seleção do checkout e tracking, além da fonte, após montar o footer.

## FAQ a partir do DOCX

Quando PDF ou DOCX sinalizar um FAQ, leia a seção correspondente do DOCX e use literalmente todas as perguntas **e respostas**, na mesma ordem, preservando pontuação, idioma e ênfases. O PDF determina posição e visual; o DOCX fornece o conteúdo, inclusive quando o PDF mostra apenas um marcador de FAQ. Confira cada par renderizado com o DOCX, permitindo normalizar somente espaços/quebras de linha na comparação. Use acordeões nativos `<details open>` com `<summary>`: iniciam abertos e permitem fechar/reabrir, salvo instrução explícita diferente. Fonte e pesos seguem a tipografia aprovada da página. Se a referência sinalizar FAQ e faltar o DOCX ou o conteúdo divergir entre fontes, solicite a fonte/decisão necessária em vez de inventar perguntas, resumir respostas ou transplantar FAQ de outra página.

## Valide antes de entregar

Faça verificação proporcional ao risco, incluindo:

- inspeção visual em 320/360 px, 390 ou 402 px, 768 px e desktop largo;
- aceite do contrato de HTML/CSS real: copy visível e selecionável no DOM, ofertas nativas e conteúdo preservado ao ocultar os assets visuais; transcrição oculta ou igualdade de pixels com um screenshot não satisfazem esse aceite;
- teste de CTAs, links de recusa, downsell/modal e repetição de ofertas;
- auditoria de shortcodes, assets remotos, console, overflow e navegação por teclado;
- checagem da fonte realmente carregada no conteúdo, FAQ e footer; igualdade de todas as perguntas/respostas com o DOCX; footer único e merchant compatível com o checkout, no HTML externo e no preview Elastic;
- checagem de dimensões de imagens, prioridade do LCP e lazy loading abaixo da dobra.

Para páginas HTML/Elastic, execute `scripts/check-fonts.py --url URL --selector SELETOR_DE_TEXTO --selector '#shark-footer nav a'`, incluindo seletores da headline, corpo, buybox e pergunta do FAQ quando presentes. O teste consulta os glifos renderizados via Chrome, identifica fallback e bloqueia os pixels conhecidos durante a verificação. Para uma fonte aprovada diferente, informe `--font`; para preview com segredo, passe a URL por `SHARK_FONT_CHECK_URL`. Confira separadamente os assets gráficos permitidos, como logos e selos; eles não substituem os testes da copy em HTML.

## Revisão de fidelidade antes da otimização

Faça duas revisões explícitas contra a referência fornecida, usando a mesma largura de viewport e a precedência de fontes definida acima:

1. **Conteúdo:** confronte cada bloco visível, na ordem, com a referência. Confira texto, ênfase, quantidade, preço, frete, garantia, depoimentos, FAQ, oferta repetida, CTA e recusa. Corrija toda divergência não aprovada e registre qualquer diferença deliberada exigida por uma instrução mais recente.
2. **Visual:** capture a página renderizada e compare lado a lado ou sobreposta à referência. Confira posição, largura, altura, tipografia, quebras, cores, espaçamento, imagens e proporções dos componentes. Ajuste e capture novamente até não restar diferença visual não aprovada no viewport de referência; depois confira os demais viewports exigidos.

Só conclua estas revisões quando o contrato de HTML/CSS real estiver atendido e conteúdo e visual corresponderem à referência, ou quando cada desvio visual restante estiver justificado pelo pedido do usuário. Ao corrigir uma página existente baseada em recortes, reconstrua seus blocos antes de considerá-la conforme; atualizar esta skill não corrige nem republica automaticamente páginas anteriores. Faça a otimização em seguida e repita a comparação se ela alterar a apresentação.

Como última etapa de implementação, invoque a skill `optimizing-direct-response-pages`. Preserve o comportamento de conversão aprovado enquanto aplica as correções justificadas por essa revisão. Se ela não estiver disponível no ambiente, execute o checklist equivalente e declare a limitação.

Na entrega, diga objetivamente quais viewports, integrações, assets e verificações de desempenho foram conferidos. Identifique limites externos, como CDN, fonte de terceiros, biblioteca remota, runtime do page builder ou ausência do ambiente final de hospedagem.
