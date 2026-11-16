# url-shortener

Base62 URL shortener with JSON persistence.

## Usage

```bash
python3 -c "from shortener import *; s=Shortener(); print(s.shorten('https://example.com'))"
python3 -c "from shortener import *; s=Shortener(); print(s.shorten('https://example.com', alias='my-link'))"
python3 -c "from shortener import *; s=Shortener(); s.shorten('https://example.com'); s.resolve('1'); print(s.stats())"
```

## Features

- Base62 codes generated from a counter
- Custom aliases via Shortener.shorten(url, alias=None)
- URL validation and persistence
- Persisted hit counters with Shortener.stats()
- Delete short codes with Shortener.delete(code)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
