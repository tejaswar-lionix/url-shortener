# url-shortener

Base62 URL shortener with JSON persistence.

## Usage

```bash
python3 -c "from shortener import *; s=Shortener(); print(s.shorten('https://example.com'))"
```

## Features

- Base62 codes generated from a counter
- URL validation and persistence
- Delete short codes with Shortener.delete(code)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
