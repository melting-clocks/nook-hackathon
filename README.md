# Nook eval: Elastic vs Original

Built for the Cloud Native Hackathon (Nov 9, 2026). Nook is a shared memory for AI agents. This repo has the eval we used to test a new Elastic retrieval method against Nook's current one, and the dashboard that shows the results.

**Live demo:** open [`docs/index.html`](docs/index.html) (one self-contained file, no server).

## Results (Nov 9, 2026, 40 questions)

| | Original | Elastic |
|---|---|---|
| **Answered correctly** | 15/40 (+10 partial) | **19/40** (+10 partial) |
| Hard 20 | 9 | **12** |
| Hidden 10 | 2 | **6** |
| No shared words (2) | 0 | **2** |
| Exact evidence (7) | 3 | 2 |
| Search found / filter kept / returned (of 37) | 37 / 36 / 34 | 36 / 36 / 36 |
| Avg rank of the right source | #4.9 | #2.1 |
| Typical / slow | 1.6 s / 2.0 s | 1.5 s / 2.0 s |

On the same 20 original questions, Original went from 5/20 (eval 1, regraded with the same judge) to 6/20, and Elastic from 6/20 to 7/20.

**What it means:** retrieval now finds and returns the right source almost every time. Most of the remaining losses happen afterwards, in the excerpt the agent receives. The next fix is to pass the matched passage plus its neighbors.

## About the data

The real eval ran on 65 private company items (30 meeting recordings + 35 decoy notes). Those questions, quotes, contexts and answers are **not** in this repo.

`data/demo/` is a made-up dataset in the same format. It covers a fictional four-person team and has 40 invented questions. Its per-method totals are set to match the real run above, so the dashboard shows the real result, but **the individual questions, notes and answers are invented**. `scripts/make_demo.py` generates it and asserts every total.

## How the eval works

- **Methods:** Original (`cards_decisions_v1`, Nook's current default) and Elastic (`elastic_decisions_v1`). Elastic combines BM25 and kNN (768-dimension cosine) with native RRF on Elastic Serverless. Both run through the same relevance filter and a 1600-token context budget.
- **Questions:** 20 original + 20 hard. The hard types are two meetings, changed our mind, idea vs done, never discussed (correct = "not in memory"), who said it, no shared words, decoy trap, and exact number/quote. 10 questions are held out (`split: "hidden"`) for the final score.
- **Grading** (`grader/grade.mjs`): Claude Sonnet 5.5 answers using *only* the context retrieval returned. Claude Opus 5.5 grades each answer against the key as correct, partial or wrong. Exact evidence (the quote and speaker reached the agent) is checked only on evidence questions.
- **Dashboard steps:** Search found it → Filter kept it → Returned → Answered correctly, plus Exact evidence.

## Run it

```sh
# Rebuild the demo data and dashboard
python3 scripts/make_demo.py
python3 dashboard/build.py data/demo docs/index.html

# Grade a run of your own (needs a Vercel AI Gateway key)
AI_GATEWAY_API_KEY=... node grader/grade.mjs elastic_decisions_v1 data/private
python3 dashboard/build.py data/private out/dashboard.html   # out/ is gitignored; file is chmod 600
```

A data directory holds:

- `questions-v2.json`: `{id, question, kind, gold:[{note_id, must_include[], speaker, time}], answer, hard, evidence, split}`
- `runs/<method>-r1.json`: `{timestamp, cases:[{id, latency_ms, trace_url}]}`
- `runs/<method>-r1-raw.json`: per question, `{evaluation:{question_id}, trace:{runs:[{output, degraded, queries:[{base:{stages}, stages}]}]}, response:{runs:[{result:{context, sources}}]}}`
- `grades/<method>.json`: `{id, agent_answer, verdict, reason, evidence}`
- `history.json`: `{name, date, questions, note, grades_dir, exact_text:{<method>:n}}`, one entry per eval

The runner that produced the real `runs/` files calls Nook's retrieval service and isn't part of this repo.

The dashboard builds every node with `textContent`, never `innerHTML`, so the data can't inject markup.
