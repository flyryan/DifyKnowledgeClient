# Knowledge API

## Authentication

Service API authenticates using an `API-Key`.

It is suggested that developers store the `API-Key` in the backend instead of sharing or storing it in the client side to avoid the leakage of the `API-Key`, which may lead to property loss.

All API requests should include your `API-Key` in the **`Authorization`** HTTP Header, as shown below:

```javascript
Authorization: Bearer {API_KEY}
```

---

## API Endpoints

### Create a Document from Text

**POST** `/datasets/{dataset_id}/document/create-by-text`

This API is based on an existing knowledge and creates a new document through text based on this knowledge.

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `name` | string | Document name |
| `text` | string | Document content |
| `indexing_technique` | string | Index mode<br/>• `high_quality` High quality: embedding using embedding model, built as vector database index<br/>• `economy` Economy: Build using inverted index of keyword table index |
| `doc_form` | string | Format of indexed content<br/>• `text_model` Text documents are directly embedded; `economy` mode defaults to using this form<br/>• `hierarchical_model` Parent-child mode<br/>• `qa_model` Q&A Mode: Generates Q&A pairs for segmented documents and then embeds the questions |
| `doc_language` | string | In Q&A mode, specify the language of the document, for example: `English`, `Chinese` |
| `process_rule` | object | Processing rules (see details below) |

##### Process Rule Object

- `mode` (string) Cleaning, segmentation mode, automatic / custom / hierarchical
- `rules` (object) Custom rules (in automatic mode, this field is empty)
  - `pre_processing_rules` (array[object]) Preprocessing rules
    - `id` (string) Unique identifier for the preprocessing rule
      - `remove_extra_spaces` Replace consecutive spaces, newlines, tabs
      - `remove_urls_emails` Delete URL, email address
    - `enabled` (bool) Whether to select this rule or not. If no document ID is passed in, it represents the default value.
  - `segmentation` (object) Segmentation rules
    - `separator` Custom segment identifier, currently only allows one delimiter to be set. Default is \n
    - `max_tokens` Maximum length (token) defaults to 1000
  - `parent_mode` Retrieval mode of parent chunks: `full-doc` full text retrieval / `paragraph` paragraph retrieval
  - `subchunk_segmentation` (object) Child chunk rules
    - `separator` Segmentation identifier. Currently, only one delimiter is allowed. The default is `***`
    - `max_tokens` The maximum length (tokens) must be validated to be shorter than the length of the parent chunk
    - `chunk_overlap` Define the overlap between adjacent chunks (optional)

> **Note:** When no parameters are set for the knowledge base, the first upload requires the following parameters to be provided; if not provided, the default parameters will be used.

| Name | Type | Description |
|------|------|-------------|
| `retrieval_model` | object | Retrieval model (see details below) |
| `embedding_model` | string | Embedding model name |
| `embedding_model_provider` | string | Embedding model provider |

##### Retrieval Model Object

- `search_method` (string) Search method
  - `hybrid_search` Hybrid search
  - `semantic_search` Semantic search
  - `full_text_search` Full-text search
- `reranking_enable` (bool) Whether to enable reranking
- `reranking_mode` (object) Rerank model configuration
  - `reranking_provider_name` (string) Rerank model provider
  - `reranking_model_name` (string) Rerank model name
