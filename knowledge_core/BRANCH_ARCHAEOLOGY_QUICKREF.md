# Branch Archaeology Quick Reference

**For Agents:** Fast access to repository development history

## What Is This?

A semantic knowledge graph documenting **260 repository branches**, their relationships, status, and development themes. Think of it as the repository's "fossil record" - preserving institutional memory of what was tried, what succeeded, and what failed.

## Quick Access

### Machine-Readable (Query These)

```python
# JSON-LD
import json
with open('knowledge_core/branch_archaeology.jsonld') as f:
    kg = json.load(f)

# YAML-LD  
import yaml
with open('knowledge_core/branch_archaeology.yaml') as f:
    kg = yaml.safe_load(f)

# RDF/Turtle (SPARQL)
# Load into RDF store for semantic queries
```

### Human-Readable (Read These)

- **Full Documentation**: `docs/BRANCH_ARCHAEOLOGY.md`
- **Anomaly Investigation**: `docs/BRANCH_ANOMALIES.md`
- **Metadata**: `knowledge_core/branch_archaeology_meta.yaml`

## Common Queries

### "What work has been done on X?"

```python
# Find branches related to protocols
protocol_branches = [b for b in kg['branches'] 
                     if 'protocol' in b['tags']]

# Find branches with 'refactor' in name
refactor_branches = [b for b in kg['branches'] 
                     if 'refactor' in b['name'].lower()]
```

### "What are the prerequisites for Y?"

```python
# Find version series
for rel in kg['relationships']:
    if rel['type'] == 'supersedes':
        print(f"{rel['source']} supersedes {rel['target']}")

# Find thematic relationships
theme_branches = [rel for rel in kg['relationships']
                  if rel['type'] == 'thematic_group' 
                  and rel['target'] == 'chc']
```

### "What failed attempts exist?"

```python
# Find stalled branches
stalled = [b for b in kg['branches'] 
           if b['status'] == 'stalled']

# Find experimental branches
experimental = [b for b in kg['branches']
                if b['status'] == 'experimental']
```

## Data Structure

### Branch Object

```json
{
  "name": "feat-chc-protocol-framework",
  "commit_hash": "99cbce7bff...",
  "status": "experimental",
  "tags": ["feature", "core", "chc"],
  "purpose": "feat: Introduce CHC Protocol Framework",
  "author_date": "2025-10-31 08:49:33 +0000"
}
```

### Relationship Object

```json
{
  "type": "supersedes",
  "source": "feat-aorp-v3-integration",
  "target": "feat-aorp-v2-integration",
  "explanation": "Version progression in feat-aorp series"
}
```

## Status Values

- `active`: Recent work (< 30 days)
- `inactive`: Dormant (30-90 days)
- `stalled`: Long-dormant (> 90 days)
- `experimental`: Explicitly experimental
- `archived`: Completed/abandoned
- `automated`: Bot-created

## Relationship Types

- `converges_to`: Same commit
- `supersedes`: Version progression
- `thematic_group`: Part of theme

## Statistics (as of generation)

- **Total Branches**: 260
- **Stalled**: 185 (71.2%)
- **Experimental**: 70 (26.9%)
- **Most Common Theme**: addition (85 branches)
- **Relationships**: 134

## Integration Points

Cross-reference with:
- `integrated_knowledge.json` - System knowledge
- `symbols.json` - Code entities
- `dependency_graph.json` - Architecture
- `lessons.jsonl` - Learned lessons
- `plan_registry.json` - Execution plans

## Regeneration

```bash
# Regenerate all branch archaeology data
python3 tooling/branch_archaeologist.py

# Custom output location
python3 tooling/branch_archaeologist.py --output-dir /path/to/output
```

## Use Cases by Agent Phase

### L1 Self-Awareness
- Not typically needed

### L2 Repository Sync
- **Load branch archaeology** to understand development history
- Identify recently active branches
- Note experimental areas

### L3 Environmental Probing
- Query specific feature branches
- Check for prior work on current task
- Identify failed attempts to avoid

### L4 Deep Research
- **Primary resource** for understanding repository evolution
- Trace feature development through version series
- Analyze patterns in stalled branches

## Pro Tips

1. **Always check stalled branches first** - Learn from past failures
2. **Look for version series** - Understand evolution of features
3. **Cross-reference with lessons.jsonl** - Link attempts to learnings
4. **Use thematic queries** - Find all work on a topic quickly
5. **Check convergences** - Understand branching strategies

## SPARQL Example

```sparql
PREFIX git: <http://metavacua.io/ontology/git#>
PREFIX schema: <http://schema.org/>

SELECT ?branch ?status ?tags
WHERE {
  ?branch a git:Branch ;
          schema:name ?name ;
          git:status ?status ;
          schema:keywords ?tags .
  FILTER(?status = "experimental")
  FILTER(CONTAINS(?name, "chc"))
}
```

## Questions?

See full documentation at `docs/BRANCH_ARCHAEOLOGY.md`
