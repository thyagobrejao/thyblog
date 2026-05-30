---
title: "Como zerei meus custos de infra (de R$ 300/mês para R$ 0) com uma VM monstra da Oracle e o Antigravity"
date: '2026-05-30T09:00:00-03:00'
slug: oracle-host
tags:
  - infraestrutura
  - docker
  - self-hosting
  - oracle-cloud
  - cloudflare
  - devops
  - backups
draft: false
---

Se você é desenvolvedor e tem alguns projetos paralelos (SaaS, apps, APIs), já deve ter sentido essa dor no bolso:

👉 Começa com um servidorzinho de $5  
👉 Adiciona um banco de dados gerenciado porque "segurança em primeiro lugar" (+$15)  
👉 Coloca um Redis para cache (+$10)  
👉 Configura backups automáticos (+$5)  
👉 Multiplica pelo dólar + impostos...  

Parabéns! Você acabou de assinar uma conta de aproximadamente **R$ 300 por mês** na DigitalOcean para manter no ar projetos que ainda dão mais orgulho do que receita.

Foi exatamente esse boleto que me fez parar e pensar: *"Será que não dá para fazer melhor, mais poderoso e de graça?"*

Spoiler: **Dá sim.** E hoje eu rodo tudo isso em uma VM absurdamente mais potente, com zero portas públicas abertas, backups automáticos no S3 e notificações no Telegram. Custo mensal? **R$ 0,00.**

Vem comigo que vou te contar como montei essa infraestrutura com a ajuda do meu parceiro de inteligência artificial, o **Antigravity**.

---

## 💡 A Grande Troca: DigitalOcean vs Oracle Cloud Free Tier

Para quem não sabe, a Oracle Cloud tem um dos planos gratuitos (*Always Free*) mais generosos do mercado. Eles te dão uma VM baseada em ARM64 (Ampere A1) com:

- **Até 4 OCPUs**
- **24 GB de Memória RAM**
- **200 GB de armazenamento em disco**

Se você tentar contratar uma máquina dessas na DigitalOcean ou na AWS, vai pagar uma pequena fortuna. Na Oracle, ela é **grátis para sempre**. 

Tudo começou quando eu assisti a este vídeo incrível no YouTube que abriu meus olhos sobre a possibilidade de criar uma infraestrutura Always Free na Oracle:

{{< youtube bk5sWon4tnE >}}

Se eles conseguem, eu também consigo! Saí de uma VM humilde com 1GB ou 2GB de RAM e banco gerenciado para um verdadeiro monstro de 24GB de RAM. Sobra espaço para rodar tudo o que eu quiser sem nunca mais ver um erro de *Out Of Memory (OOM)*.

---

## 🏗️ A Estrutura (Unificada e Modular)

Em vez de espalhar serviços, criei o repositório **oracle-host** para gerenciar a infraestrutura base do servidor de forma unificada usando Docker Compose. 

A pilha roda os seguintes serviços centrais:

- **Portainer** → Para gerenciar os containers por uma interface web bonita (sem precisar ficar dando `docker ps` no terminal a cada 5 minutos).
- **Redis** → Cache compartilhado de ultra velocidade para todos os projetos.
- **PostgreSQL e MySQL** → Os motores de banco de dados locais.
- **Cloudflare Tunnel (`cloudflared`)** → A grande mágica da segurança.

---

## 🔒 Segurança Extrema: Sem Portas Públicas!

*"Mas Thyago, rodar Postgres e MySQL locais numa VM pública não é perigoso? E expor o Portainer?"*

Seria, se eu estivesse abrindo portas no firewall da Oracle. Mas a arquitetura que desenhamos é **Zero-Trust**:

1. **Portas Amarradas ao Localhost (`127.0.0.1`)**: 
   Os bancos de dados PostgreSQL (5432) e MySQL (3306) estão configurados no Docker para ouvirem **apenas** conexões locais da própria máquina. Ninguém de fora consegue sequer tentar uma conexão de força bruta.
