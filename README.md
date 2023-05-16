# werkzeug-interceptor
Werkzeug-Interceptor allows you to mock specific endpoints based on the HTTP method name, endpoint, and response you define.

## Usage

```bash
http_intercept -p 8000 '[{"methods": ["POST"], "path": "test-endpoint", "response": "Hello"}]'
```

```bash
curl -X POST -H "X-Access-Key: some-random-key" http://localhost:8000/test-endpoint
```

## Development

Manages the dependencies using [Rye](https://github.com/mitsuhiko/rye)
```
cd werkzeug-interceptor
rye sync
```

## License

This project is licensed under the MIT License.