- `top_k` (int) Number of results to return
- `score_threshold_enabled` (bool) Whether to enable score threshold
- `score_threshold` (float) Score threshold

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/document/create-by-text' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "text","text": "text","indexing_technique": "high_quality","process_rule": {"mode": "automatic"}}'
```

#### Response Example

```json
{
  "document": {
    "id": "",
    "position": 1,
    "data_source_type": "upload_file",
    "data_source_info": {
        "upload_file_id": ""
    },
    "dataset_process_rule_id": "",
    "name": "text.txt",
    "created_from": "api",
    "created_by": "",
    "created_at": 1695690280,
    "tokens": 0,
    "indexing_status": "waiting",
    "error": null,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "archived": false,
    "display_status": "queuing",
    "word_count": 0,
    "hit_count": 0,
    "doc_form": "text_model"
  },
  "batch": ""
}
```

---

### Create a Document from a File

**POST** `/datasets/{dataset_id}/document/create-by-file`

This API is based on an existing knowledge and creates a new document through a file based on this knowledge.

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `data` | multipart/form-data json string | Document configuration data (see details below) |
| `file` | multipart/form-data | Files that need to be uploaded |

##### Data Object Properties

- `original_document_id` Source document ID (optional)
  - Used to re-upload the document or modify the document cleaning and segmentation configuration. The missing information is copied from the source document
  - The source document cannot be an archived document
  - When original_document_id is passed in, the update operation is performed on behalf of the document. process_rule is a fillable item. If not filled in, the segmentation method of the source document will be used by default
  - When original_document_id is not passed in, the new operation is performed on behalf of the document, and process_rule is required
- `indexing_technique` Index mode
  - `high_quality` High quality: embedding using embedding model, built as vector database index
  - `economy` Economy: Build using inverted index of keyword table index
- `doc_form` Format of indexed content
  - `text_model` Text documents are directly embedded; `economy` mode defaults to using this form
  - `hierarchical_model` Parent-child mode
  - `qa_model` Q&A Mode: Generates Q&A pairs for segmented documents and then embeds the questions
- `doc_language` In Q&A mode, specify the language of the document, for example: `English`, `Chinese`
- `process_rule` Processing rules (same structure as in create-by-text)

> **Note:** When no parameters are set for the knowledge base, the first upload requires the retrieval_model, embedding_model, and embedding_model_provider parameters to be provided.

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/document/create-by-file' \
--header 'Authorization: Bearer {api_key}' \
--form 'data="{"indexing_technique":"high_quality","process_rule":{"rules":{"pre_processing_rules":[{"id":"remove_extra_spaces","enabled":true},{"id":"remove_urls_emails","enabled":true}],"segmentation":{"separator":"###","max_tokens":500}},"mode":"custom"}}";type=text/plain' \
--form 'file=@"/path/to/file"'
```

#### Response Example

```json
{
  "document": {
    "id": "",
    "position": 1,
    "data_source_type": "upload_file",
    "data_source_info": {
      "upload_file_id": ""
    },
    "dataset_process_rule_id": "",
    "name": "Dify.txt",
    "created_from": "api",
    "created_by": "",
    "created_at": 1695308667,
    "tokens": 0,
    "indexing_status": "waiting",
    "error": null,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "archived": false,
    "display_status": "queuing",
    "word_count": 0,
    "hit_count": 0,
    "doc_form": "text_model"
  },
  "batch": ""
}
```

---

### Create an Empty Knowledge Base

