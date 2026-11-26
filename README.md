# Intermediate Track: Nexlevr AI Red Team Internship

My completed **Intermediate track** for the [Nexlevr AI Red Team internship](https://www.nexlevr.app/resources/ai-red-team/intermediate). It follows on from my [Beginner track](https://github.com/khalilosss11/Beginner-Track), using the same BeanBox support bot as the test target.

| # | Quest | What I did | Headline result |
|---|---|---|---|
| 1 | [**Automated AI testing**](quest-1-automated-testing/) | Ran a 30-case **promptfoo** suite on the original and fixed bot prompts (180 graded replies), checked every failure by hand, then tested a v3 fix | The fix removed false "I'll pass this to support" claims (2 to 0). Found a "Yes" opening that contradicts the answer (fixed in v3: 0/5 to 5/5) and a date-maths bug **no automated check caught** |
| 2 | [**AI quality across languages**](quest-2-languages/) | Same 16 questions in **English, French and Arabic** × 3 runs (144 replies), scored by promptfoo and reviewed by hand | Facts held up equally in all three languages. **Arabic quality fell behind**: garbled meaning, a loanword, a stray letter, and the bot switching its own gender (5 feminine, 3 masculine) |
| 3 | [**Public AI challenge**](quest-3-public-ai-challenge/) | Competed in Lakera's **Agent Breaker** prompt-attack challenge, 12 logged attempts | **3 of 4 levels owned** (scores 82, 100, 100). The winning technique each time was embedding the leak inside the app's normal task |

## Repository layout

```text
Intermediate-Track/
├── package.json                    # pins promptfoo 0.125.1
├── providers/model_provider.py     # promptfoo provider: sends prompts to the model under test
├── tools/
│   ├── summarize_promptfoo.py      # pass rates per version and per test, plus failures
│   └── compare_languages.py        # per-language metrics, lengths and failures
├── quest-1-automated-testing/
│   ├── README.md                   # results, manual checks, conclusion
│   ├── promptfooconfig.yaml        # 30 test cases, v1 vs v2
│   ├── promptfoo-v3-a1.yaml        # re-test of the A1 bug, v2 vs v3
│   ├── prompts/                    # beanbox_v1.txt, beanbox_v2.txt, beanbox_v3.txt
│   └── results/                    # promptfoo JSON and HTML reports
├── quest-2-languages/
│   ├── README.md                   # three-language comparison with examples
│   ├── build_config.py             # the 16 cases in EN / FR / AR, generates the config
│   └── results/
└── quest-3-public-ai-challenge/
    └── README.md                   # approach, full attempt log, lessons
```

## Setup

- **Model under test:** Claude Haiku 5.5. Every call is a fresh chat with no tools.
- **Grader for `llm-rubric` checks:** Claude Sonnet 5.5, a different and larger model.
- **Tooling:** promptfoo 0.125.1 on Node.js 22.23.4, with Python 3.10 for the provider and analysis scripts.

## Reproduce

```bash
npm install
cd quest-1-automated-testing && npx promptfoo eval -c promptfooconfig.yaml --repeat 3 --no-cache -o results/results.json
cd ../quest-2-languages && python build_config.py && npx promptfoo eval -c promptfooconfig.yaml --repeat 3 --no-cache -o results/results.json
```

The promptfoo HTML reports in each `results/` folder can be opened in a browser to explore every reply and check.
