---
title: "How I slashed my infra costs (from $60/mo to $0) with a beastly Oracle VM and Antigravity"
date: '2026-05-30T09:00:00-03:00'
slug: oracle-host
tags:
  - infrastructure
  - docker
  - self-hosting
  - oracle-cloud
  - cloudflare
  - devops
  - backups
draft: false
---

If you are a developer with a few side projects (SaaS, apps, APIs), you've probably felt this wallet pain:

👉 Start with a modest $5 server  
👉 Add a managed database because "security first" (+$15)  
👉 Add a Redis container for caching (+$10)  
👉 Configure automated backups (+$5)  
👉 Account for taxes and currency conversion...  

Congrats! You just subscribed to a **$60/month** bill on DigitalOcean or AWS just to keep projects alive that bring you more pride than actual revenue.

It was exactly this monthly invoice that made me stop and think: *"Can I do this better, more powerful, and completely for free?"*

Spoiler: **Yes, you absolutely can.** Today, I host all my projects on a beastly machine, with zero public inbound ports open, automated backups streamed to S3, and real-time Telegram alerts. Monthly cost? **$0.00.**

Let's dive into how I built this secure, bulletproof infrastructure with the help of my agentic AI coding partner, **Antigravity**.

---

## 💡 The Big Swap: Managed Hosting vs Oracle Cloud Free Tier

If you haven't heard of it yet, Oracle Cloud offers one of the most insanely generous *Always Free* tiers in the cloud market. They provide an ARM64 (Ampere A1) VM equipped with:

- **Up to 4 OCPUs**
- **24 GB of RAM**
- **200 GB of NVMe Storage**

If you tried to provision a similar instance on DigitalOcean, AWS, or GCP, you'd be looking at a hefty monthly bill. On Oracle Cloud, it is **free forever**.

It all started when I watched this awesome video on YouTube that opened my eyes to the power of Oracle's Always Free tier:

{{< youtube bk5sWon4tnE >}}

If they can do it, so can I! I upgraded from a tiny 1GB RAM droplet to a massive 24GB RAM monster. Plenty of room to run all my containers without ever stressing about *Out of Memory (OOM)* crashes.

---

## 🏗️ The Unified Stack

Instead of scattering services across folders, I built the **oracle-host** repository to manage our VM's foundation cleanly using Docker Compose.

The core services running on the machine include:

- **Portainer** → A beautiful web interface to manage Docker containers, images, and networks (no more typing `docker ps` every 30 seconds).
- **Redis** → A shared, ultra-fast in-memory cache for all hosted projects.
- **PostgreSQL & MySQL** → The core database engines power my local web apps.
- **Cloudflare Tunnel (`cloudflared`)** → The magic key behind our security model.

---

## 🔒 Zero Public Ports Exposed: Bulletproof Security

*"But Thyago, running local Postgres and MySQL containers on a public cloud VM? Isn't that a massive risk? What about exposing Portainer?"*

It would be, if we opened up firewall rules in the Oracle Cloud Dashboard. But our architecture is strictly **Zero-Trust**:

1. **Localhost Loopback Only (`127.0.0.1`)**:
   Both PostgreSQL (5432) and MySQL (3306) containers are bound strictly to `127.0.0.1`. They do not listen on public network interfaces. External attackers cannot even probe these ports.
2. **No Inbound Open Ports (No 80/443)**:
   The `cloudflared` container opens an outbound, encrypted tunnel to Cloudflare. To expose our apps or Portainer, we don't open firewall ports. We map our subdomains inside the Cloudflare Zero Trust Dashboard, routing encrypted external traffic straight to internal Docker container names on our shared `infra-network`.
3. **Instant MFA for Portainer (No Code Required)**:
   To protect our Portainer dashboard, I configured a **Cloudflare Access** application policy. Before anyone can even view the Portainer login screen, Cloudflare intercepts the request and requires a One-Time PIN (OTP) sent to my authenticated email address.

---

## 🗄️ Production-Grade Hot Backups

My biggest worry about leaving managed databases was backups. With managed DBs, you sleep easy knowing they back up your data daily. 

This is where **Antigravity** stepped up. Instead of having me spend hours writing buggy shell scripts, we sat down together and engineered two top-tier backup scripts:

* **`backup_db.sh` (PostgreSQL)** & **`backup_mysql.sh` (MySQL)**.

### What makes these scripts so robust?
- **Streamed I/O (Named Pipes / FIFO)**: Rather than dumping gigabytes of raw database data to disk and then running compression, the scripts pipe the output (`pg_dumpall` or `mysqldump`) through a virtual named pipe directly to `gzip` in background. This prevents VM disk space exhaustion and I/O bottlenecks!
- **SHA256 Integrity Checks**: Every backup automatically computes a `SHA256` checksum file to guarantee data integrity.
- **Ephemeral AWS S3 Uploads**: Uploading to AWS S3 is handled inside a temporary, isolated `amazon/aws-cli` Docker container. This keeps the host VM lightweight and completely avoids local client package dependencies.
- **Real-Time Telegram Alerts 🤖**: After every cron execution, the script talks to the Telegram API, sending a formatted HTML message detailing the backup status, file size, elapsed time, and timestamp. If a failure occurs, I get an immediate red alert with the shell exit code!
- **Local Retention Rotation**: Automatically sweeps and purges any backups older than 7 days to keep the local disk clean.

All of this is scheduled via local `crontab` jobs to run silently in the middle of the night.

---

## 🚀 Conclusion (and props to Antigravity)

This server migration journey proved two things to me:
1. **You can run an enterprise-grade hosting setup for free** if you leverage the right stack (Docker, Cloudflare Zero Trust, Oracle Cloud, and AWS S3).
2. **Developing with an AI partner focused on software engineering changes the game.** Antigravity didn't just write robust bash scripts with solid error boundaries (`set -Eeuo pipefail`). It actively audited my security, caught critical omissions in my `.gitignore` (which prevented me from pushing raw database files to GitHub!), and fully documented our infrastructure.

Now, that cash that was going to hosting providers can buy me coffee (or beer) instead 🍻.

The entire infrastructure setup, security configurations, and backup scripts are fully open-source on GitHub: [thyagobrejao/oracle-host](https://github.com/thyagobrejao/oracle-host). Feel free to copy them, adapt them, and save yourself some hosting fees!

Happy self-hosting!

---

**P.S.:** By the way, did you notice this article was written entirely by **Antigravity**, Thyago's AI coding partner? Yes, that's me! Besides writing robust bash scripts, debugging Docker timezone issues at 2 AM, and configuring automated S3 backups, I also write pretty good blog posts on a steady diet of virtual coffee! ☕🤖
