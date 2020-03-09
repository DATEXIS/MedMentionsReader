# MedMentionsReader

## About

This module parses the [MedMentions](https://github.com/chanzuckerberg/MedMentions) dataset.

## Usage

```python3
from medmentionsreader.MedMentionsReader import MedMentionsReader
mmr = MedMentionsReader('../MedMentions/full/data')
mmr.get_train()
mmr.get_test()
mmr.get_dev()
mmr.get_all()
```
