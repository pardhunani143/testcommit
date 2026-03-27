"""
Built-in question bank for the ECE (Elastic Certified Engineer) Elasticsearch 8.1 exam.
Used as a fallback when no OpenAI API key is configured, and to seed the chatbot
with domain-specific context.
"""

# Questions are grouped by exam domain topic.
QUESTION_BANK = {
    "Data Management": [
        {
            "question": "How do you define a custom analyzer in an Elasticsearch 8.1 index mapping?",
            "answer": (
                "A custom analyzer is defined in the 'settings.analysis' block of the index "
                "settings. It combines a tokenizer, zero or more token filters, and optional "
                "character filters. Example:\n"
                "{\n"
                "  \"settings\": {\n"
                "    \"analysis\": {\n"
                "      \"analyzer\": {\n"
                "        \"my_custom_analyzer\": {\n"
                "          \"type\": \"custom\",\n"
                "          \"tokenizer\": \"standard\",\n"
                "          \"filter\": [\"lowercase\", \"stop\"]\n"
                "        }\n"
                "      }\n"
                "    }\n"
                "  }\n"
                "}"
            ),
            "difficulty": "medium",
        },
        {
            "question": (
                "What is the difference between 'text' and 'keyword' field types in "
                "Elasticsearch 8.1?"
            ),
            "answer": (
                "'text' fields are analyzed and broken into tokens, making them suitable for "
                "full-text search. 'keyword' fields are stored as-is (not analyzed) and are "
                "used for exact-value matching, aggregations, sorting, and filtering."
            ),
            "difficulty": "easy",
        },
        {
            "question": "How do you use the Reindex API to copy documents from one index to another?",
            "answer": (
                "Use POST /_reindex with a source and destination:\n"
                "{\n"
                "  \"source\": { \"index\": \"source_index\" },\n"
                "  \"dest\":   { \"index\": \"dest_index\" }\n"
                "}\n"
                "You can add a query to filter which documents are reindexed, and use "
                "'op_type': 'create' to avoid overwriting existing docs."
            ),
            "difficulty": "medium",
        },
        {
            "question": "Explain the purpose of Index Lifecycle Management (ILM) in Elasticsearch 8.1.",
            "answer": (
                "ILM automates the management of index lifecycles through phases: Hot, Warm, "
                "Cold, Frozen, and Delete. Each phase can trigger actions such as rollover, "
                "shrink, force-merge, freeze, and delete based on age or size conditions. "
                "This reduces operational overhead for time-series data."
            ),
            "difficulty": "medium",
        },
        {
            "question": "What is a data stream in Elasticsearch 8.1 and when would you use it?",
            "answer": (
                "A data stream is an abstraction over multiple backing indices optimized for "
                "append-only, time-series data (e.g., logs, metrics). It automatically manages "
                "rollover and is paired with ILM policies. You use it when data is always "
                "appended and queried by time range."
            ),
            "difficulty": "medium",
        },
        {
            "question": "How do you create an ingest pipeline in Elasticsearch 8.1?",
            "answer": (
                "Use PUT /_ingest/pipeline/<pipeline_id> with a list of processors:\n"
                "{\n"
                "  \"description\": \"My pipeline\",\n"
                "  \"processors\": [\n"
                "    { \"set\": { \"field\": \"env\", \"value\": \"production\" } },\n"
                "    { \"lowercase\": { \"field\": \"message\" } }\n"
                "  ]\n"
                "}\n"
                "Specify the pipeline at index time via the 'pipeline' query parameter or as "
                "a default pipeline on the index."
            ),
            "difficulty": "medium",
        },
    ],
    "Searching Data": [
        {
            "question": "What is the difference between 'filter' and 'must' clauses in a bool query?",
            "answer": (
                "'must' clauses contribute to the relevance score (_score). 'filter' clauses "
                "do not affect scoring and are cached, making them faster. Use 'filter' for "
                "yes/no criteria (e.g., date ranges, status fields) and 'must' when relevance "
                "ranking matters."
            ),
            "difficulty": "easy",
        },
        {
            "question": "How does the 'match_phrase' query differ from the 'match' query?",
            "answer": (
                "'match' performs a full-text search where terms can appear anywhere in the "
                "field. 'match_phrase' requires all terms to appear in the specified order "
                "with no gaps (unless 'slop' is used). Use 'match_phrase' when word order "
                "matters."
            ),
            "difficulty": "easy",
        },
        {
            "question": "Explain the purpose of the 'highlight' feature in Elasticsearch.",
            "answer": (
                "Highlighting returns fragments of the matched field text with matching tokens "
                "wrapped in HTML tags (default <em>). Useful for showing users why a document "
                "matched. Configured in the 'highlight' section of the request body with "
                "fields, fragment sizes, and number of fragments."
            ),
            "difficulty": "medium",
        },
        {
            "question": "What is a function_score query and when would you use it?",
            "answer": (
                "function_score modifies the relevance score returned by the main query using "
                "functions such as 'weight', 'field_value_factor', 'gauss', 'linear', or "
                "'exp'. Use it to boost documents based on recency, popularity, or geo "
                "distance while still maintaining text relevance."
            ),
            "difficulty": "hard",
        },
        {
            "question": "How do you implement pagination using search_after in Elasticsearch 8.1?",
            "answer": (
                "Add a 'sort' clause and use the sort values from the last hit as the "
                "'search_after' parameter in the next request. Unlike from/size, search_after "
                "is efficient for deep pagination and requires a consistent sort order. Include "
                "a tiebreaker field (e.g., _id) to avoid duplicate results."
            ),
            "difficulty": "medium",
        },
        {
            "question": "What is the purpose of the 'explain' API in Elasticsearch?",
            "answer": (
                "The Explain API (GET /<index>/_explain/<id>) shows why a specific document "
                "received its relevance score for a given query. It breaks down the TF-IDF or "
                "BM25 calculation, showing field-level contributions. Useful for debugging "
                "unexpected ranking results."
            ),
            "difficulty": "medium",
        },
        {
            "question": "How do you use runtime fields in an Elasticsearch 8.1 search request?",
            "answer": (
                "Runtime fields are defined in the 'runtime_mappings' section of the search "
                "request (or index mapping). They are computed at query time using a Painless "
                "script. Example:\n"
                "{\n"
                "  \"runtime_mappings\": {\n"
                "    \"price_with_tax\": {\n"
                "      \"type\": \"double\",\n"
                "      \"script\": \"emit(doc['price'].value * 1.1)\"\n"
                "    }\n"
                "  }\n"
                "}"
            ),
            "difficulty": "hard",
        },
    ],
    "Aggregations": [
        {
            "question": "What is the difference between 'terms' and 'significant_terms' aggregations?",
            "answer": (
                "'terms' returns the most frequent values for a field. 'significant_terms' "
                "returns terms that are statistically more frequent in the query result set "
                "compared to the background corpus, surfacing terms that are unusual or "
                "noteworthy in context."
            ),
            "difficulty": "medium",
        },
        {
            "question": "How do you nest a metric aggregation inside a bucket aggregation?",
            "answer": (
                "Define a sub-aggregation using the 'aggs' (or 'aggregations') key inside the "
                "parent bucket aggregation. Example – average price per category:\n"
                "{\n"
                "  \"aggs\": {\n"
                "    \"by_category\": {\n"
                "      \"terms\": { \"field\": \"category\" },\n"
                "      \"aggs\": {\n"
                "        \"avg_price\": { \"avg\": { \"field\": \"price\" } }\n"
                "      }\n"
                "    }\n"
                "  }\n"
                "}"
            ),
            "difficulty": "easy",
        },
        {
            "question": "Explain the 'cardinality' aggregation and its trade-offs.",
            "answer": (
                "The cardinality aggregation estimates the number of distinct values for a "
                "field using the HyperLogLog++ algorithm. It is approximate (controlled by "
                "'precision_threshold': 1–40000). Higher precision uses more memory. Use it "
                "when exact count is not required and performance matters."
            ),
            "difficulty": "medium",
        },
        {
            "question": "What is a pipeline aggregation and give an example?",
            "answer": (
                "Pipeline aggregations operate on the output of other aggregations rather than "
                "on documents directly. For example, 'avg_bucket' computes the average of a "
                "metric across all buckets of a sibling aggregation:\n"
                "{\n"
                "  \"aggs\": {\n"
                "    \"monthly_sales\": { \"date_histogram\": { ... }, \"aggs\": { \"total\": { \"sum\": { \"field\": \"revenue\" } } } },\n"
                "    \"avg_monthly\": { \"avg_bucket\": { \"buckets_path\": \"monthly_sales>total\" } }\n"
                "  }\n"
                "}"
            ),
            "difficulty": "hard",
        },
    ],
    "Mappings & Analysis": [
        {
            "question": "How do you prevent dynamic mapping in Elasticsearch 8.1?",
            "answer": (
                "Set 'dynamic' to 'false' (ignores new fields), 'strict' (throws an exception "
                "for unknown fields), or 'runtime' (maps new fields as runtime fields) in the "
                "index mapping. Example: PUT /my_index { \"mappings\": { \"dynamic\": \"strict\" } }"
            ),
            "difficulty": "easy",
        },
        {
            "question": "What is the purpose of the 'copy_to' mapping parameter?",
            "answer": (
                "'copy_to' copies the values of multiple source fields into a single target "
                "field, which can then be queried as a catch-all field. The target field is "
                "not stored in _source. It's often used to create a combined 'full_text' "
                "search field without duplicating data in _source."
            ),
            "difficulty": "medium",
        },
        {
            "question": "Explain the 'multi-fields' mapping feature in Elasticsearch.",
            "answer": (
                "Multi-fields allow a single field to be indexed in multiple ways using the "
                "'fields' parameter. A common pattern is indexing a string as both 'text' "
                "(for full-text search) and 'keyword' (for sorting/aggregation):\n"
                "\"title\": { \"type\": \"text\", \"fields\": { \"raw\": { \"type\": \"keyword\" } } }"
            ),
            "difficulty": "easy",
        },
        {
            "question": "What is index normalization and how do you disable it for a keyword field?",
            "answer": (
                "Normalization for keyword fields applies a lightweight analysis process "
                "(e.g., lowercase) before indexing. Disable it by setting 'normalizer' to "
                "null or don't set it. To apply normalization, define a custom normalizer in "
                "index settings with the desired filters (e.g., lowercase)."
            ),
            "difficulty": "medium",
        },
    ],
    "Cluster Management": [
        {
            "question": "What is the role of a master-eligible node in an Elasticsearch cluster?",
            "answer": (
                "Master-eligible nodes can be elected as the cluster master, which is "
                "responsible for lightweight cluster-wide actions: creating/deleting indices, "
                "tracking cluster membership, and allocating shards. In Elasticsearch 8.x, "
                "the voting-only node role can participate in elections without becoming master."
            ),
            "difficulty": "easy",
        },
        {
            "question": "How do you perform a rolling restart of an Elasticsearch cluster?",
            "answer": (
                "1. Disable shard allocation: PUT /_cluster/settings { \"persistent\": { \"cluster.routing.allocation.enable\": \"primaries\" } }\n"
                "2. Stop non-essential indexing and flush: POST /_flush\n"
                "3. Restart one node, wait for it to join the cluster.\n"
                "4. Re-enable shard allocation and wait for green status.\n"
                "5. Repeat for each node."
            ),
            "difficulty": "hard",
        },
        {
            "question": "What does the Cluster Health API report and what do the status colors mean?",
            "answer": (
                "GET /_cluster/health returns overall cluster status:\n"
                "• green – all primary and replica shards are assigned.\n"
                "• yellow – all primaries assigned, but some replicas are not.\n"
                "• red – some primary shards are not assigned; data may be unavailable."
            ),
            "difficulty": "easy",
        },
        {
            "question": "How do you configure shard allocation awareness in Elasticsearch 8.1?",
            "answer": (
                "Set node attributes (e.g., node.attr.zone: zone1) on each node, then configure "
                "allocation awareness:\n"
                "PUT /_cluster/settings {\n"
                "  \"persistent\": {\n"
                "    \"cluster.routing.allocation.awareness.attributes\": \"zone\"\n"
                "  }\n"
                "}\n"
                "For forced awareness, add 'cluster.routing.allocation.awareness.force.zone.values'."
            ),
            "difficulty": "hard",
        },
        {
            "question": "What is cross-cluster search (CCS) and how do you configure it?",
            "answer": (
                "CCS allows a local cluster to search indices on remote clusters. Configure "
                "remote clusters via cluster settings or elasticsearch.yml:\n"
                "PUT /_cluster/settings {\n"
                "  \"persistent\": {\n"
                "    \"cluster.remote.my_remote.seeds\": [\"remote-node:9300\"]\n"
                "  }\n"
                "}\n"
                "Then search with: GET /my_remote:remote_index/_search"
            ),
            "difficulty": "hard",
        },
    ],
    "Security": [
        {
            "question": "How do you enable and configure TLS/SSL for inter-node communication in Elasticsearch 8.1?",
            "answer": (
                "In Elasticsearch 8.x, TLS is enabled by default for new clusters. Configure "
                "in elasticsearch.yml:\n"
                "xpack.security.transport.ssl.enabled: true\n"
                "xpack.security.transport.ssl.verification_mode: certificate\n"
                "xpack.security.transport.ssl.keystore.path: certs/elastic-certificates.p12\n"
                "Generate certificates with: bin/elasticsearch-certutil ca && bin/elasticsearch-certutil cert"
            ),
            "difficulty": "hard",
        },
        {
            "question": "What is role-based access control (RBAC) in Elasticsearch 8.1?",
            "answer": (
                "RBAC controls what users can do in Elasticsearch. A role defines: cluster "
                "privileges (e.g., monitor, manage), index privileges (e.g., read, write, "
                "manage) on specific index patterns, and field/document-level security. Users "
                "are assigned one or more roles. Roles are defined with PUT /_security/role/<name>."
            ),
            "difficulty": "medium",
        },
        {
            "question": "Explain document-level security (DLS) and field-level security (FLS) in Elasticsearch.",
            "answer": (
                "DLS restricts which documents a user can access by applying a query to the "
                "role definition. FLS restricts which fields are visible by specifying allowed "
                "or denied fields. Both are configured within a role's index privileges:\n"
                "{ \"indices\": [{ \"names\": [\"orders\"], \"privileges\": [\"read\"], "
                "\"query\": \"{\\\"term\\\":{\\\"region\\\":\\\"us\\\"}}\", "
                "\"field_security\": { \"grant\": [\"order_id\", \"amount\"] } }] }"
            ),
            "difficulty": "hard",
        },
        {
            "question": "How do you reset the 'elastic' superuser password in Elasticsearch 8.1?",
            "answer": (
                "Use the elasticsearch-reset-password tool:\n"
                "bin/elasticsearch-reset-password -u elastic\n"
                "This generates a random password. To set a specific password:\n"
                "bin/elasticsearch-reset-password -u elastic -i\n"
                "Alternatively use: POST /_security/user/elastic/_password { \"password\": \"new_pw\" }"
            ),
            "difficulty": "easy",
        },
    ],
    "Performance & Monitoring": [
        {
            "question": "What are the key metrics to monitor for Elasticsearch cluster health?",
            "answer": (
                "Key metrics include:\n"
                "• JVM heap usage (keep below 75%)\n"
                "• GC frequency and duration\n"
                "• Search and indexing latency/throughput\n"
                "• Shard count and size\n"
                "• Disk I/O and available disk space\n"
                "• Thread pool queue sizes and rejected counts\n"
                "• Cluster status (green/yellow/red)\n"
                "Use GET /_nodes/stats and the Monitoring UI in Kibana."
            ),
            "difficulty": "medium",
        },
        {
            "question": "How do you optimize Elasticsearch indexing performance?",
            "answer": (
                "• Use bulk indexing (POST /_bulk) to batch documents.\n"
                "• Increase refresh_interval (e.g., '30s') to reduce I/O during bulk loads.\n"
                "• Disable replicas during initial load, then re-enable.\n"
                "• Increase index.translog.durability to 'async' for non-critical data.\n"
                "• Use multiple shards to parallelize indexing across nodes.\n"
                "• Tune thread pool sizes for write operations."
            ),
            "difficulty": "medium",
        },
        {
            "question": "What is the force merge API and when should you use it?",
            "answer": (
                "POST /<index>/_forcemerge?max_num_segments=1 merges Lucene segments into "
                "fewer, larger ones. Use on read-only (closed for writes) indices to improve "
                "search performance and free disk space. Avoid on actively written indices as "
                "it is I/O intensive and can impact cluster performance."
            ),
            "difficulty": "medium",
        },
        {
            "question": "Explain the circuit breaker mechanism in Elasticsearch 8.1.",
            "answer": (
                "Circuit breakers prevent out-of-memory errors by estimating memory usage "
                "before executing operations. Types include:\n"
                "• Parent breaker – overall memory limit.\n"
                "• Field data breaker – limits field data cache size.\n"
                "• Request breaker – limits per-request memory.\n"
                "• In-flight requests breaker – limits memory for in-flight HTTP requests.\n"
                "When a limit is exceeded, a CircuitBreakingException is thrown."
            ),
            "difficulty": "hard",
        },
    ],
    "Snapshot & Restore": [
        {
            "question": "How do you register a snapshot repository in Elasticsearch 8.1?",
            "answer": (
                "Use PUT /_snapshot/<repo_name> with the repository type and settings. "
                "For a shared filesystem:\n"
                "PUT /_snapshot/my_backup {\n"
                "  \"type\": \"fs\",\n"
                "  \"settings\": { \"location\": \"/mnt/snapshots\" }\n"
                "}\n"
                "Other types: s3, gcs, azure, hdfs (via plugins)."
            ),
            "difficulty": "easy",
        },
        {
            "question": "What is a searchable snapshot and what are its benefits?",
            "answer": (
                "Searchable snapshots (available with appropriate license) allow you to search "
                "snapshot data without fully restoring it to local disk. Benefits include "
                "reduced storage costs (data lives in the snapshot repository), and integration "
                "with ILM cold/frozen tiers to move data off expensive local storage while "
                "keeping it searchable."
            ),
            "difficulty": "hard",
        },
        {
            "question": "How do you restore specific indices from a snapshot?",
            "answer": (
                "POST /_snapshot/<repo>/<snapshot>/_restore {\n"
                "  \"indices\": \"index_1,index_2\",\n"
                "  \"ignore_unavailable\": true,\n"
                "  \"include_global_state\": false,\n"
                "  \"rename_pattern\": \"index_(.*)\",\n"
                "  \"rename_replacement\": \"restored_index_$1\"\n"
                "}\n"
                "Note: You cannot restore to an index that already exists (must delete or rename)."
            ),
            "difficulty": "medium",
        },
    ],
}

ALL_TOPICS = list(QUESTION_BANK.keys())


def get_questions_by_topic(topic: str) -> list:
    """Return all questions for a given topic (case-insensitive partial match)."""
    topic_lower = topic.lower()
    for key, questions in QUESTION_BANK.items():
        if topic_lower in key.lower():
            return questions
    return []


def get_random_question(topic: str = None) -> dict:
    """Return a random question, optionally filtered by topic."""
    import random

    if topic:
        questions = get_questions_by_topic(topic)
    else:
        questions = [q for qs in QUESTION_BANK.values() for q in qs]

    if not questions:
        return {}
    return random.choice(questions)


def get_all_questions() -> list:
    """Return all questions across all topics."""
    return [q for qs in QUESTION_BANK.values() for q in qs]
