Example Documentation
=======

## Pre-requisites

Prior to proceeding through the examples, please ensure that you have performed the installation
steps for the project found [here](../README.md#installation)

## Installation

In addition to installing those requirements, please ensure you install the additional packages from the base
of the repository:

1. Install the requirements file for the examples:

```python
pip install -r requirements-example.txt
```

## Example Documentation

All examples are well documented, and those with a good knowledge of Python should be able to follow along.

### Using yagmail (gmail example)

In relation to the yagmail example, the `username` and `password` is managed via environmental variables. Your environmental variable must be as follows:

```bash
GMAIL_ACC="email_username"
GMAIL_PWORD="email_password"
```

By default, the example will perform the following:

1) Use the system defined environmental variables.
2) If the system defined environmental variables are not set, it will load what is defined in the `.env` at this location in the repo:

`rat_hunter/backend/creds/.env`

There are many ways with Option 1 to inject environmental variables, and that should be the preferred method. If you choose to use Option 2, please consult the [python-dotenv documentation](https://github.com/theskumar/python-dotenv)

In relation to generating a `username` and `password` for the application, please consult the [yagmail documentation](https://github.com/kootenpv/yagmail). yagmail recommends generating an [Application-Specific Password](https://support.google.com/accounts/answer/185833).


#### Why not Oauth2?

[yagmail supports Oauth2](https://github.com/kootenpv/yagmail#oauth2), so if you feel like adding this capability to this project, feel free to raise an issue, and we can discuss it.
