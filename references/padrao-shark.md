# Padrão Shark para páginas de resposta direta

Este documento registra os padrões reutilizáveis observados nas páginas aprovadas do workspace. Ele descreve decisões de implementação, não textos ou ofertas específicas de um produto.

## 1. Contrato de fidelidade

- Trate PDF, screenshot ou layout aprovado como especificação visual, não como inspiração vaga.
- Preserve a ordem narrativa da copy e a posição relativa de headline, argumento, oferta, prova, garantia e fechamento.
- Meça proporções na referência: largura útil, gutters, tamanhos de headline, espaçamento vertical, dimensões do produto e densidade do buybox.
- Não introduza seções, selos, contadores, urgência, animações ou claims que não existam no material aprovado.
- Diferencie elementos intencionais de artefatos do arquivo. Um detalhe presente em somente uma página não vira regra global sem motivo funcional.

### Implementação real obrigatória

Este contrato vale para todas as páginas da skill, incluindo todos os upsells e suas variantes:

- Construa headline, parágrafos, listas, benefícios, depoimentos, copy de garantia, FAQ, preços, quantidades, condições, botões e recusas com elementos HTML visíveis, semânticos e editáveis. Use CSS para layout, fundos, bordas, espaçamento, tipografia e responsividade; use JavaScript somente para interações necessárias.
- PDF e screenshots servem para medir e comparar a referência. Não entregue a página inteira ou seções narrativas/transacionais como screenshot, recorte de PDF, bitmap, background de imagem, canvas ou SVG de texto. SVG com bitmap embutido ou letras convertidas em paths continua sendo uma substituição gráfica, não implementação da copy.
- Botões e links têm texto visível e área interativa própria no fluxo do layout. Hotspots transparentes sobre arte da referência não implementam uma buybox ou CTA. Transcrições em `sr-only`, `alt`, `aria-label` ou blocos ocultos não compensam conteúdo visível renderizado como imagem.
- Assets visuais são elementos gráficos isolados: logo, packshot, foto, ilustração anatômica, selo, ícone e marca de pagamento. Extraia do PDF somente esse elemento quando não houver asset fornecido. Seu crop não pode carregar junto títulos, parágrafos, preços, botão ou a seção completa. Texto intrínseco ao logo, rótulo da embalagem ou selo pode permanecer no asset; a copy da página e os termos da oferta continuam em HTML.
- Gráficos e diagramas podem usar SVG/canvas para a figura; títulos, explicações, legendas e disclaimers da página permanecem texto real. Em depoimentos, use HTML para o relato, nome e estado de verificação, com foto separada; um screenshot original de uma prova externa só pode ser evidência complementar, não substituir a seção textual.
- Ajuste o layout por fluxo e breakpoints, permitindo que o texto quebre linhas naturalmente. Encolher um screenshot ou um palco inteiro com coordenadas fixas não é responsividade. Fidelidade 1:1 é o objetivo visual da reconstrução, não uma exceção a este contrato.

Antes da revisão visual, inspecione o DOM e os arquivos de mídia usados, inclusive SVGs. O aceite exige: toda a copy existente em elementos **visíveis**; preço, quantidade, CTA e recusa editáveis independentemente; e, ao ocultar temporariamente imagens/backgrounds gráficos/SVGs/canvas no navegador, a narrativa, condições da oferta, links e FAQ continuarem visíveis, legíveis e operáveis. Teste também a quebra de texto nos viewports exigidos. Compare a referência com a implementação real após restaurar os assets. Não declare conformidade com base apenas em screenshot ou transcrição oculta.

## 2. Contrato responsivo

As referências móveis aprovadas usam largura nativa de 390 ou 402 px. Preserve esse ritmo de leitura como padrão.

| Viewport | Comportamento esperado |
| --- | --- |
| 320–360 px | Reduza gutters, headlines e largura dos cards; mantenha todo o conteúdo e os CTAs utilizáveis. |
| 390–402 px | Reproduza a referência principal com máxima fidelidade. |
| 403–599 px | Mantenha shell e fundos em largura total; centralize o conteúdo em coluna de aproximadamente 390–402 px. |
| 600–767 px | Use largura total para shell, fundos e faixas, mantendo o conteúdo narrativo em coluna central de aproximadamente 390–402 px. |
| 768 px ou mais | Faixas de status, progresso e marca ocupam toda a largura da viewport; a coluna de leitura permanece estreita salvo layout desktop explicitamente aprovado. |

