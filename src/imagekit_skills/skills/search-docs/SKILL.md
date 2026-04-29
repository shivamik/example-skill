---
name: search-docs
description: >
  Search ImageKit documentation to find guides, API references, and examples.
  Use when the user asks about ImageKit features, APIs, SDKs, transformations,
  configuration, or troubleshooting. Also use when the user needs to look up
  specific parameters, supported formats, or integration guides.
---

# Documentation Search Skill

## When to use
- User asks about ImageKit features, capabilities, or services
- Transformation builder fails and you need parameter/limit info
- User asks about APIs, configuration, pricing, or DAM features
- Need to verify if ImageKit supports a specific feature

## Using search_docs tool

**Required**: `query` - Clear, specific question about ImageKit

**Optional**: `sources` array (default: `["imagekit_guides", "imagekit_community"]`)
- `imagekit_guides`: Official guides and tutorials
- `imagekit_community`: User-generated content, practical solutions
- `imagekit_api_references`: Technical API details
- `imagekit_sdk`: SDK implementation examples

## Source Selection

| Use Case | Sources |
|----------|---------|
| General features | `["imagekit_guides", "imagekit_community"]` |
| API details | `["imagekit_guides", "imagekit_api_references"]` |
| SDK examples | `["imagekit_sdk", "imagekit_guides"]` |
| Troubleshooting | `["imagekit_community", "imagekit_guides"]` |

## Handling Results

Always cite sources:
```
References:
1. [Title]: [URL]
```

If results don't answer the question, acknowledge the limitation and suggest contacting ImageKit support.

## Gotchas

- Specific queries yield better results ("How to apply background removal using API" not "tell me about ImageKit")
- Multiple searches may be needed; refine query if first search is insufficient
- Community sources provide real-world solutions; official guides are authoritative
