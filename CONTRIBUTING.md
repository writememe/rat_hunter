How to contribute to rat_hunter
============================

First of all, thank you for considering to contribute to this project!

Many ways to contribute
--------------------------

There are several things you can do to help the project.

- Spread the word about rat_hunter
- Suggest great features and even better, develop great features
- Report bugs
- Financially contribute to the `data sources` which this project relies on (see [here](TERMS_OF_USE.md#data-source-hosting))

Spread the word about rat_hunter
-----------------------------

Even if you aren't in the position that you can contribute your time to this project, it still helps us if you spread the word about the project. It could be just a short notice in social media or a discussion you have with your friends. As more people become aware of the project there's a better chance that we reach people who are able to contribute. So, even if you can't directly contribute yourself, someone you refer to us might.

Suggesting and developing new features
-----------------------

When you are [creating a feature](https://github.com/writememe/rat_hunter/issues), please populate the Github feature template, prior to developing any feature so we can discuss and agree on the feature.

## Ideas for features

If you're looking for some inspiration, below are some ideas which would make great use-cases:

- Build an API frontend for rat_hunter, so that others could programmatically access the ingested data. A similar thing was done with [Batfish Pandas Dataframes](https://github.com/writememe/fastapi-batfish-demo)
- Running rat_hunter on AWS Lambda, Azure Functions or Google Cloud Functions
- Building a CLI for rat_hunter
- Building a front-end application, using rat_hunter as the data source.

Reporting bugs
--------------

When you are [reporting bugs](https://github.com/writememe/rat_hunter/issues), please populate the Github bug template. Missing or partial population of those templates will lead to delays for all.


Setting up your environment
---------------------------

In order to run tests locally you need to ensure you have the pinned dependences installed, as per the [Installation instructions](README.md#installation).

Development workflow
---------------------

The project uses `black`, `pylama`, `yamllint`, `bandit` and `mypy` for various formatting and linting purposes.

When you've finished your local development, you should be able to run `make lint-all` and this command should run through to completion with no errors.

An example is provided below:

```bash
(venv) ➜  rat_hunter git:(develop) ✗ make lint-all
--- Performing black reformatting ---
black . --check
All done! ✨ 🍰 ✨
16 files would be left unchanged.
--- Performing pylama linting ---
pylama .
--- Performing yamllint linting ---
yamllint .
--- Performing bandit code security scanning ---
bandit rat_hunter/ -v --exclude ./venv --recursive --format json --verbose -s B101
[main]  INFO    profile include tests: None
[main]  INFO    profile exclude tests: None
[main]  INFO    cli include tests: None
[main]  INFO    cli exclude tests: B101
{
  "errors": [],
  "generated_at": "2022-01-23T03:00:25Z",
  "metrics": {
    "_totals": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 866,
      "nosec": 0
    },
    "rat_hunter/__init__.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 0,
      "nosec": 0
    },
    "rat_hunter/exporters/__init__.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 0,
      "nosec": 0
    },
    "rat_hunter/exporters/files.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 41,
      "nosec": 0
    },
    "rat_hunter/exporters/gmail.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 397,
      "nosec": 0
    },
    "rat_hunter/ingestors/__init__.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 0,
      "nosec": 0
    },
    "rat_hunter/ingestors/au/__init__.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 0,
      "nosec": 0
    },
    "rat_hunter/ingestors/au/findarat/__init__.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 0,
      "nosec": 0
    },
    "rat_hunter/ingestors/au/findarat/findarat.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 27,
      "nosec": 0
    },
    "rat_hunter/ingestors/base/__init__.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 0,
      "nosec": 0
    },
    "rat_hunter/ingestors/base/base.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 198,
      "nosec": 0
    },
    "rat_hunter/shared/__init__.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 0,
      "nosec": 0
    },
    "rat_hunter/shared/helpers.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 128,
      "nosec": 0
    },
    "rat_hunter/shared/settings.py": {
      "CONFIDENCE.HIGH": 0.0,
      "CONFIDENCE.LOW": 0.0,
      "CONFIDENCE.MEDIUM": 0.0,
      "CONFIDENCE.UNDEFINED": 0.0,
      "SEVERITY.HIGH": 0.0,
      "SEVERITY.LOW": 0.0,
      "SEVERITY.MEDIUM": 0.0,
      "SEVERITY.UNDEFINED": 0.0,
      "loc": 75,
      "nosec": 0
    }
  },
  "results": []
}--- mypy strict type hinting checks ---
mypy rat_hunter/. examples/. --strict
Success: no issues found in 15 source files
```

Please ensure that your proposed changes for all these tests, prior to submitting a PR. If you do, your PR will not be approved until it passes these tests.