# Billing Overview

!!! info "Audience"
    Educators and project sponsors who need to understand the recurring costs associated with running the DeVILSona platform.

This page provides a plain-language breakdown of every cost involved in operating DeVILSona. The good news: for a typical semester of classroom use, **the total cost is extremely low** — estimated at no more than $20 per semester.

---

## At a Glance

| Cost Category | Estimated Cost per Semester | Who Pays? |
|---------------|----------------------------|-----------|
| [AWS Cloud Infrastructure](#aws-cloud-infrastructure) | **~$10–20** | AWS account holder |
| [OpenAI API Usage](#openai-api-usage) | **$0** (covered by ASU) | ASU AI Acceleration team |
| [GitHub Team Plan](#github-team-plan) | **$0 – $20/month** (only during active development) | GitHub organization owner |

---

## AWS Cloud Infrastructure

DeVILSona uses a small set of Amazon Web Services (AWS) to power its backend. These services handle student login, saving session data (interview transcripts, scores, etc.), and routing requests from the VR headsets to the cloud.

The infrastructure is defined as code in the [`DeVILSona-infra`](https://github.com/FSE100Capstone/DeVILSona-infra) repository and consists of the following services:

### Services Deployed

| AWS Service | What It Does | Why DeVILSona Needs It |
|-------------|-------------|----------------------|
| **API Gateway** (HTTP API) | Receives incoming web requests from VR headsets | Routes student login and session-save requests to the correct backend function |
| **Lambda** (2 functions) | Runs small pieces of code on-demand | `FSE100_Login` handles student authentication; `FSE100_SaveSession` saves interview data to the database |
| **DynamoDB** (1 table) | Stores structured data in a database | Stores all student session records (interview transcripts, scores, timestamps) |
| **Route 53** (1 hosted zone) | Manages the custom domain name | Provides the `api.devilsona.click` address so headsets can find the backend |
| **ACM** (1 certificate) | Provides an SSL/TLS security certificate | Encrypts all data sent between headsets and the backend (the "https" in the URL) |
| **IAM** | Manages permissions between services | Ensures Lambda functions can access DynamoDB securely (no direct cost) |

### Usage Estimate for a Typical Semester

The estimate below assumes **4 class sessions per semester** (one session per FSE100 class), with approximately **10 teams per class** and **4 students per team**, resulting in roughly **160 total student interactions** per semester. Each interaction generates approximately 2 API requests (1 login + 1 session save).

!!! note "What Is an API Request?"
    Every time a student logs in or their interview session is saved, that counts as one "request" — a small message sent from the VR headset to the cloud. With 160 students each making about 2 requests, that's roughly **320 total requests per semester**. This is an extremely low volume.

#### Per-Service Cost Breakdown

| AWS Service | Pricing Model | Semester Usage | Estimated Cost |
|-------------|--------------|----------------|---------------|
| **API Gateway** | $1.00 per million requests | ~320 requests | **< $1.00** |
| **Lambda** | $0.20 per million requests + compute time | ~320 invocations | **< $1.00** |
| **DynamoDB** | $1.25 per million writes / $0.25 per million reads | ~160 writes, ~160 reads | **< $1.00** |
| **Route 53** | $0.50 per hosted zone per month + DNS query fees | 1 zone × ~5 months | **~$3–5** |
| **ACM Certificate** | Free (when used with API Gateway) | 1 certificate | **$0.00** |
| **IAM** | Always free | — | **$0.00** |
| **Domain Registration** | $3/year (`.click` TLD) | Annual renewal | **$3.00/year** |

#### Estimated Total AWS Cost

!!! success "Bottom Line"
    **Estimated total AWS cost: no more than ~$20 per semester.**

    The majority of this cost comes from the Route 53 hosted zone fee ($0.50/month), DNS query charges, and the annual domain name renewal. The usage-based charges (API Gateway, Lambda, DynamoDB) are minimal at this volume but are budgeted with a conservative buffer to account for testing, retries, or unexpected usage spikes.

!!! tip "AWS Free Tier"
    If the AWS account is less than 12 months old, many of these services include a generous free tier (e.g., 1 million free Lambda requests/month, 1 million free API Gateway requests/month, 25 GB of free DynamoDB storage). During the free tier period, the only cost would be Route 53 and domain registration.

### Official AWS Pricing References

For the most current pricing, refer to the official AWS pricing pages:

- [API Gateway Pricing](https://aws.amazon.com/api-gateway/pricing/)
- [Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
- [DynamoDB Pricing](https://aws.amazon.com/dynamodb/pricing/)
- [Route 53 Pricing](https://aws.amazon.com/route53/pricing/)
- [ACM Pricing](https://aws.amazon.com/certificate-manager/pricing/)
- [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/)

---

## OpenAI API Usage

DeVILSona uses OpenAI's GPT APIs to power the real-time AI conversations that students have with the virtual characters during interview scenarios.

!!! success "This costs $0 for DeVILSona."
    The project uses OpenAI APIs through **ASU's enterprise OpenAI platform account**, which is managed and funded by **ASU's AI Acceleration team**. There is no direct charge to the project, the educator, or the students for API usage.

The API keys used by DeVILSona were granted by **Gil Speyer** from the ASU AI Acceleration team.

!!! note "Questions or Concerns?"
    If you have any questions about the OpenAI API access, billing, or usage limits, please contact:

    **Gil Speyer** — [speyer@asu.edu](mailto:speyer@asu.edu)

---

## GitHub Team Plan

GitHub offers a **Team** plan at **$4 per user per month** that provides features useful for collaborative software development (such as required code reviews, branch protection rules, and advanced access controls).

!!! warning "Only Relevant During Active Development"
    The GitHub Team plan cost **only applies if a capstone development team is actively working on the DeVILSona codebase**. If no team is currently developing the project, this cost is **not required**.

    The DeVILSona repositories can remain accessible on GitHub's free plan. The free plan supports unlimited public and private repositories, so all project code, documentation, and history will remain available at no cost even without an active Team subscription.

**When a team is actively developing:**

| Item | Cost |
|------|------|
| GitHub Team plan | $4/user/month |
| Typical capstone team (5 members) | **~$20/month** |
| Per semester (~5 months) | **~$100/semester** |

**When no team is working on the project:**

| Item | Cost |
|------|------|
| GitHub Free plan | **$0** |

---

## Summary

| Category | When It Applies | Estimated Semester Cost |
|----------|----------------|------------------------|
| **AWS Infrastructure** | Always (while backend is running) | **~$10–20** |
| **OpenAI API** | Always (covered by ASU) | **$0** |
| **GitHub Team** | Only during active capstone development | **$0 – $100** |
| | | |
| **Total (classroom use only, no dev team)** | | **~$10–20/semester** |
| **Total (with active dev team)** | | **~$110–120/semester** |
