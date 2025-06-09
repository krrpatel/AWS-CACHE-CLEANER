# AWS-CACHE-CLEANER

## helps to auto delete cache file when reaches >=29GB to maintain the free tier memory allocation.

```bash
screen -S cachebot
```

```bash
git clone https://github.com/krrpatel/AWS-CACHE-CLEANER.git
```

``` bash
cd AWS-CACHE-CLEANER
```

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install python-telegram-bot schedule
```

```bash
python3 main.py
```
