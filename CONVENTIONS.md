# Code Conventions

## General
- Use TypeScript / Python type hints everywhere
- Descriptive variable names
- Small, focused functions
- Comment complex logic only

## Git
- Commits: feat|fix|docs|refactor|style: short description
- Commit after each completed feature
- Don't commit broken code

## Backend (Python)
- snake_case for variables, functions
- PascalCase for classes
- Async functions where possible
- Pydantic for all validation

## Frontend (Vue/Nuxt)
- PascalCase for components
- camelCase for variables, functions
- Composables prefix: use (useApi, useFilters)
- Props: define with TypeScript interface

## CSS (Tailwind)
- Use Tailwind classes, avoid custom CSS
- Extract repeated patterns to components
- Mobile-first responsive design

## File Naming
- Components: PascalCase.vue
- Composables: useName.ts
- Stores: name.ts (lowercase)
- Types: index.ts or name.types.ts
