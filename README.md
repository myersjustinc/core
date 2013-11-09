# core


Core repo for election results data acquisition, transformation and output.

## Getting started as a developer


Create a sandboxed development environment using [virtualenv](http://www.virtualenv.org/en/latest/).
Below is based on plain vanilla virtualenv, but you can make your world a much happier place
by using the most excellent [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/).

```bash
# cd to your virtualenv home
cd ~/.virtualenvs
$ virtualenv openelex-core
```

Jump in and activate your virtualenv.
```bash
$ cd openelex-core
$ . bin/activate

```

NOTE: To deactivate your environment:
```bash
$ deactivate
```

[Fork](https://help.github.com/articles/fork-a-repo) and clone the openelex *core.git* repo on Github
to wherever you stash your code.
```bash
$ mkdir src/
$ cd src/
$ git clone git@github.com:<my_github_user>/core.git openelex-core
$ cd openelex-core 
```

Install the python dependencies.
**Perform below commands while inside an active virtual environment.**
```bash
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

Add the ``openelex`` package to your PYTHONPATH.
```bash
$ export PYTHONPATH=$PYTHONPATH:`pwd`
```

Create ``settings.py`` from the template.
```bash
$ cp settings.py.tmplt openelex/settings.py
```

### Optional


Edit *settings.py* if you plan to archive raw results on your own S3 account
and/or plan to write data loaders for [mongo](http://docs.mongodb.org/manual/installation/).
```bash
$ vim openelex/settings.py
```
