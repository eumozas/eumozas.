# Playbook diário: Instagram @moisesbsilvaa

Campanha de 10 dias (13/10/2026 a 22/10/2026): um post por hora, das 8h às 20h (horário de Brasília), publicado automaticamente pelo Metricool.

- **Metricool:** blogId `7186095`, rede `instagram`, fuso `America/Sao_Paulo`, `autoPublish: true`
- **Repositório:** `eumozas/eumozas.` (branch `main`). As imagens ficam em `posts/AAAA-MM-DD/` e a URL pública é `https://raw.githubusercontent.com/eumozas/eumozas./main/<caminho>`
- **Gerador:** `python3 automacao/gerar.py automacao/dias/AAAA-MM-DD.json --push`, que gera as artes 1080×1350 e imprime `HH:MM <url>` para cada post

## Grade do dia (13 horários)

| Hora | Tipo (`tipo`) | Conteúdo |
|---|---|---|
| 08:00 | `frase` | Motivacional para começar o dia, com uma foto do Moises |
| 09:00 | `noticia` | Tecnologia, redes sociais ou IA (Instagram, Meta, TikTok, OpenAI, Google, Apple…) |
| 10:00 | `ia` | Série "IA no dia a dia". **De 14 a 20/10 já está agendada; não criar.** Em 21/10 use `numero` 8 e em 22/10 `numero` 9 |
| 11:00 | `servico` | Um serviço do Moises (estratégia, conteúdo, identidade visual) com CTA do diagnóstico |
| 12:00 | `noticia` | Política ou Brasil, no quadro "O que você acha disso?" |
| 13:00 | `frase` | Bastidores ou trabalho de videomaker e fotógrafo |
| 14:00 | `servico` | Dica prática de Instagram (eyebrow "Dica de Instagram") |
| 15:00 | `noticia` | Economia ou finanças (dólar, Bolsa, juros, inflação, Pix) |
| 16:00 | `frase` | Frase de impacto sobre ideias, atitude e execução |
| 17:00 | `servico` | Diagnóstico gratuito, portfólio ou clientes |
| 18:00 | `noticia` | Lançamentos digitais, produtos, empreendedorismo e economia criativa |
| 19:00 | `noticia` | Assunto do dia que mais gera debate (pode ser política), sempre neutro |
| 20:00 | `boanoite` | Reflexão curta de boa noite |

Além disso, o **Bom dia às 05:00** já está agendado de 14 a 20/10. Em 21 e 22/10, crie também um Bom dia às 05:00 (`tipo: frase`, `foto: cidade.jpg`, `eyebrow` com o dia da semana).

## Procedimento

1. Veja a data de hoje. Se for depois de **2026-10-22**, não crie nada: a campanha terminou.
2. Consulte o Metricool (`getScheduledPosts`, de hoje 00:00 a 23:59, fuso America/Sao_Paulo). **Não crie posts em horários que já tenham um post agendado ou publicado.**
3. **Pesquise as notícias do dia** com WebSearch e WebFetch, em fontes jornalísticas reconhecidas, com notícias das últimas 24 a 48 horas. Confira os números na fonte. Não invente dados.
4. Escreva `automacao/dias/AAAA-MM-DD.json` com os posts que faltam (veja os campos em `gerar.py` e o exemplo `dias/2026-10-13.json`). Cada post precisa de `hora`, `tipo`, os campos do modelo, `legenda` e `alt`.
5. Rode `python3 automacao/gerar.py automacao/dias/AAAA-MM-DD.json --push`.
6. Abra 2 ou 3 artes com a ferramenta Read para conferir se nenhum texto vazou ou ficou cortado. Se precisar, ajuste o JSON e rode de novo.
7. Agende cada post no Metricool (`createScheduledPost`) com a URL impressa pelo gerador, `publicationDate` = data + hora, timezone `America/Sao_Paulo`, `autoPublish: true`, `instagramData: {"type":"POST","isAiGenerated":false}`, `mediaAltText` = alt.
8. Faça o commit do JSON do dia no repositório.

## Regras de conteúdo

- **Identidade:** Moises Silva é **fotógrafo, videomaker e estrategista de Instagram** (não é piloto). Site: moisessilva.netlify.app. Diagnóstico: moisessilva.netlify.app/#diagnostico. WhatsApp: (15) 99256-5006.
- **Fontes nas artes:** Bebas Neue e Source Sans 3 (já estão no gerador). Não usar outras.
- **Fotos:** use só as fotos do Moises em `automacao/fotos/` (retrato-pb, notebook-sofa, aviao, pensativo, selfie-mesa, cidade). Varie ao longo do dia. **Não use fotos de terceiros** (jornais, revistas, agências), nem logos de veículos.
- **Notícias:** tom neutro e factual. Em temas políticos, apresente os dois lados quando houver acusação e resposta, e não tome partido. Sempre cite as fontes na arte (`fontes`) e na legenda. Feche com "O que você acha disso?" e "Comente com respeito 👇".
- **Pesquisas eleitorais:** só divulgue com todos os dados: instituto, contratante, período, amostra, margem de erro, nível de confiança e **número de registro no TSE**, na arte e na legenda (exigência da lei eleitoral). Se faltar o registro, não publique a pesquisa.
- **Legendas:** português do Brasil, 3 a 8 parágrafos curtos, emojis com moderação, uma pergunta para gerar comentários e 4 a 6 hashtags. Nos posts de serviço, inclua o site e o WhatsApp.
- **Variedade:** não repita frase, tema ou foto no mesmo dia. Consulte os JSON dos dias anteriores em `automacao/dias/` para não repetir conteúdo.
- **Destaques:** use `<em>palavra</em>` para destacar em dourado e `<b>texto</b>` para negrito nos tópicos.
