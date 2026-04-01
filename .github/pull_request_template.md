## Summary
<!-- What does this PR implement? Link to issue: Closes #XX -->

**Task:** 
**Service:** 
**Spec:** docs/modules/XX-name.md

---

## Changes
<!-- List what was built -->
- 
- 

---

## Test Checklist
<!-- All boxes must be checked before merging to develop -->

### Unit Tests
- [ ] Written in `{service}/tests/test_{task}.py`
- [ ] 80%+ coverage on new code
- [ ] All edge cases covered (invalid input, unauthorized, not found)

### Integration Tests
- [ ] All API endpoints tested with real DB
- [ ] Request/response contracts verified
- [ ] Auth & permissions tested

### Manual Verification
- [ ] FastAPI `/docs` shows all new endpoints
- [ ] No regressions in existing tests (`pytest -x`)
- [ ] `flake8` and `black --check` pass

---

## Deployment
- [ ] Runs on dev after merge to `develop`
- [ ] Migrations safe (no breaking schema changes)
- [ ] Environment variables documented in `.env.example`

---

## Merge Path
```
feature/{task} → develop → staging → main
```
