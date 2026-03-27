"""
Built-in ECE (Elastic Certified Engineer) exam question bank for Elasticsearch 8.1.

Each question has:
  - id: unique identifier
  - category: exam domain
  - question: the question text
  - options: list of answer choices (for multiple-choice questions)
  - answer: correct answer key (A/B/C/D) or short text for open-ended
  - explanation: why the answer is correct
"""

QUESTIONS = [
    # ─────────────────────────────────────────────────────────────────────────
    # INSTALLATION & CONFIGURATION
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 1,
        "category": "Installation & Configuration",
        "question": "Which file is the primary configuration file for an Elasticsearch 8.1 node?",
        "options": {
            "A": "elasticsearch.yml",
            "B": "config.json",
            "C": "node.yml",
            "D": "settings.xml",
        },
        "answer": "A",
        "explanation": (
            "elasticsearch.yml is the main configuration file for every Elasticsearch node. "
            "It lives in the $ES_HOME/config directory and controls settings such as "
            "cluster name, node name, network host, and discovery."
        ),
    },
    {
        "id": 2,
        "category": "Installation & Configuration",
        "question": (
            "In Elasticsearch 8.1, which JVM option file should you use to "
            "set the heap size instead of editing jvm.options directly?"
        ),
        "options": {
            "A": "jvm.options.d/*.options files",
            "B": "elasticsearch.yml under 'jvm.heap' key",
            "C": "config/heap.cfg",
            "D": "config/java.ini",
        },
        "answer": "A",
        "explanation": (
            "Starting from Elasticsearch 7.7 you should place custom JVM options in "
            "drop-in files under jvm.options.d/ (e.g. custom-heap.options) rather than "
            "editing the shipped jvm.options file, which is overwritten on upgrades."
        ),
    },
    {
        "id": 3,
        "category": "Installation & Configuration",
        "question": (
            "What is the recommended way to set the Elasticsearch heap size in 8.1?"
        ),
        "options": {
            "A": "Set ES_JAVA_OPTS environment variable only",
            "B": "Use the ES_HEAP_SIZE environment variable",
            "C": "Set -Xms and -Xmx to the same value in a jvm.options.d file",
            "D": "Configure heap in elasticsearch.yml under node.heap",
        },
        "answer": "C",
        "explanation": (
            "Elasticsearch recommends setting -Xms and -Xmx to the same value (no more "
            "than 50 % of available RAM, and no more than 31 GB) to avoid heap resizing "
            "pauses at runtime."
        ),
    },
    {
        "id": 4,
        "category": "Installation & Configuration",
        "question": (
            "Which setting in elasticsearch.yml enables a node to be discovered "
            "by other nodes in the cluster?"
        ),
        "options": {
            "A": "network.host",
            "B": "discovery.seed_hosts",
            "C": "node.master",
            "D": "cluster.initial_master_nodes",
        },
        "answer": "B",
        "explanation": (
            "discovery.seed_hosts provides a list of hosts that a node uses to "
            "bootstrap discovery of the cluster. cluster.initial_master_nodes is used "
            "only once during the very first cluster bootstrap."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # INDEXING
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 5,
        "category": "Indexing",
        "question": (
            "What is the default number of primary shards for a new index in "
            "Elasticsearch 8.1?"
        ),
        "options": {
            "A": "5",
            "B": "3",
            "C": "1",
            "D": "10",
        },
        "answer": "C",
        "explanation": (
            "Since Elasticsearch 7.0 the default number of primary shards per index "
            "changed from 5 to 1. You can override this with index.number_of_shards "
            "in the index settings."
        ),
    },
    {
        "id": 6,
        "category": "Indexing",
        "question": "Which API is used to reindex documents from one index to another in Elasticsearch 8.1?",
        "options": {
            "A": "POST /_copy",
            "B": "POST /_reindex",
            "C": "PUT /_transfer",
            "D": "POST /_clone",
        },
        "answer": "B",
        "explanation": (
            "The Reindex API (POST /_reindex) copies documents from a source index "
            "(or indices) into a destination index. The _clone API creates a copy of "
            "an entire index including its settings and mappings but is different from reindexing."
        ),
    },
    {
        "id": 7,
        "category": "Indexing",
        "question": (
            "Which parameter controls the refresh interval of an Elasticsearch index, "
            "and what is its default value?"
        ),
        "options": {
            "A": "index.refresh_interval – default 30s",
            "B": "index.refresh_interval – default 1s",
            "C": "index.flush_interval – default 5s",
            "D": "index.sync_interval – default 1s",
        },
        "answer": "B",
        "explanation": (
            "index.refresh_interval controls how often a shard performs a refresh "
            "operation that makes recently indexed documents visible to search. "
            "The default is 1s. Setting it to -1 disables automatic refreshes."
        ),
    },
    {
        "id": 8,
        "category": "Indexing",
        "question": "What is an ingest pipeline in Elasticsearch 8.1?",
        "options": {
            "A": "A Logstash configuration file",
            "B": "A series of processors applied to documents before indexing",
            "C": "A Kibana dashboard template",
            "D": "A cross-cluster replication policy",
        },
        "answer": "B",
        "explanation": (
            "An ingest pipeline is a sequence of processors defined in Elasticsearch "
            "that transform or enrich documents before they are indexed. "
            "Processors can parse dates, rename fields, remove fields, and more."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # MAPPINGS
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 9,
        "category": "Mappings",
        "question": (
            "What happens when you try to index a document with a field that does not "
            "exist in the current mapping and dynamic mapping is enabled?"
        ),
        "options": {
            "A": "The document is rejected",
            "B": "The field is ignored silently",
            "C": "The field is dynamically added to the mapping",
            "D": "Elasticsearch throws a MapperParsingException",
        },
        "answer": "C",
        "explanation": (
            "When dynamic mapping is enabled (the default), Elasticsearch automatically "
            "detects and adds new fields to the index mapping when new documents "
            "containing unknown fields are indexed."
        ),
    },
    {
        "id": 10,
        "category": "Mappings",
        "question": (
            "Which field data type should you use to store structured JSON objects "
            "in a flattened single-level structure to avoid mapping explosions?"
        ),
        "options": {
            "A": "object",
            "B": "nested",
            "C": "flattened",
            "D": "keyword",
        },
        "answer": "C",
        "explanation": (
            "The 'flattened' data type stores an entire JSON object as a single field, "
            "mapping the object's keys as keyword sub-fields. This prevents mapping "
            "explosion when objects have many unique keys."
        ),
    },
    {
        "id": 11,
        "category": "Mappings",
        "question": (
            "What is the difference between the 'text' and 'keyword' field types in Elasticsearch 8.1?"
        ),
        "options": {
            "A": "'text' is for full-text search; 'keyword' is for exact-value matching and aggregations",
            "B": "'text' stores numbers; 'keyword' stores strings",
            "C": "'keyword' is analyzed; 'text' is not analyzed",
            "D": "They are identical; 'keyword' is an alias for 'text'",
        },
        "answer": "A",
        "explanation": (
            "'text' fields are analyzed (tokenized and normalized) and are suitable "
            "for full-text search. 'keyword' fields are not analyzed and are used for "
            "exact matching, filtering, sorting, and aggregations."
        ),
    },
    {
        "id": 12,
        "category": "Mappings",
        "question": "How do you prevent a field from being indexed in Elasticsearch 8.1?",
        "options": {
            "A": "Set 'index: false' on the field mapping",
            "B": "Set 'store: false' on the field mapping",
            "C": "Remove the field from the _source",
            "D": "Set 'enabled: false' on the index",
        },
        "answer": "A",
        "explanation": (
            "Setting 'index: false' on a field mapping prevents that field from being "
            "indexed. The field will still be stored in _source (if _source is enabled) "
            "but cannot be searched."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # SEARCHING
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 13,
        "category": "Searching",
        "question": (
            "Which query type in Elasticsearch is used to find documents where "
            "a field value falls within a given range?"
        ),
        "options": {
            "A": "match query",
            "B": "term query",
            "C": "range query",
            "D": "wildcard query",
        },
        "answer": "C",
        "explanation": (
            "The range query returns documents that contain terms within a provided "
            "range. Parameters include 'gte' (greater than or equal), 'lte' "
            "(less than or equal), 'gt', and 'lt'."
        ),
    },
    {
        "id": 14,
        "category": "Searching",
        "question": "What does the 'filter' context do differently from the 'query' context in Elasticsearch?",
        "options": {
            "A": "Filter context calculates relevance scores; query context does not",
            "B": "Filter context does not calculate relevance scores and results are cached",
            "C": "Filter context only works with keyword fields",
            "D": "Filter context requires a separate index",
        },
        "answer": "B",
        "explanation": (
            "In filter context, a query clause answers 'does this document match?' "
            "without computing a relevance score. Filtered results are also cached "
            "by Elasticsearch for better performance on repeated queries."
        ),
    },
    {
        "id": 15,
        "category": "Searching",
        "question": (
            "Which search type executes a query across multiple shards in two rounds "
            "to improve the accuracy of relevance scoring?"
        ),
        "options": {
            "A": "query_then_fetch (default)",
            "B": "dfs_query_then_fetch",
            "C": "count",
            "D": "scan",
        },
        "answer": "B",
        "explanation": (
            "dfs_query_then_fetch first gathers global term/document frequencies from "
            "all shards, then executes the query using those global stats. "
            "This produces more accurate relevance scores, at the cost of extra "
            "network round-trips."
        ),
    },
    {
        "id": 16,
        "category": "Searching",
        "question": (
            "What is a 'scroll' API used for in Elasticsearch 8.1 and what is its "
            "recommended replacement?"
        ),
        "options": {
            "A": "Paginating large result sets; replaced by search_after with a PIT",
            "B": "Streaming data into Elasticsearch; replaced by the Bulk API",
            "C": "Monitoring cluster health; replaced by the CAT API",
            "D": "Cross-cluster search; replaced by CCS with async search",
        },
        "answer": "A",
        "explanation": (
            "The Scroll API was designed to retrieve large numbers of results "
            "efficiently, but it is now deprecated for deep pagination. "
            "The recommended approach is to use 'search_after' combined with a "
            "Point in Time (PIT) to paginate consistently through large result sets."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # AGGREGATIONS
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 17,
        "category": "Aggregations",
        "question": "Which aggregation type computes statistics (min, max, avg, sum, count) over a numeric field?",
        "options": {
            "A": "terms aggregation",
            "B": "histogram aggregation",
            "C": "stats aggregation",
            "D": "cardinality aggregation",
        },
        "answer": "C",
        "explanation": (
            "The 'stats' aggregation is a multi-value metrics aggregation that "
            "computes stats (count, min, max, avg, sum) over numeric fields. "
            "The 'extended_stats' aggregation also includes variance and standard deviation."
        ),
    },
    {
        "id": 18,
        "category": "Aggregations",
        "question": (
            "What does the 'terms' aggregation do in Elasticsearch 8.1?"
        ),
        "options": {
            "A": "Performs full-text analysis on a text field",
            "B": "Groups documents by unique field values and counts documents per bucket",
            "C": "Computes percentiles of a numeric field",
            "D": "Searches for terms matching a wildcard pattern",
        },
        "answer": "B",
        "explanation": (
            "The 'terms' aggregation dynamically builds a bucket for each unique "
            "value encountered in the specified field, and counts the number of "
            "documents falling into each bucket. It returns the top N buckets "
            "by document count by default."
        ),
    },
    {
        "id": 19,
        "category": "Aggregations",
        "question": (
            "Which pipeline aggregation calculates the derivative of another aggregation's values?"
        ),
        "options": {
            "A": "moving_avg",
            "B": "derivative",
            "C": "bucket_sort",
            "D": "cumulative_sum",
        },
        "answer": "B",
        "explanation": (
            "The 'derivative' pipeline aggregation calculates the first-order "
            "derivative of a series of values produced by a parent histogram (or "
            "date_histogram) aggregation. This is useful for identifying the rate "
            "of change of a metric over time."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # CLUSTER MANAGEMENT
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 20,
        "category": "Cluster Management",
        "question": "What does a 'yellow' cluster health status mean in Elasticsearch 8.1?",
        "options": {
            "A": "All primary and replica shards are assigned",
            "B": "All primary shards are assigned but at least one replica shard is unassigned",
            "C": "At least one primary shard is unassigned",
            "D": "The cluster is in read-only mode",
        },
        "answer": "B",
        "explanation": (
            "Yellow status means all primary shards are active, but one or more "
            "replica shards are not allocated. Data is still accessible, but fault "
            "tolerance is reduced. Red status indicates one or more primary shards "
            "are unassigned."
        ),
    },
    {
        "id": 21,
        "category": "Cluster Management",
        "question": (
            "Which API would you use to view the current shard allocation in an "
            "Elasticsearch 8.1 cluster?"
        ),
        "options": {
            "A": "GET /_cluster/health",
            "B": "GET /_cat/shards",
            "C": "GET /_nodes/stats",
            "D": "GET /_cluster/settings",
        },
        "answer": "B",
        "explanation": (
            "The CAT shards API (GET /_cat/shards) provides a summary of the shards "
            "in each index, including their state, size, and which nodes they reside on. "
            "Use ?v for verbose column headers and ?h to select specific columns."
        ),
    },
    {
        "id": 22,
        "category": "Cluster Management",
        "question": (
            "How do you perform a rolling upgrade of an Elasticsearch 8.1 cluster "
            "with zero downtime?"
        ),
        "options": {
            "A": "Stop all nodes, upgrade all at once, then restart",
            "B": "Disable shard allocation, upgrade one node at a time, re-enable allocation after each node",
            "C": "Use a snapshot to restore to a new cluster running the new version",
            "D": "Enable cross-cluster replication to a new cluster, then switch traffic",
        },
        "answer": "B",
        "explanation": (
            "A rolling upgrade: (1) disable shard allocation, (2) perform a synced "
            "flush, (3) stop and upgrade one node, (4) start the node and re-enable "
            "shard allocation, (5) wait for the cluster to go green, then repeat for "
            "each remaining node."
        ),
    },
    {
        "id": 23,
        "category": "Cluster Management",
        "question": (
            "What is the purpose of 'cluster.routing.allocation.enable' setting "
            "and what does setting it to 'none' do?"
        ),
        "options": {
            "A": "Controls which nodes can join the cluster; 'none' prevents new nodes",
            "B": "Controls shard allocation; 'none' stops Elasticsearch from moving or assigning shards",
            "C": "Controls indexing; 'none' makes the cluster read-only",
            "D": "Controls discovery; 'none' disables unicast discovery",
        },
        "answer": "B",
        "explanation": (
            "cluster.routing.allocation.enable controls whether shard allocation is "
            "enabled. Setting it to 'none' prevents any shards from being allocated "
            "or rebalanced, which is useful during rolling upgrades to avoid "
            "unnecessary shard movement."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # SECURITY
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 24,
        "category": "Security",
        "question": (
            "In Elasticsearch 8.1, what is enabled by default that was optional in "
            "earlier versions?"
        ),
        "options": {
            "A": "Cross-cluster search",
            "B": "Security features (TLS and authentication)",
            "C": "Index lifecycle management",
            "D": "Machine learning",
        },
        "answer": "B",
        "explanation": (
            "Since Elasticsearch 8.0, security features are enabled by default. "
            "TLS for transport and HTTP layers and basic authentication are "
            "automatically configured when you start a new cluster."
        ),
    },
    {
        "id": 25,
        "category": "Security",
        "question": "Which built-in role in Elasticsearch 8.1 grants full read access to all indices?",
        "options": {
            "A": "superuser",
            "B": "kibana_admin",
            "C": "read",
            "D": "monitoring_user",
        },
        "answer": "C",
        "explanation": (
            "The 'read' built-in role grants read-only access to all indices "
            "(read, view_index_metadata privileges). 'superuser' grants full "
            "cluster and index access. 'kibana_admin' grants access to Kibana features."
        ),
    },
    {
        "id": 26,
        "category": "Security",
        "question": (
            "What is field-level security (FLS) in Elasticsearch 8.1?"
        ),
        "options": {
            "A": "Encrypting specific fields using AES-256",
            "B": "Restricting which fields a user can see in search results",
            "C": "Masking field values in Kibana dashboards",
            "D": "Preventing specific fields from being updated",
        },
        "answer": "B",
        "explanation": (
            "Field-level security allows you to control which fields in an index "
            "are accessible to a given role. Users with FLS restrictions will not "
            "see the restricted fields in query results or aggregations."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # SNAPSHOTS & RESTORE
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 27,
        "category": "Snapshots & Restore",
        "question": (
            "What must be configured before you can take a snapshot in Elasticsearch 8.1?"
        ),
        "options": {
            "A": "A dedicated snapshot node",
            "B": "A snapshot repository",
            "C": "Index lifecycle management policy",
            "D": "A hot-warm architecture",
        },
        "answer": "B",
        "explanation": (
            "Before taking snapshots you must register a snapshot repository "
            "(e.g., a shared file system, S3, GCS, or Azure Blob Storage). "
            "The repository defines where snapshot data is stored."
        ),
    },
    {
        "id": 28,
        "category": "Snapshots & Restore",
        "question": (
            "How does Elasticsearch 8.1 store incremental snapshots?"
        ),
        "options": {
            "A": "Each snapshot is a full copy of all segment files",
            "B": "Each snapshot only stores segment files not already present in the repository",
            "C": "Snapshots are stored as compressed JSON exports",
            "D": "Snapshots require a separate backup node",
        },
        "answer": "B",
        "explanation": (
            "Elasticsearch snapshots are incremental. The first snapshot is a full "
            "copy, but subsequent snapshots only copy segment files that have changed "
            "since the last snapshot. Unchanged segment files are referenced from "
            "the existing snapshot."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # INDEX LIFECYCLE MANAGEMENT (ILM)
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 29,
        "category": "Index Lifecycle Management",
        "question": (
            "What are the four phases available in an Elasticsearch 8.1 ILM policy?"
        ),
        "options": {
            "A": "create, update, delete, archive",
            "B": "hot, warm, cold, delete",
            "C": "active, inactive, frozen, purged",
            "D": "primary, replica, frozen, delete",
        },
        "answer": "B",
        "explanation": (
            "An ILM policy can define up to four phases: hot (actively written and "
            "queried), warm (no longer written but still queried), cold (infrequently "
            "queried), and delete (safe to remove). A fifth 'frozen' phase is also "
            "available in Elasticsearch 7.12+ for very infrequently accessed data."
        ),
    },
    {
        "id": 30,
        "category": "Index Lifecycle Management",
        "question": (
            "Which ILM action reduces the number of segments in a shard to improve "
            "search performance?"
        ),
        "options": {
            "A": "rollover",
            "B": "shrink",
            "C": "forcemerge",
            "D": "freeze",
        },
        "answer": "C",
        "explanation": (
            "The 'forcemerge' action merges the shards in an index down to the "
            "specified maximum number of segments (max_num_segments). This is "
            "typically used in the warm phase after an index is read-only "
            "to optimize search performance."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # DATA STREAMS
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 31,
        "category": "Data Streams",
        "question": "What is a data stream in Elasticsearch 8.1?",
        "options": {
            "A": "A real-time feed from Logstash",
            "B": "A collection of time-series indices managed by an ILM policy behind a single named resource",
            "C": "A Kafka topic mirrored into Elasticsearch",
            "D": "A Kibana visualization for time-series data",
        },
        "answer": "B",
        "explanation": (
            "A data stream is a named resource that transparently manages multiple "
            "backing indices optimized for time-series data (logs, metrics, events). "
            "Documents are indexed to the most recent backing index ('write index'), "
            "and ILM can automatically roll over and manage the backing indices."
        ),
    },
    {
        "id": 32,
        "category": "Data Streams",
        "question": (
            "What is required for a data stream index template in Elasticsearch 8.1?"
        ),
        "options": {
            "A": "A @timestamp field of type 'date' and data_stream: {}",
            "B": "A _id field and a version field",
            "C": "An ILM policy and a rollover alias",
            "D": "A keyword field named 'stream'",
        },
        "answer": "A",
        "explanation": (
            "To create a data stream, the matching index template must: (1) include "
            "'data_stream: {}' to mark it as a data stream template, and (2) the "
            "backing indices must contain a '@timestamp' field of type 'date' or "
            "'date_nanos'."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # CROSS-CLUSTER REPLICATION
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 33,
        "category": "Cross-Cluster Replication",
        "question": "What is cross-cluster replication (CCR) used for in Elasticsearch 8.1?",
        "options": {
            "A": "Migrating data between Elasticsearch versions",
            "B": "Replicating indices from a leader cluster to one or more follower clusters",
            "C": "Synchronising Kibana dashboards across clusters",
            "D": "Performing federated search across multiple clusters",
        },
        "answer": "B",
        "explanation": (
            "CCR allows you to replicate indices from a 'leader' cluster to one or "
            "more 'follower' clusters. Use cases include disaster recovery, "
            "geo-proximity access, and centralised reporting across clusters."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────────
    # MONITORING
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 34,
        "category": "Monitoring",
        "question": (
            "Which API provides a quick human-readable overview of index-level "
            "metrics such as document count and store size?"
        ),
        "options": {
            "A": "GET /_stats",
            "B": "GET /_cat/indices",
            "C": "GET /_cluster/stats",
            "D": "GET /_nodes/usage",
        },
        "answer": "B",
        "explanation": (
            "The CAT indices API (GET /_cat/indices) displays a row per index with "
            "columns for health, status, document count, deleted docs, store size, "
            "and primary store size. It is optimised for human readability in a terminal."
        ),
    },
    {
        "id": 35,
        "category": "Monitoring",
        "question": (
            "What does the Cluster Allocation Explain API "
            "(GET /_cluster/allocation/explain) do?"
        ),
        "options": {
            "A": "Lists all nodes in the cluster with their disk usage",
            "B": "Explains why a shard is unassigned or where it would be allocated",
            "C": "Shows the cluster topology in a tree view",
            "D": "Returns the current ILM phase of every index",
        },
        "answer": "B",
        "explanation": (
            "The Cluster Allocation Explain API provides a detailed explanation for "
            "why a shard is currently in its allocation state—whether it is "
            "unassigned, being relocated, or stuck. It is the primary tool for "
            "diagnosing shard allocation issues."
        ),
    },
]

CATEGORIES = sorted({q["category"] for q in QUESTIONS})