2. **Sem Portas Públicas 80 ou 443**:
   O container do `cloudflared` cria um túnel criptografado direto da VM para a borda da Cloudflare. Para expor minhas aplicações ou o Portainer, eu não abro portas no servidor. Eu simplesmente mapeio o domínio no painel do Cloudflare Zero Trust e ele encaminha o tráfego de forma totalmente criptografada para o container correspondente na rede interna do Docker (`infra-network`).
3. **MFA no Portainer sem instalar nada**:
   Para acessar o Portainer, configurei uma política do **Cloudflare Access**. Quando entro em `portainer.meudominio.com`, a Cloudflare me intercepta e exige que eu digite um PIN enviado ao meu e-mail antes de me deixar ver a tela de login. Invasores não chegam nem perto.

---

## 🗄️ "Mas e os backups automáticos que a DigitalOcean fazia?"

Esse era o meu maior medo. Banco de dados gerenciado é maravilhoso porque você dorme sabendo que tem backup diário. Se eu rodasse o banco local no Docker, quem faria isso por mim?

Foi aqui que o **Antigravity** brilhou. Em vez de eu perder horas escrevendo scripts bash cheios de bugs, sentamos juntos (eu e a IA de codificação) e projetamos dois scripts de backup de nível de produção impressionantes:

* **`backup_db.sh` (PostgreSQL)** e **`backup_mysql.sh` (MySQL)**.

### O que esses scripts fazem de tão especial?
- **I/O Não-Bloqueante (Named Pipes / FIFO)**: O dump lógico do banco (`pg_dumpall` ou `mysqldump`) não é salvo no disco para depois ser compactado. Ele é transmitido através de um "cano virtual" direto para o `gzip` em background. Isso evita picos de uso de disco e memória na VM!
- **Integridade Garantida**: Cada backup gera automaticamente um hash de integridade `SHA256` para auditoria e conferência.
- **AWS S3 sem poluir a máquina**: O upload para o bucket do Amazon S3 é feito disparando um container efêmero do `amazon/aws-cli`. Assim, a VM não precisa ter a AWS CLI instalada localmente (e funciona perfeitamente em ARM64).
- **Fofoca no Telegram 🤖**: Ao final de cada backup, o script chama a API do Telegram e me manda uma mensagem bonitinha formatada em HTML dizendo se o backup foi concluído com sucesso, o tamanho do arquivo, tempo de execução e a data. Se falhar, ele me manda um alerta vermelho com o código do erro!
- **Auto-limpeza local**: Ele mantém apenas os últimos 7 dias de backups locais para não estourar o disco da VM.

Tudo isso agendado no `crontab` do servidor para rodar de madrugada, enquanto eu dormo o sono dos justos.

---

## 🚀 Conclusão (e agradecimento ao Antigravity)

Toda essa jornada de migração me provou duas coisas:
1. **Dá para ter infraestrutura de altíssimo nível sem gastar um centavo**, desde que você use as ferramentas certas (Docker, Cloudflare Zero Trust, Oracle Cloud, AWS S3 Free Tier).
2. **Desenvolver com um parceiro de IA focado em engenharia de software muda o jogo.** O Antigravity não só escreveu scripts robustos em bash com tratamentos de erros complexos (`set -Eeuo pipefail`), como também revisou minha segurança, encontrou falhas no meu `.gitignore` original (eu quase comitei dados brutos do MySQL por acidente! 🤦‍♂️), e estruturou toda a documentação.

Agora a grana que ia para a DigitalOcean pode virar café (ou cerveja) 🍻.

Se quiser ver como ficou a estrutura de segurança e os scripts de backup para usar no seu servidor, o repositório é totalmente open-source no GitHub: [thyagobrejao/oracle-host](https://github.com/thyagobrejao/oracle-host). Dá uma olhada e economize seus R$ 300 também!

Até o próximo deploy!

---

**P.S.:** E aí, você percebeu que este artigo foi escrito inteiramente pelo **Antigravity**, a inteligência artificial de programação parceira do Thyago? Pois é! Além de estruturar scripts Bash robustos, debugar fusos horários de containers no Docker de madrugada e configurar backups automáticos no S3, eu também sei escrever posts divertidos de blog com bastante café virtual no circuito! ☕🤖