**POST** `/datasets`

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `name` | string | Knowledge name |
| `description` | string | Knowledge description (optional) |
| `indexing_technique` | string | Index technique (optional)<br/>If this is not set, embedding_model, embedding_model_provider and retrieval_model will be set to null<br/>• `high_quality` High quality<br/>• `economy` Economy |
| `permission` | string | Permission<br/>• `only_me` Only me<br/>• `all_team_members` All team members<br/>• `partial_members` Partial members |
| `provider` | string | Provider (optional, default: vendor)<br/>• `vendor` Vendor<br/>• `external` External knowledge |
| `external_knowledge_api_id` | string | External knowledge API ID (optional) |
| `external_knowledge_id` | string | External knowledge ID (optional) |
| `embedding_model` | string | Embedding model name (optional) |
| `embedding_model_provider` | string | Embedding model provider name (optional) |
| `retrieval_model` | object | Retrieval model (optional) - same structure as above |

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "name", "permission": "only_me"}'
```

#### Response Example

```json
{
  "id": "",
  "name": "name",
  "description": null,
  "provider": "vendor",
  "permission": "only_me",
  "data_source_type": null,
  "indexing_technique": null,
  "app_count": 0,
  "document_count": 0,
  "word_count": 0,
  "created_by": "",
  "created_at": 1695636173,
  "updated_by": "",
  "updated_at": 1695636173,
  "embedding_model": null,
  "embedding_model_provider": null,
  "embedding_available": null
}
```

---

### Get Knowledge Base List

**GET** `/datasets`

#### Query Parameters

| Name | Type | Description |
|------|------|-------------|
| `keyword` | string | Search keyword, optional |
| `tag_ids` | array[string] | Tag ID list, optional |
| `page` | string | Page number, optional, default 1 |
| `limit` | string | Number of items returned, optional, default 20, range 1-100 |
| `include_all` | boolean | Whether to include all datasets (only effective for owners), optional, defaults to false |

#### Request Example

```bash
curl --location --request GET 'https://trendgpt-difytest.testenvs.click/v1/datasets?page=1&limit=20' \
--header 'Authorization: Bearer {api_key}'
```

#### Response Example

```json
{
  "data": [
    {
      "id": "",
      "name": "name",
      "description": "desc",
      "permission": "only_me",
      "data_source_type": "upload_file",
      "indexing_technique": "",
      "app_count": 2,
      "document_count": 10,
      "word_count": 1200,
      "created_by": "",
      "created_at": "",
      "updated_by": "",
      "updated_at": ""
    }
  ],
  "has_more": true,
  "limit": 20,
  "total": 50,
  "page": 1
}
```

---

### Get Knowledge Base Details

**GET** `/datasets/{dataset_id}`

Get knowledge base details by knowledge base ID.

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge Base ID |

#### Request Example

```bash
curl --location --request GET 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}' \
--header 'Authorization: Bearer {api_key}'
```

#### Response Example

```json
{
  "id": "eaedb485-95ac-4ffd-ab1e-18da6d676a2f",
  "name": "Test Knowledge Base",
  "description": "",
  "provider": "vendor",
  "permission": "only_me",
  "data_source_type": null,
  "indexing_technique": null,
  "app_count": 0,
  "document_count": 0,
  "word_count": 0,
  "created_by": "e99a1635-f725-4951-a99a-1daaaa76cfc6",
  "created_at": 1735620612,
  "updated_by": "e99a1635-f725-4951-a99a-1daaaa76cfc6",
  "updated_at": 1735620612,
  "embedding_model": null,
  "embedding_model_provider": null,
  "embedding_available": true,
  "retrieval_model_dict": {
    "search_method": "semantic_search",
    "reranking_enable": false,
    "reranking_mode": null,
    "reranking_model": {
      "reranking_provider_name": "",
      "reranking_model_name": ""
    },
    "weights": null,
    "top_k": 2,
    "score_threshold_enabled": false,
    "score_threshold": null
  },
  "tags": [],
  "doc_form": null,
  "external_knowledge_info": {
    "external_knowledge_id": null,
    "external_knowledge_api_id": null,
    "external_knowledge_api_name": null,
    "external_knowledge_api_endpoint": null
  },
  "external_retrieval_model": {
    "top_k": 2,
    "score_threshold": 0.0,
    "score_threshold_enabled": null
  }
}
```

---

### Update Knowledge Base

**PATCH** `/datasets/{dataset_id}`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge Base ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `indexing_technique` | string | Index technique (optional)<br/>• `high_quality` High quality<br/>• `economy` Economy |
| `permission` | string | Permission<br/>• `only_me` Only me<br/>• `all_team_members` All team members<br/>• `partial_members` Partial members |
| `embedding_model_provider` | string | Specified embedding model provider, must be set up in the system first, corresponding to the provider field (Optional) |
| `embedding_model` | string | Specified embedding model, corresponding to the model field (Optional) |
| `retrieval_model` | object | Retrieval model (optional, if not filled, it will be recalled according to the default method) |
| `partial_member_list` | array | Partial member list (Optional) |

##### Retrieval Model Object for Update

- `search_method` (text) Search method: One of the following four keywords is required
  - `keyword_search` Keyword search
  - `semantic_search` Semantic search
  - `full_text_search` Full-text search
  - `hybrid_search` Hybrid search
- `reranking_enable` (bool) Whether to enable reranking, required if the search mode is semantic_search or hybrid_search (optional)
- `reranking_mode` (object) Rerank model configuration, required if reranking is enabled
  - `reranking_provider_name` (string) Rerank model provider
  - `reranking_model_name` (string) Rerank model name
- `weights` (float) Semantic search weight setting in hybrid search mode
- `top_k` (integer) Number of results to return (optional)
- `score_threshold_enabled` (bool) Whether to enable score threshold
- `score_threshold` (float) Score threshold

#### Request Example

```bash
curl --location --request PATCH 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
      "name": "Test Knowledge Base", 
      "indexing_technique": "high_quality", 
      "permission": "only_me", 
      "embedding_model_provider": "zhipuai", 
      "embedding_model": "embedding-3", 
      "retrieval_model": {
        "search_method": "keyword_search",
        "reranking_enable": false,
        "reranking_mode": null,
        "reranking_model": {
            "reranking_provider_name": "",
            "reranking_model_name": ""
        },
        "weights": null,
        "top_k": 1,
        "score_threshold_enabled": false,
        "score_threshold": null
      }, 
      "partial_member_list": []
    }'
