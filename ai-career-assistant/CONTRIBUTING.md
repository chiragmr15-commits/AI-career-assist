# CONTRIBUTING.md

## Contributing to AI Career Assistant

Thank you for interest in contributing! Please follow these guidelines.

### Code Style

#### Python (Backend)
- Follow PEP 8
- Use type hints
- Max line length: 100
- Use Black for formatting

```python
def analyze_resume(file_path: str) -> Dict[str, Any]:
    """Analyze resume and return results."""
    pass
```

#### JavaScript (Frontend)
- Use ES6+
- Use Prettier for formatting
- Follow React best practices

```jsx
const Component = ({ data }) => {
  const [state, setState] = React.useState(null);
  return <div>{state}</div>;
};
```

### Commit Messages

Follow conventional commits:

```
type(scope): subject

feat(resume): add PDF parsing
fix(auth): correct token refresh logic
docs(readme): update installation guide
```

Types: feat, fix, docs, style, refactor, test, chore

### Pull Request Process

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Testing

#### Backend
```bash
python manage.py test
```

#### Frontend
```bash
npm test
```

### Performance Guidelines

- Frontend bundle < 500KB gzipped
- API response time < 200ms
- Database queries < 100ms

### Documentation

- Update README.md for new features
- Add docstrings to functions
- Update API documentation
- Include examples

### Issues

- Use provided templates
- Provide minimal reproducible example
- Include environment details
- Add screenshots if applicable

Thank you for contributing!
