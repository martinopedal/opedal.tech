---
title: "Why I Build with GitHub Copilot on Every Project"
description: "A look at how multi-agent AI workflows change the way solo architects ship production code — and the review practices that keep it honest."
pubDate: 2025-05-01
tags: ["GitHub Copilot", "AI", "DevOps"]
---

Over the last year, GitHub Copilot has moved from autocomplete curiosity to the primary author of most of the code I ship. I steer the architecture, write the prompts, and review every line. The agent writes the implementation.

Here's what that actually looks like in practice, and why I think it's the right model for a solo architect maintaining a lot of infrastructure code.

## The problem with solo maintenance

When you're the only reviewer for your own code, the bottleneck isn't writing — it's context switching. You write something on Monday, and by Thursday you've forgotten why you made that trade-off. Review cycles collapse into "looks fine to me" when you're reviewing your own work.

AI-assisted development doesn't solve this problem by itself. In fact, naive use makes it worse: you can generate more code than you can review, accumulating technical debt faster than ever.

## What actually works: multi-agent review patterns

The approach I've settled on is treating GitHub Copilot as a **team member**, not a code generator. Concretely:

1. **Issue-first**: I write a detailed issue with acceptance criteria before any code is generated.
2. **Agent creates a PR**: Copilot Coding Agent opens a pull request against the issue.
3. **Copilot PR reviewer reviews it**: A second agent run reviews the PR with a different prompt focused on security and correctness.
4. **I do the final merge review**: I only see code that has already passed two automated reviews.

This three-pass model means I spend my review time on things only a human can catch: business logic correctness, architectural coherence, and things the reviewers were not prompted to look for.

## The governance layer matters

The other thing that makes this work is keeping the AI's behaviour documented and auditable. I maintain an `AI_GOVERNANCE.md` file in every repo that records:

- Which AI tools are in use
- What they are and aren't authorised to do
- What the human review expectations are

This isn't bureaucracy — it's the same thing we do with any other external contributor. If a third-party library can't modify production secrets, neither can an AI agent.

## What I've shipped this way

In the last six months, using this pattern across multiple engagements:

- The `azure-analyzer` tool (azqr + PSRule + AzGovViz bundled into a single runner)
- The `alz-graph-queries` library (135 ARG queries for the ALZ checklist)
- Multiple Terraform modules for AKS and GitHub runners
- This website

None of these would have been shipped without AI assistance — not because they're too hard, but because I simply don't have the time to write every line solo. The AI handles the mechanical translation from intent to code. I handle the architecture and the review.

## The review discipline is the product

The thing I keep coming back to is this: **the quality of AI-generated code is a function of the quality of your review process**, not the quality of the model.

A great model with a weak review process produces confident-looking code with subtle bugs. A mediocre model with rigorous review produces maintainable code you can trust.

The investment I've made isn't in finding the best model — it's in building the review muscle. Prompt engineering is just structured thinking. Code review is still code review.

If you're building infrastructure with AI, I'd start there.
