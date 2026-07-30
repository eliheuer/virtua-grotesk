# Google Fonts Workflow Porting Checklist

Retired. The canonical checklist is
[`.agents/google-fonts-onboarding-checklists.md`](.agents/google-fonts-onboarding-checklists.md),
which also carries the portable-token table used by the
`.agents/skills/google-fonts-*` skills when copying this workflow to another
font repo.

Two rulings that supersede older wording that lived in this file:

- Fontspector (`make qa`) is the QA tool; fontbakery is retired.
- The release bar is the honest warning floor — a zero-noise gate achieved by
  documented, owned, temporary exclusions, never by hiding intended scope.

The final local gate before any submission pass:

```bash
make clean && make setup && make build && make proof && make reports \
  && make preflight && make test
```
