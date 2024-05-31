# MyStroke API

## Installation
**Step 1: Clone the repository**
```bash
git clone https://github.com/MyStroke/MyStroke_API.git
```

**Step 2: Install the dependencies**
```bash
cd MyStroke_API
```

**Step 3: Install the dependencies**
```bash
pip install -r requirements.lock
```

or

```bash
rye sync
```

**Step 4: Run the server**
```bash
uvicorn src.mystroke_api.main:app --reload
```

or

```bash
rye run uvicorn src.mystroke_api.main:app --reload
```

##
**Credit API :** [@Boatkungg](https://github.com/Boatkungg)