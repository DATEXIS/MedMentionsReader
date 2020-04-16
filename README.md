# MedMentionsReader

## About

This module parses the [MedMentions](https://github.com/chanzuckerberg/MedMentions) dataset.

## Usage

### Preparing the Dataset

The dataset needs to be unzipped after cloning.

```bash
git clone https://github.com/chanzuckerberg/MedMentions.git
gunzip MedMentions/full/data/corpus_pubtator.txt.gz
```

### API Examples

```python3
from medmentionsreader.MedMentionsReader import MedMentionsReader
mmr = MedMentionsReader('../MedMentions/full/data')
mmr.get_train()
mmr.get_test()
mmr.get_dev()
mmr.get_all()
```
