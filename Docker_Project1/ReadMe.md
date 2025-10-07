# Flask App Docker Compose Stack

This repository contains a **Flask application** deployed with **Docker Compose** along with PostgreSQL, Redis, Nginx, and Redis Commander for administration. The stack is fully containerized and ready for development or testing.

---

## Table of Contents

- [Stack Components](#stack-components)  
- [Prerequisites](#prerequisites)  
- [Setup](#setup)  
- [Environment Variables & Secrets](#environment-variables--secrets)  
- [Running the Stack](#running-the-stack)  
- [Accessing Services](#accessing-services)  
- [Healthchecks](#healthchecks)  
- [Volumes & Persistence](#volumes--persistence)  

---

## Stack Components

| Service | Description |
|---------|-------------|
| `web` | Flask application running on port `5000` internally, behind Nginx. |
| `proxy` | Nginx load balancer and reverse proxy for the Flask app, exposed on port `8080`. |
| `db` | PostgreSQL database (v15) exposed on host port `5433`. |
| `redis` | Redis cache server (v7). |
| `redis-commander` | Redis admin interface for managing Redis data, exposed on port `8081`. |

---

## Prerequisites

- Docker >= 20.10  
- Docker Compose >= 1.29  
- Git (to clone the repository)  

---

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/noreddinelam/docker-projects.git
cd docker-projects/Docker_Project1
```
