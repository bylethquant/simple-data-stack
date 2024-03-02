# A Practical Guide to a Simple Data Stack

This GitHub repository hosts the source code for my infrastructure
series, [A Practical Guide to a Simple Data Stack](https://hiddenorder.io). It expands
upon the Substack posts and provides a step-by-step guide to building the data infrastructure depicted in the figure
below.

## Introduction

The series is inspired by recent discussions in my crypto quant circle about leveraging modern applications like
[Grafana](https://grafana.com) for a budget-friendly solo data infrastructure. But what is the simplest way to gain
exposure and
utilize these applications? Today, [Docker](https://www.docker.com) stands out as an excellent tool for experimenting
with these applications. For
instance, [Grafana](https://grafana.com) can be run locally with just a few lines of code. This series aims to equip
everyone with the
knowledge necessary to deploy tools such as
[Grafana](https://grafana.com), [Timescale](https://www.timescale.com), [Apache Airflow](https://airflow.apache.org),
and [Traefik](https://traefik.io/traefik) for local development.

## Overview

Let's start with the outcome: In the substack posts, I provided a guide to building step by step the data stack as
illustrated in the figure below:

<div align="center">
    <img src=".github/data-infra.webp" alt="data-infra" width="500" />
</div>

*Orchestration* is managed using Apache Airflow, which facilitates the implementation and management of data pipelines.
As a practical example, I will develop Extract-Transform-Load (ETL) pipelines to process 1-minute candlestick data,
including spot and future price data as well as funding rates from Binance. *Data Storage* will be handled by
Timescale. *Visualization* will be provided by Grafana, with Docker as the main hosting tool and Traefik serving as
the reverse proxy. Following local development, I will showcase how to deploy this infrastructure on a cloud service
provider. A domain will be registered through [Porkbun](https://porkbun.com/), with DNS records set up to enable access
to Docker containers via
subdomains such as airflow.mydomain.com and grafana.mydomain.com.

Additionally, while Binance data ingestion pipelines serve as the primary example, the infrastructure is designed with
flexibility in mind. It can accommodate pipelines for processing log files or any other data sources.

In what follows, I aim to keep everything straightforward so that anyone can adopt elements of this data stack
 for their own data infrastructure. This repository provides the source code for each post.

## Structure

1. Introduction to Docker, Docker Compose, and Setting Up Timescale
2. Setting up Apache Airflow and Creating Pipelines

## Tools

* Docker Desktop 4.27.2
* Python 3.11.5
* Airflow 2.8.1
* Grafana 10.0.2
* Timescale pg15
* Traefik 3.0