Regras complementares:

- Use `meta viewport` com `width=device-width, initial-scale=1` e suporte a `viewport-fit=cover` quando apropriado.
- O frame global é full-bleed: `html`, `body`, shell, fundo/página, cabeçalho, progresso e faixa de marca não podem herdar `max-width` da coluna central. Apenas o conteúdo usa `width: min(100%, 402px)` e centralização.
- Em páginas com o cabeçalho Shark de três faixas, o padrão é status de 40 px + progresso de 26 px + marca de 74 px (140 px no total), com logo em torno de 152 px.
- Em upsells cuja referência usa somente duas faixas, o padrão é marca de 67 px + alerta de 35 px (102 px no total), com logo em torno de 149 × 28 px. Não compacte essa variante para uma barra reduzida. Preserve a escala em todos os viewports, reduzindo somente o necessário para impedir recortes em telas estreitas.
- O kicker vermelho em caixa alta acima da headline é um subtítulo editorial, não microcopy. Na largura de referência de 390–402 px, use aproximadamente 13 px, peso 800–900 e contraste forte; a medida do PDF ou protótipo aprovado sempre prevalece.
- Evite alturas rígidas em blocos de texto. Altura fixa só é aceitável para elementos controlados como barras, ícones ou molduras de produto.
- Imagens e SVGs devem usar `max-width: 100%`; declare `width` e `height` intrínsecos para reduzir layout shift.
- Não permita overflow horizontal em 320 px. Verifique especialmente preços, labels, grids de benefícios e barra de progresso.
- CTAs devem continuar legíveis e acionáveis com toque. O texto não pode cortar nem transbordar.
- Não converta automaticamente o desktop em grid ou duas colunas. A continuidade vertical concentrada faz parte do padrão dessas páginas.

## 3. Arquitetura da página

Inclua somente blocos sustentados pela copy ou referência. A sequência recorrente é:

1. alerta ou estado do pedido, quando aplicável;
2. indicador do checkout com a etapa atual destacada;
3. faixa de marca;
4. hero/introdução com headline e argumento de continuidade;
5. primeira oferta;
6. mecanismo, benefícios, prova visual, gráfico, depoimentos ou FAQ conforme o material;
7. garantia;
8. repetição da oferta final;
9. recusa e eventual downsell, no ponto aprovado do fluxo.
10. footer universal obrigatório da skill, com dados/merchant da brand de destino (consulte `footer-universal.md`).

Páginas de upsell devem parecer continuação natural da compra já iniciada. Não use navegação de site, links dispersivos ou elementos que sugiram uma landing page institucional.

Quando houver várias opções de oferta:

- destaque visualmente a opção aprovada como melhor valor;
- mostre quantidade, duração, preço unitário, total, frete, bônus e economia sem ambiguidades;
- mantenha preço e CTA próximos;
- preserve a mesma ordem de opções em todas as repetições;
- use uma única definição reutilizável se a oferta reaparecer no topo e no fim.

### Estrutura obrigatória de buyboxes em upsells

- Trate cada opção como uma unidade composta por `buybox + recusa`. A recusa pertence ao fluxo da oferta, mas deve ficar **fora do contêiner visual da buybox**, centralizada e imediatamente abaixo do card.
- Nunca coloque o link `[UPSELL_DECLINE=...]` dentro do elemento que recebe fundo, borda, sombra ou padding da buybox. Use um wrapper neutro para agrupar o card e sua recusa quando houver várias opções.
- Vincule cada recusa ao mesmo identificador de produto do CTA daquela opção e preserve esse pareamento nas ofertas repetidas.
- Mantenha a recusa visualmente secundária, legível, sublinhada e com foco de teclado visível; ela não deve parecer parte do botão principal.
- Não inclua labels de preço como “Your reduced price” sem aprovação explícita na copy ou na referência.
- Calcule e confira o total exibido a partir do preço unitário e da quantidade cobrada. Garanta que bônus grátis não entrem no total.
- Exiba frete grátis somente nas variantes explicitamente elegíveis. As demais devem informar frete pago ou a condição aprovada, sem herdar o benefício da opção principal.