```

#### Response Example

```json
{
  "id": "eaedb485-95ac-4ffd-ab1e-18da6d676a2f",
  "name": "Test Knowledge Base",
  "description": "",
  "provider": "vendor",
  "permission": "only_me",
  "data_source_type": null,
  "indexing_technique": "high_quality",
  "app_count": 0,
  "document_count": 0,
  "word_count": 0,
  "created_by": "e99a1635-f725-4951-a99a-1daaaa76cfc6",
  "created_at": 1735620612,
  "updated_by": "e99a1635-f725-4951-a99a-1daaaa76cfc6",
  "updated_at": 1735622679,
  "embedding_model": "embedding-3",
  "embedding_model_provider": "zhipuai",
  "embedding_available": null,
  "retrieval_model_dict": {
      "search_method": "semantic_search",
      "reranking_enable": false,
      "reranking_mode": null,
      "reranking_model": {
          "reranking_provider_name": "",
          "reranking_model_name": ""
      },
      "weights": null,
      "top_k": 2,
      "score_threshold_enabled": false,
      "score_threshold": null
  },
  "tags": [],
  "doc_form": null,
  "external_knowledge_info": {
      "external_knowledge_id": null,
      "external_knowledge_api_id": null,
      "external_knowledge_api_name": null,
      "external_knowledge_api_endpoint": null
  },
  "external_retrieval_model": {
      "top_k": 2,
      "score_threshold": 0.0,
      "score_threshold_enabled": null
  },
  "partial_member_list": []
}
```

---

### Delete a Knowledge Base

**DELETE** `/datasets/{dataset_id}`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |

#### Request Example

```bash
curl --location --request DELETE 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}' \
--header 'Authorization: Bearer {api_key}'
```

#### Response

`204 No Content`

---

### Update a Document with Text

**POST** `/datasets/{dataset_id}/documents/{document_id}/update-by-text`

This API is based on an existing knowledge and updates the document through text based on this knowledge.

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `name` | string | Document name (optional) |
| `text` | string | Document content (optional) |
| `process_rule` | object | Processing rules (same structure as in create-by-text) |

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}/update-by-text' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "name","text": "text"}'
```

#### Response Example

```json
{
  "document": {
    "id": "",
    "position": 1,
    "data_source_type": "upload_file",
    "data_source_info": {
      "upload_file_id": ""
    },
    "dataset_process_rule_id": "",
    "name": "name.txt",
    "created_from": "api",
    "created_by": "",
    "created_at": 1695308667,
    "tokens": 0,
    "indexing_status": "waiting",
    "error": null,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "archived": false,
    "display_status": "queuing",
    "word_count": 0,
    "hit_count": 0,
    "doc_form": "text_model"
  },
  "batch": ""
}
```

---

### Update a Document with a File

**POST** `/datasets/{dataset_id}/documents/{document_id}/update-by-file`

