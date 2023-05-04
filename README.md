# ACLTLDR

This is a python-based CLI tool used to generate summaries for ACL conference papers on [this page](https://sotaro.io/tldrs).


## Installation

```
pip install acltldr
```


## Usage

An example command to generate summaries for the proceedings of EACL 2021.
Following command will generate a jsonl file with all the data, and a markdown file for the post.

```
acltldr https://raw.githubusercontent.com/acl-org/acl-anthology/master/data/xml/2021.eacl.xml \
        ./ \
	--prefix "2021.eacl" \
	--use-gpu
```
