# werkzeug-interceptor
How often do you find yourself writing flask apps just to mock that one third party HTTP endpoint? Well, this solves it.


# Usage

```bash
http_intercept -p 8000 '[{"methods": ["POST"], "path": "test-endpoint", "response": "Hello"}]'
```

```bash
curl -X POST -H "X-Access-Key: some-random-key" http://localhost:8000/test-endpoint
```