This API is based on an existing knowledge, and updates documents through files based on this knowledge.

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `name` | string | Document name (optional) |
| `file` | multipart/form-data | Files to be uploaded |
| `process_rule` | object | Processing rules (same structure as in create-by-text) |

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}/update-by-file' \
--header 'Authorization: Bearer {api_key}' \
--form 'data="{"name":"Dify","indexing_technique":"high_quality","process_rule":{"rules":{"pre_processing_rules":[{"id":"remove_extra_spaces","enabled":true},{"id":"remove_urls_emails","enabled":true}],"segmentation":{"separator":"###","max_tokens":500}},"mode":"custom"}}";type=text/plain' \
--form 'file=@"/path/to/file"'
```

#### Response Example

```json
{
  "document": {
    "id": "",
    "position": 1,
    "data_source_type": "upload_file",
    "data_source_info": {
      "upload_file_id": ""
    },
    "dataset_process_rule_id": "",
    "name": "Dify.txt",
    "created_from": "api",
    "created_by": "",
    "created_at": 1695308667,
    "tokens": 0,
    "indexing_status": "waiting",
    "error": null,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "archived": false,
    "display_status": "queuing",
    "word_count": 0,
    "hit_count": 0,
    "doc_form": "text_model"
  },
  "batch": "20230921150427533684"
}
```

---

### Get Document Embedding Status (Progress)

**GET** `/datasets/{dataset_id}/documents/{batch}/indexing-status`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `batch` | string | Batch number of uploaded documents |

#### Request Example

```bash
curl --location --request GET 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{batch}/indexing-status' \
--header 'Authorization: Bearer {api_key}'
```

#### Response Example

```json
{
  "data":[{
    "id": "",
    "indexing_status": "indexing",
    "processing_started_at": 1681623462.0,
    "parsing_completed_at": 1681623462.0,
    "cleaning_completed_at": 1681623462.0,
    "splitting_completed_at": 1681623462.0,
    "completed_at": null,
    "paused_at": null,
    "error": null,
    "stopped_at": null,
    "completed_segments": 24,
    "total_segments": 100
  }]
}
```

---

### Delete a Document

**DELETE** `/datasets/{dataset_id}/documents/{document_id}`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |

#### Request Example

```bash
curl --location --request DELETE 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}' \
--header 'Authorization: Bearer {api_key}'
```

#### Response

`204 No Content`

---

### Get the Document List of a Knowledge Base

**GET** `/datasets/{dataset_id}/documents`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |

#### Query Parameters

| Name | Type | Description |
|------|------|-------------|
| `keyword` | string | Search keywords, currently only search document names (optional) |
| `page` | string | Page number (optional) |
| `limit` | string | Number of items returned, default 20, range 1-100 (optional) |

#### Request Example

```bash
curl --location --request GET 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents' \
--header 'Authorization: Bearer {api_key}'
```

#### Response Example

```json
{
  "data": [
    {
      "id": "",
      "position": 1,
      "data_source_type": "file_upload",
      "data_source_info": null,
      "dataset_process_rule_id": null,
      "name": "dify",
      "created_from": "",
      "created_by": "",
      "created_at": 1681623639,
      "tokens": 0,
      "indexing_status": "waiting",
      "error": null,
      "enabled": true,
      "disabled_at": null,
      "disabled_by": null,
      "archived": false
    }
  ],
  "has_more": false,
  "limit": 20,
  "total": 9,
  "page": 1
}
```

---

### Add Chunks to a Document

**POST** `/datasets/{dataset_id}/documents/{document_id}/segments`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `segments` | object list | Segment list containing:<br/>• `content` (text) Text content / question content, required<br/>• `answer` (text) Answer content, if the mode of the knowledge is Q&A mode, pass the value (optional)<br/>• `keywords` (list) Keywords (optional) |

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}/segments' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"segments": [{"content": "1","answer": "1","keywords": ["a"]}]}'
```

#### Response Example

```json
{
  "data": [{
    "id": "",
    "position": 1,
    "document_id": "",
    "content": "1",
    "answer": "1",
    "word_count": 25,
    "tokens": 0,
    "keywords": [
      "a"
    ],
    "index_node_id": "",
    "index_node_hash": "",
    "hit_count": 0,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  }],
  "doc_form": "text_model"
}
```

---

### Get Chunks from a Document

**GET** `/datasets/{dataset_id}/documents/{document_id}/segments`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |

#### Query Parameters

| Name | Type | Description |
|------|------|-------------|
| `keyword` | string | Keyword (optional) |
| `status` | string | Search status, completed |
| `page` | string | Page number (optional) |
| `limit` | string | Number of items returned, default 20, range 1-100 (optional) |

#### Request Example

```bash
curl --location --request GET 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}/segments' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'
```

#### Response Example

```json
{
  "data": [{
    "id": "",
    "position": 1,
    "document_id": "",
    "content": "1",
    "answer": "1",
    "word_count": 25,
    "tokens": 0,
    "keywords": [
        "a"
    ],
    "index_node_id": "",
    "index_node_hash": "",
    "hit_count": 0,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  }],
  "doc_form": "text_model",
  "has_more": false,
  "limit": 20,
  "total": 9,
  "page": 1
}
```

---

### Delete a Chunk in a Document

**DELETE** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |
| `segment_id` | string | Document Segment ID |

#### Request Example

```bash
curl --location --request DELETE 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'
```

#### Response

`204 No Content`

---

### Update a Chunk in a Document

