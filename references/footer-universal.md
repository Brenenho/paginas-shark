# Footer universal Shark

Todas as páginas produzidas com esta skill incluem uma única cópia de `assets/footer-universal.html` antes de `</body>`, com CSS e JavaScript inline. O fragmento deriva do footer Oilbase-20, componente Elastic 1704, mas usa HTML nativo e configuração separada. Funciona sem registrar um componente remoto em cada brand; um componente compartilhado é uma alternativa de manutenção, não uma dependência.

## Configuração obrigatória por destino

Preencha o JSON `shark-footer-config` na página usando os dados reais da brand: `brandName`, `domains`, `links`, `merchants`, `trackingEnabled` e `trackConversion`. Busque domínios/merchants, variáveis e footer existente via CLI quando o destino for Elastic. O arquivo `assets/footer-oilbase20.config.json` contém somente a configuração Oilbase-20 recuperada do componente original; aplique-o somente a páginas desse produto, verificando os valores atuais antes de publicar.

- `domains`: mapa de hostname exato para `{merchant, brandName}`. Registre explicitamente variantes `www` ou outros domínios aprovados; o fragmento não adivinha a brand pelo domínio.
- `links`: URLs das páginas reais de contato, privacidade, termos e reembolsos. Use URLs absolutas quando o HTML também puder ser hospedado fora do domínio da brand.
- `merchants.buygoods`: conta, lista de produtos e token público do pixel quando já aprovados para essa etapa.
- `merchants.clickbank.vendor`: vendor real da brand.
- `merchants.digistore24.disclaimer`: copy aprovada quando essa integração for usada; a origem Oilbase não forneceu conteúdo para esse bloco. Integre seu tracking somente a partir do código aprovado do destino.
- `trackingEnabled`: habilita os scripts de atribuição aprovados. `trackConversion`: habilita o pixel de conversão BuyGoods somente em uma etapa que já o utiliza ou tenha autorização específica. Ter footer em toda página não autoriza disparar conversões em toda página.

Contas, vendors, produtos e URLs de uma brand pertencem àquela brand. Para outra brand, configure dados reais; se faltarem dados, entregue a parte comum do footer e informe o bloqueio de integração, sem usar silenciosamente Oilbase como fallback.

## Seleção de merchant

No Elastic, preserve `data-elastic-merchant="{{ request.merchant_code }}"` e `data-elastic-brand="{{ var.offer_name }}"` no footer. Essas expressões são oficiais e devem ser conferidas no preview: o merchant ativo inclui a seleção do domínio e o contexto estabelecido por Page Events. Código de checkout, avisos legais e trackers precisam concordar.

Fora do Elastic, remova esses dois atributos da cópia destinada à hospedagem externa. O mesmo HTML usa `location.hostname` e o mapa `domains`; um checkout dinâmico externo chama `window.SharkFooter.setMerchant('buygoods')` ou outro merchant configurado. `clearMerchant()` retorna à resolução padrão e `refresh()` relê o contexto. Esse adaptador deve ser chamado pela integração confiável do checkout, não por parâmetros livres da URL.

A prioridade é: merchant explícito do adaptador → contexto renderizado pelo Elastic → configuração do hostname → `defaultMerchant` aprovado. Um merchant sem bloco/configuração mantém somente links e copyright. Selecione um bloco por vez; os outros ficam em `<template>` inerte. Trackers são carregados uma vez por conta/vendor na página e o footer não executa compras.

## Aparência e aceitação

O CSS está escopado em `#shark-footer`, usa `--shark-page-font`/Barlow e não altera fontes do corpo, FAQ ou buyboxes. Carregue Barlow no `<head>` da página pelo Google Fonts, conforme a skill; a fonte do último modelo aprovado permanece a autoridade quando existir override explícito.

Execute `scripts/validate-footer.py` (Playwright e Chrome; `--chrome` aceita outro executável) e confira também o preview real do Elastic. O teste cobre BuyGoods, ClickBank, contexto do servidor prioritário, merchant/domínio desconhecidos, override e retorno ao padrão, scripts únicos e ausência de alteração global da fonte. Testes/preview interceptam scripts e iframes de tracking; não criam conversões reais. Confira links reais, ano/marca, logo, ausência de carga de imagens de templates inativos e fonte aprovada após a montagem. Preserve comentários sem tags estruturais de fechamento escritas literalmente: o parser HTML do Elastic pode encerrar o documento ao encontrá-las até em comentários. Nenhum `efmeta` de componente antigo entra no fragmento ou numa duplicação.

Fontes oficiais: [Merchant Containers](https://docs.elasticfunnels.io/pages/containers#merchant-container), [contexto do request](https://docs.elasticfunnels.io/pages/page-variables#available-request-fields) e [componentes](https://docs.elasticfunnels.io/backend-template-engine/directives#components-component).