## 4. Sistema visual

- Derive a paleta do produto e declare tokens em `:root` para cor principal, variação escura, texto, muted, linhas, sucesso, alerta e CTA.
- Use Barlow como fonte global padrão, sempre carregada pelo Google Fonts (`fonts.googleapis.com`/`fonts.gstatic.com`) com `display=swap` e fallbacks seguros. Não use WOFF2 local para Barlow. Uma identidade ou referência que exija outra fonte explicitamente pode substituir este padrão.
- Headlines são compactas, fortes e com tracking negativo moderado. Corpo de texto prioriza leitura e contraste.
- O buybox é o principal componente transacional: produto grande, hierarquia de preço imediata, benefício do pacote visível e CTA de alto contraste.
- Use sombras, bordas e arredondamento com moderação e de modo consistente com a marca.
- Prefira SVG inline para ícones simples. Não carregue bibliotecas de ícones para poucos símbolos.
- Preserve quebras de linha intencionais somente quando elas continuam funcionando nos viewports necessários.

## 5. Copy, claims e prova

- Mantenha idioma, capitalização, pontuação e ênfases da copy aprovada.
- Não “melhore” claims de saúde, números, resultados médios, depoimentos ou garantias por conta própria.
- Gráficos conceituais precisam de rótulo acessível e disclaimer visível quando a referência os tratar como ilustração.
- Depoimentos seguem o contrato de implementação real: relato, nome e estado de verificação em HTML, preservando o texto aprovado; fotos ou evidências complementares precisam de `alt` útil.
- A garantia deve deixar prazo e condição coerentes em headline, corpo, buybox e selos.

## 6. Integrações e comportamento de conversão

Shortcodes entre colchetes são contratos da plataforma. Preserve literalmente formatos como:

- `[BUY=IDENTIFICADOR]` — CTA de compra em front, VSL, advertorial e buybox de checkout
- `[UPSELL=IDENTIFICADOR]`
- `[UPSELL_DECLINE=IDENTIFICADOR]`
- `[DOWNSELL=IDENTIFICADOR]`

O identificador é o código do catálogo (ex.: `NEM6UP1`, `GPP6V4`). Não invente código, URL de checkout nem `href="#"`. Em funis com product check, `[BUY=]` vazio só é válido quando o runtime preenche o SKU da sessão; na geração da página, prefira o código explícito do catálogo.

Antes da entrega:

- liste todos os shortcodes encontrados e compare com a especificação;
- confirme que cada CTA aponta para a variante correta;
- confirme que a recusa leva ao destino aprovado ou abre o downsell exatamente uma vez;
- não deixe `href="#"`, URLs fictícias ou placeholders descritivos parecendo integração final;
- mantenha o shortcode diretamente no `href` quando essa for a convenção da plataforma;
- verifique que scripts de modal não bloqueiam a navegação definitiva após a recusa confirmada.

Para modais/downsell:

- use `role="dialog"`, `aria-modal`, título associado e estado `aria-hidden` coerente;
- permita fechamento por botão e `Escape` quando isso não contrariar o funil aprovado;
- controle o scroll do fundo e restaure-o ao fechar;
- evite conteúdo que ultrapasse `100dvh`; corpo rolável e CTA final visível são preferíveis;
- gerencie foco quando houver interação de teclado relevante.

## 7. Assets e carregamento