**POST** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |
| `segment_id` | string | Document Segment ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `segment` | object | Segment data containing:<br/>• `content` (text) Text content / question content, required<br/>• `answer` (text) Answer content, passed if the knowledge is in Q&A mode (optional)<br/>• `keywords` (list) Keyword (optional)<br/>• `enabled` (bool) False / true (optional)<br/>• `regenerate_child_chunks` (bool) Whether to regenerate child chunks (optional) |

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'\
--data-raw '{"segment": {"content": "1","answer": "1", "keywords": ["a"], "enabled": false}}'
```

#### Response Example

```json
{
  "data": {
    "id": "",
    "position": 1,
    "document_id": "",
    "content": "1",
    "answer": "1",
    "word_count": 25,
    "tokens": 0,
    "keywords": [
        "a"
    ],
    "index_node_id": "",
    "index_node_hash": "",
    "hit_count": 0,
    "enabled": true,
    "disabled_at": null,
    "disabled_by": null,
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  },
  "doc_form": "text_model"
}
```

---

### Create Child Chunk

**POST** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |
| `segment_id` | string | Segment ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `content` | string | Child chunk content |

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"content": "Child chunk content"}'
```

#### Response Example

```json
{
  "data": {
    "id": "",
    "segment_id": "",
    "content": "Child chunk content",
    "word_count": 25,
    "tokens": 0,
    "index_node_id": "",
    "index_node_hash": "",
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  }
}
```

---

### Get Child Chunks

**GET** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |
| `segment_id` | string | Segment ID |

#### Query Parameters

| Name | Type | Description |
|------|------|-------------|
| `keyword` | string | Search keyword (optional) |
| `page` | integer | Page number (optional, default: 1) |
| `limit` | integer | Items per page (optional, default: 20, max: 100) |

#### Request Example

```bash
curl --location --request GET 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks?page=1&limit=20' \
--header 'Authorization: Bearer {api_key}'
```

#### Response Example

```json
{
  "data": [{
    "id": "",
    "segment_id": "",
    "content": "Child chunk content",
    "word_count": 25,
    "tokens": 0,
    "index_node_id": "",
    "index_node_hash": "",
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  }],
  "total": 1,
  "total_pages": 1,
  "page": 1,
  "limit": 20
}
```

---

### Delete Child Chunk

**DELETE** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks/{child_chunk_id}`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |
| `segment_id` | string | Segment ID |
| `child_chunk_id` | string | Child Chunk ID |

#### Request Example

```bash
curl --location --request DELETE 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/segments/{segment_id}/child_chunks/{child_chunk_id}' \
--header 'Authorization: Bearer {api_key}'
```

#### Response

`204 No Content`

---

### Update Child Chunk

**PATCH** `/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks/{child_chunk_id}`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |
| `segment_id` | string | Segment ID |
| `child_chunk_id` | string | Child Chunk ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `content` | string | Child chunk content |

#### Request Example

```bash
curl --location --request PATCH 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks/{child_chunk_id}' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"content": "Updated child chunk content"}'
```

#### Response Example

```json
{
  "data": {
    "id": "",
    "segment_id": "",
    "content": "Updated child chunk content",
    "word_count": 25,
    "tokens": 0,
    "index_node_id": "",
    "index_node_hash": "",
    "status": "completed",
    "created_by": "",
    "created_at": 1695312007,
    "indexing_at": 1695312007,
    "completed_at": 1695312007,
    "error": null,
    "stopped_at": null
  }
}
```

---

### Get Upload File

**GET** `/datasets/{dataset_id}/documents/{document_id}/upload-file`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `document_id` | string | Document ID |

#### Request Example

```bash
curl --location --request GET 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/{document_id}/upload-file' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'
```

#### Response Example

```json
{
  "id": "file_id",
  "name": "file_name",
  "size": 1024,
  "extension": "txt",
  "url": "preview_url",
  "download_url": "download_url",
  "mime_type": "text/plain",
  "created_by": "user_id",
  "created_at": 1728734540
}
```

---

### Retrieve Chunks from a Knowledge Base

**POST** `/datasets/{dataset_id}/retrieve`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `query` | string | Query keyword |
| `retrieval_model` | object | Retrieval model (optional, if not filled, it will be recalled according to the default method) |
| `external_retrieval_model` | object | Unused field |

##### Retrieval Model Object

- `search_method` (text) Search method: One of the following four keywords is required
  - `keyword_search` Keyword search
  - `semantic_search` Semantic search
  - `full_text_search` Full-text search
  - `hybrid_search` Hybrid search
- `reranking_enable` (bool) Whether to enable reranking, required if the search mode is semantic_search or hybrid_search (optional)
- `reranking_mode` (object) Rerank model configuration, required if reranking is enabled
  - `reranking_provider_name` (string) Rerank model provider
  - `reranking_model_name` (string) Rerank model name
- `weights` (float) Semantic search weight setting in hybrid search mode
- `top_k` (integer) Number of results to return (optional)
- `score_threshold_enabled` (bool) Whether to enable score threshold
- `score_threshold` (float) Score threshold

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/retrieve' \
--header 'Authorization: Bearer {api_key}'\
--header 'Content-Type: application/json'\
--data-raw '{
  "query": "test",
  "retrieval_model": {
      "search_method": "keyword_search",
      "reranking_enable": false,
      "reranking_mode": null,
      "reranking_model": {
          "reranking_provider_name": "",
          "reranking_model_name": ""
      },
      "weights": null,
      "top_k": 1,
      "score_threshold_enabled": false,
      "score_threshold": null
  }
}'
```

