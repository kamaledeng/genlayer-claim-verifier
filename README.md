# GenLayer Claim Verifier

A reusable GenLayer Intelligent Contract for verifying factual claims against external web evidence.

## Overview

Claim Verifier accepts a claim and a source URL, retrieves the source content, and evaluates whether the evidence supports the claim.

The contract stores:

- the submitted claim
- the source URL
- the final verdict
- the explanation produced from the evidence

## How It Works

1. A user submits a claim and source URL.
2. The leader retrieves the source using GenLayer web access.
3. The leader evaluates the evidence and returns a structured verdict.
4. Validators independently evaluate the same source.
5. The validator compares the verification decision with the leader result.
6. GenLayer consensus determines whether the transaction is accepted.
7. The final verification result is stored in contract state.

## Consensus

The contract uses GenLayer's non-deterministic execution and validator mechanism because web content and language-model evaluation are not deterministic blockchain operations.

Validators independently inspect the source instead of only checking the output format.

The verification decision is:

- `supported`
- `not_supported`

## Example Tests

### Supported claim

Claim:

`GenLayer is an AI-powered blockchain.`

Source:

`https://genlayer.com/`

Result:

`supported`

### Unsupported claim

Claim:

`GenLayer is a centralized blockchain controlled by a single server.`

Source:

`https://genlayer.com/`

Result:

`not_supported`

Both verification transactions were finalized through full consensus in GenLayer Studio.

## Contract State

The contract stores:

```text
claim
source_url
verdict
explanation