- Prefira assets fornecidos e versões já aprovadas. Não troque packshot, logo, selo ou imagem de pagamento por aproximações.
- Se o destino final usar CDN, preserve URLs aprovadas. No Shark Funnels, use somente URLs já hospedadas em `assets.json` (Storage/CDN). Não invente `cdn.elasticfunnels.io` nem caminhos locais que o lead não alcança.
- Se a publicação ainda não aconteceu e não houver URL hospedada, use o caminho local funcional e documente a troca pendente.
- Use AVIF/WebP com fallback apenas quando a cadeia de hospedagem suportar essas variantes e a troca não alterar a aparência.
- Priorize somente o provável LCP: `fetchpriority="high"`, carregamento eager e, se realmente útil, um único preload correspondente.
- Aplique `loading="lazy"` às imagens abaixo da dobra. Não marque tudo como preload ou alta prioridade.
- Faça `preconnect` somente para origens realmente usadas no caminho crítico.
- Evite bibliotecas externas para efeitos que HTML/CSS resolvem. Carregue gráficos ou scripts pesados sob demanda, perto do viewport, quando forem necessários.
- Barlow deve ser carregada sempre pelo Google Fonts, com `display=swap`; não substitua essa origem por WOFF2 local. Registre a dependência externa de fonte no handoff e verifique o comportamento de fallback quando a rede estiver indisponível.

## 8. HTML, CSS, JavaScript e acessibilidade

- Use HTML semântico: `header`, `nav`, `main`, `section`, headings em ordem e nomes acessíveis para regiões e ofertas.
- Cada imagem informativa precisa de `alt`; imagens decorativas usam `alt=""`.
- Preserve foco visível, contraste e uso por teclado. Respeite `prefers-reduced-motion` quando houver transição ou animação.
- Faça reset mínimo e use `box-sizing: border-box`.
- Escopo de componentes embutidos deve evitar colisões com page builders; use um prefixo estável para buyboxes e modais quando necessário.
- No Elastic, use um wrapper full-bleed explícito no conteúdo (por exemplo, `<div class="shark-shell variante">`) para as classes de variante, tokens, fonte e demais estilos específicos. O runtime pode descartar atributos/classes do `<body>` ao montar a página; regras como `body.variante` não são uma base confiável. Confira que o wrapper sobreviveu à montagem e compare valores computados de peso/tamanho/line-height da headline e cores de buybox/benefícios no preview e na URL pública com o modelo local aprovado. O teste de glifos confirma a família, mas não substitui essa comparação de estilo.
- Não repita IDs ao clonar templates. Remova `fetchpriority` e aplique lazy loading nas cópias abaixo da dobra.
- Não dependa de JavaScript para exibir conteúdo essencial ou o primeiro CTA sem necessidade.
- Scripts externos devem falhar de forma segura: o restante da página e os CTAs continuam funcionais.

## 9. Matriz de aceitação

Antes de considerar a página pronta, confirme:

- aceite da implementação real obrigatória, incluindo inspeção de mídia e teste com assets visuais ocultos;
- fidelidade visual nos viewports de referência;
- ausência de scroll horizontal em 320, 360, 390/402, 768 e desktop largo;
- frame full-bleed confirmado no desktop largo (inclusive 2048 px), com cabeçalho/faixas nas duas bordas e conteúdo central de aproximadamente 402 px;
- escala global do cabeçalho e uso de Barlow confirmados, salvo override explícito do protótipo;
- barra de progresso, logo, headline e primeiro CTA sem recorte;
- todas as ofertas, totais, bônus, frete, garantia e recusa consistentes;
- shortcodes/URLs exatos e sem destinos vazios;
- imagens existentes, proporção correta, dimensões declaradas e sem 404;
- somente o LCP com prioridade alta; conteúdo abaixo da dobra com lazy loading;
- console sem erros relevantes;
- modal e FAQ utilizáveis por mouse, toque e teclado quando presentes;
- FAQ sinalizado nas referências conferido integralmente com o DOCX e fonte aprovada carregada no FAQ, footer e demais componentes vivos;
- footer universal presente uma única vez, sem CSS global concorrente, com merchant/contas/links da brand correta;
- nenhum ID duplicado após a montagem dos templates;
- comportamento aceitável com JavaScript externo lento ou indisponível;
- revisão final pela skill `optimizing-direct-response-pages`.

## 10. Handoff

O relatório final deve informar:

- arquivo criado ou alterado;
- viewports efetivamente inspecionados;
- shortcodes/URLs verificados;
- assets críticos e estratégia de carregamento conferidos;
- testes executados e resultado;
- limites externos ainda não mensuráveis, como CDN, runtime da Elastic Funnels/page builder, cache, analytics, fontes ou bibliotecas de terceiros.