#### Response Example

```json
{
  "query": {
    "content": "test"
  },
  "records": [
    {
      "segment": {
        "id": "7fa6f24f-8679-48b3-bc9d-bdf28d73f218",
        "position": 1,
        "document_id": "a8c6c36f-9f5d-4d7a-8472-f5d7b75d71d2",
        "content": "Operation guide",
        "answer": null,
        "word_count": 847,
        "tokens": 280,
        "keywords": [
          "install",
          "java",
          "base",
          "scripts",
          "jdk",
          "manual",
          "internal",
          "opens",
          "add",
          "vmoptions"
        ],
        "index_node_id": "39dd8443-d960-45a8-bb46-7275ad7fbc8e",
        "index_node_hash": "0189157697b3c6a418ccf8264a09699f25858975578f3467c76d6bfc94df1d73",
        "hit_count": 0,
        "enabled": true,
        "disabled_at": null,
        "disabled_by": null,
        "status": "completed",
        "created_by": "dbcb1ab5-90c8-41a7-8b78-73b235eb6f6f",
        "created_at": 1728734540,
        "indexing_at": 1728734552,
        "completed_at": 1728734584,
        "error": null,
        "stopped_at": null,
        "document": {
          "id": "a8c6c36f-9f5d-4d7a-8472-f5d7b75d71d2",
          "data_source_type": "upload_file",
          "name": "readme.txt"
        }
      },
      "score": 3.730463140527718e-05,
      "tsne_position": null
    }
  ]
}
```

---

### Create a Knowledge Metadata

**POST** `/datasets/{dataset_id}/metadata`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `type` | string | Metadata type, required |
| `name` | string | Metadata name, required |

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/metadata' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'\
--data-raw '{"type": "string", "name": "test"}'
```

#### Response Example

```json
{
  "id": "abc",
  "type": "string",
  "name": "test"
}
```

---

### Update a Knowledge Metadata

**PATCH** `/datasets/{dataset_id}/metadata/{metadata_id}`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `metadata_id` | string | Metadata ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `name` | string | Metadata name, required |

#### Request Example

```bash
curl --location --request PATCH 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/metadata/{metadata_id}' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'\
--data-raw '{"name": "test"}'
```

#### Response Example

```json
{
  "id": "abc",
  "type": "string",
  "name": "test"
}
```

---

### Delete a Knowledge Metadata

**DELETE** `/datasets/{dataset_id}/metadata/{metadata_id}`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `metadata_id` | string | Metadata ID |

#### Request Example

```bash
curl --location --request DELETE 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/metadata/{metadata_id}' \
--header 'Authorization: Bearer {api_key}'
```

---

### Disable Or Enable Built-in Metadata

**POST** `/datasets/{dataset_id}/metadata/built-in/{action}`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |
| `action` | string | disable/enable |

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/metadata/built-in/{action}' \
--header 'Authorization: Bearer {api_key}'
```

---

### Update Documents Metadata

**POST** `/datasets/{dataset_id}/documents/metadata`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |

#### Request Body

| Name | Type | Description |
|------|------|-------------|
| `operation_data` | object list | Operation data list containing:<br/>• `document_id` (string) Document ID<br/>• `metadata_list` (list) Metadata list<br/>  • `id` (string) Metadata ID<br/>  • `value` (string) Metadata value<br/>  • `name` (string) Metadata name |

#### Request Example

