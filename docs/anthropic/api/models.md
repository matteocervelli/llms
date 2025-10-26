Agent Skills are now available! [Learn more about extending Claude's capabilities with Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview).
[Claude Docs home page![light logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/light.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=c877c45432515ee69194cb19e9f983a2)![dark logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/dark.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=f5bb877be0cb3cba86cf6d7c88185216)](https://docs.claude.com/)
![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)
English
Search...
⌘K
  * [Support](https://support.claude.com/)


Search...
Navigation
Models
Get a Model
[Home](https://docs.claude.com/en/home)[Developer Guide](https://docs.claude.com/en/docs/intro)[API Reference](https://docs.claude.com/en/api/overview)[Claude Code](https://docs.claude.com/en/docs/claude-code/overview)[Model Context Protocol (MCP)](https://docs.claude.com/en/docs/mcp)[Resources](https://docs.claude.com/en/resources/overview)[Release Notes](https://docs.claude.com/en/release-notes/overview)
##### Using the API
  * [Overview](https://docs.claude.com/en/api/overview)
  * [Client SDKs](https://docs.claude.com/en/api/client-sdks)
  * [Beta headers](https://docs.claude.com/en/api/beta-headers)
  * [Errors](https://docs.claude.com/en/api/errors)


##### Messages
  * [POSTMessages](https://docs.claude.com/en/api/messages)
  * [POSTCount Message tokens](https://docs.claude.com/en/api/messages-count-tokens)
  * [Messages examples](https://docs.claude.com/en/api/messages-examples)


##### Models
  * [GETList Models](https://docs.claude.com/en/api/models-list)
  * [GETGet a Model](https://docs.claude.com/en/api/models)


##### Message Batches
  * [POSTCreate a Message Batch](https://docs.claude.com/en/api/creating-message-batches)
  * [GETRetrieve a Message Batch](https://docs.claude.com/en/api/retrieving-message-batches)
  * [GETRetrieve Message Batch Results](https://docs.claude.com/en/api/retrieving-message-batch-results)
  * [GETList Message Batches](https://docs.claude.com/en/api/listing-message-batches)
  * [POSTCancel a Message Batch](https://docs.claude.com/en/api/canceling-message-batches)
  * [DELDelete a Message Batch](https://docs.claude.com/en/api/deleting-message-batches)
  * [Message Batches examples](https://docs.claude.com/en/api/messages-batch-examples)


##### Files
  * [POSTCreate a File](https://docs.claude.com/en/api/files-create)
  * [GETList Files](https://docs.claude.com/en/api/files-list)
  * [GETGet File Metadata](https://docs.claude.com/en/api/files-metadata)
  * [GETDownload a File](https://docs.claude.com/en/api/files-content)
  * [DELDelete a File](https://docs.claude.com/en/api/files-delete)


##### Skills
  * [Using Skills](https://docs.claude.com/en/api/skills-guide)
  * Skill Management
  * Skill Versions


##### Admin API
  * [Admin API overview](https://docs.claude.com/en/api/administration-api)
  * [Usage and Cost API](https://docs.claude.com/en/api/usage-cost-api)
  * [Claude Code Analytics API](https://docs.claude.com/en/api/claude-code-analytics-api)
  * Organization Info
  * Organization Member Management
  * Organization Invites
  * Workspace Management
  * Workspace Member Management
  * API Keys
  * Usage and Cost


##### Experimental APIs
  * Prompt tools


##### Text Completions (Legacy)
  * [Migrating from Text Completions](https://docs.claude.com/en/api/migrating-from-text-completions-to-messages)


##### Support & configuration
  * [Rate limits](https://docs.claude.com/en/api/rate-limits)
  * [Service tiers](https://docs.claude.com/en/api/service-tiers)
  * [Versions](https://docs.claude.com/en/api/versioning)
  * [IP addresses](https://docs.claude.com/en/api/ip-addresses)
  * [Supported regions](https://docs.claude.com/en/api/supported-regions)
  * [OpenAI SDK compatibility](https://docs.claude.com/en/api/openai-sdk)


cURL
cURL
Copy
```
curl https://api.anthropic.com/v1/models/claude-sonnet-4-20250514 \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01"
```

200
4XX
Copy
```
{
  "created_at": "2025-02-19T00:00:00Z",
  "display_name": "Claude Sonnet 4",
  "id": "claude-sonnet-4-20250514",
  "type": "model"
}
```

Models
# Get a Model
Copy page
Get a specific model.
The Models API response can be used to determine information about a specific model or resolve a model alias to a model ID.
Copy page
GET
/
v1
/
models
/
{model_id}
cURL
cURL
Copy
```
curl https://api.anthropic.com/v1/models/claude-sonnet-4-20250514 \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01"
```

200
4XX
Copy
```
{
  "created_at": "2025-02-19T00:00:00Z",
  "display_name": "Claude Sonnet 4",
  "id": "claude-sonnet-4-20250514",
  "type": "model"
}
```

#### Headers
[​](https://docs.claude.com/en/api/models#parameter-anthropic-version)
anthropic-version
string
required
The version of the Claude API you want to use.
Read more about versioning and our version history [here](https://docs.claude.com/en/api/versioning).
[​](https://docs.claude.com/en/api/models#parameter-x-api-key)
x-api-key
string
required
Your unique API key for authentication.
This key is required in the header of all API requests, to authenticate your account and access Anthropic's services. Get your API key through the 
[​](https://docs.claude.com/en/api/models#parameter-anthropic-beta)
anthropic-beta
string[]
Optional header to specify the beta version(s) you want to use.
To use multiple betas, use a comma separated list like `beta1,beta2` or specify the header multiple times for each beta.
#### Path Parameters
[​](https://docs.claude.com/en/api/models#parameter-model-id)
model_id
string
required
Model identifier or alias.
#### Response
200
application/json
Successful Response
[​](https://docs.claude.com/en/api/models#response-created-at)
created_at
string<date-time>
required
RFC 3339 datetime string representing the time at which the model was released. May be set to an epoch value if the release date is unknown.
Examples:
`"2025-02-19T00:00:00Z"`
[​](https://docs.claude.com/en/api/models#response-display-name)
display_name
string
required
A human-readable name for the model.
Examples:
`"Claude Sonnet 4"`
[​](https://docs.claude.com/en/api/models#response-id)
id
string
required
Unique model identifier.
Examples:
`"claude-sonnet-4-20250514"`
[​](https://docs.claude.com/en/api/models#response-type)
type
enum<string>
default:model
required
Object type.
For Models, this is always `"model"`.
Available options: Title | Const  
---|---  
Type | `model`  
Was this page helpful?
YesNo
[List Models](https://docs.claude.com/en/api/models-list)[Create a Message Batch](https://docs.claude.com/en/api/creating-message-batches)
Assistant
Responses are generated using AI and may contain mistakes.
[Claude Docs home page![light logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/light.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=c877c45432515ee69194cb19e9f983a2)![dark logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/dark.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=f5bb877be0cb3cba86cf6d7c88185216)](https://docs.claude.com/)
Company
Help and security
[Support center](https://support.claude.com/)
Learn
[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)
Terms and policies