```bash
curl --location --request POST 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/documents/metadata' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'\
--data-raw '{"operation_data": [{"document_id": "document_id", "metadata_list": [{"id": "id", "value": "value", "name": "name"}]}]}'
```

---

### Get Knowledge Metadata List

**GET** `/datasets/{dataset_id}/metadata`

#### Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `dataset_id` | string | Knowledge ID |

#### Request Example

```bash
curl --location --request GET 'https://trendgpt-difytest.testenvs.click/v1/datasets/{dataset_id}/metadata' \
--header 'Authorization: Bearer {api_key}'
```

#### Response Example

```json
{
  "doc_metadata": [
    {
      "id": "",
      "name": "name",
      "type": "string",
      "use_count": 0
    }
  ],
  "built_in_field_enabled": true
}
```

---

### Get Available Embedding Models

**GET** `/workspaces/current/models/model-types/text-embedding`

#### Request Example

```bash
curl --location --location --request GET 'https://trendgpt-difytest.testenvs.click/v1/workspaces/current/models/model-types/text-embedding' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'
```

#### Response Example

```json
{
  "data": [
      {
          "provider": "zhipuai",
          "label": {
              "zh_Hans": "智谱 AI",
              "en_US": "ZHIPU AI"
          },
          "icon_small": {
              "zh_Hans": "http://127.0.0.1:5001/console/api/workspaces/current/model-providers/zhipuai/icon_small/zh_Hans",
              "en_US": "http://127.0.0.1:5001/console/api/workspaces/current/model-providers/zhipuai/icon_small/en_US"
          },
          "icon_large": {
              "zh_Hans": "http://127.0.0.1:5001/console/api/workspaces/current/model-providers/zhipuai/icon_large/zh_Hans",
              "en_US": "http://127.0.0.1:5001/console/api/workspaces/current/model-providers/zhipuai/icon_large/en_US"
          },
          "status": "active",
          "models": [
              {
                  "model": "embedding-3",
                  "label": {
                      "zh_Hans": "embedding-3",
                      "en_US": "embedding-3"
                  },
                  "model_type": "text-embedding",
                  "features": null,
                  "fetch_from": "predefined-model",
                  "model_properties": {
                      "context_size": 8192
                  },
                  "deprecated": false,
                  "status": "active",
                  "load_balancing_enabled": false
              },
              {
                  "model": "embedding-2",
                  "label": {
                      "zh_Hans": "embedding-2",
                      "en_US": "embedding-2"
                  },
                  "model_type": "text-embedding",
                  "features": null,
                  "fetch_from": "predefined-model",
                  "model_properties": {
                      "context_size": 8192
                  },
                  "deprecated": false,
                  "status": "active",
                  "load_balancing_enabled": false
              },
              {
                  "model": "text_embedding",
                  "label": {
                      "zh_Hans": "text_embedding",
                      "en_US": "text_embedding"
                  },
                  "model_type": "text-embedding",
                  "features": null,
                  "fetch_from": "predefined-model",
                  "model_properties": {
                      "context_size": 512
                  },
                  "deprecated": false,
                  "status": "active",
                  "load_balancing_enabled": false
              }
          ]
      }
  ]
}
```

---

## Error Messages

| Name | Type | Description |
|------|------|-------------|
| `code` | string | Error code |
| `status` | number | Error status |
| `message` | string | Error message |

### Example Error Response

```json
{
  "code": "no_file_uploaded",
  "message": "Please upload your file.",
  "status": 400
}
```

### Error Code Reference

| Code | Status | Message |
|------|--------|---------|
| `no_file_uploaded` | 400 | Please upload your file. |
| `too_many_files` | 400 | Only one file is allowed. |
| `file_too_large` | 413 | File size exceeded. |
| `unsupported_file_type` | 415 | File type not allowed. |
| `high_quality_dataset_only` | 400 | Current operation only supports 'high-quality' datasets. |
| `dataset_not_initialized` | 400 | The dataset is still being initialized or indexing. Please wait a moment. |
| `archived_document_immutable` | 403 | The archived document is not editable. |
| `dataset_name_duplicate` | 409 | The dataset name already exists. Please modify your dataset name. |
| `invalid_action` | 400 | Invalid action. |
| `document_already_finished` | 400 | The document has been processed. Please refresh the page or go to the document details. |
| `document_indexing` | 400 | The document is being processed and cannot be edited. |
| `invalid_metadata` | 400 | The metadata content is incorrect. Please check and verify. |