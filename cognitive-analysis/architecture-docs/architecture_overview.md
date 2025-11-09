# Frappe Framework - Technical Architecture Overview

## Executive Summary

Frappe Framework is a full-stack, metadata-driven, low-code web framework written in Python and JavaScript. It provides a comprehensive platform for building database-driven applications with automatic admin interfaces, REST APIs, role-based permissions, and workflow automation.

**Version**: 16.0.0-dev  
**License**: MIT  
**Primary Language**: Python 3.10+  
**Database**: MariaDB (primary), PostgreSQL, SQLite  
**Frontend**: Vue 3, JavaScript/TypeScript  

## System Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Browser]
        MOBILE[Mobile Client]
        API_CLIENT[API Clients]
    end
    
    subgraph "Presentation Layer"
        NGINX[NGINX/Web Server]
        STATIC[Static Assets]
        SOCKETIO[Socket.IO Server]
    end
    
    subgraph "Application Layer"
        WSGI[WSGI Application<br/>Werkzeug]
        HANDLER[Request Handler]
        API[REST API v1/v2]
        AUTH[Authentication Layer]
        SESSION[Session Manager]
    end
    
    subgraph "Business Logic Layer"
        MODEL[Document Model<br/>ORM Layer]
        WORKFLOW[Workflow Engine]
        PERMS[Permission Manager]
        HOOKS[Hooks & Events]
        VALIDATION[Validation Engine]
    end
    
    subgraph "Data Access Layer"
        QB[Query Builder<br/>PyPika]
        DB_ABSTRACT[Database Abstraction]
        MARIADB[MariaDB Driver]
        POSTGRES[PostgreSQL Driver]
        SQLITE[SQLite Driver]
    end
    
    subgraph "Storage & Cache Layer"
        DATABASE[(Database<br/>MariaDB/Postgres)]
        REDIS[(Redis Cache)]
        FILES[File Storage]
        SEARCH[(Whoosh<br/>Full-Text Search)]
    end
    
    subgraph "Background Processing"
        RQ[RQ Worker<br/>Background Jobs]
        SCHEDULER[Cron Scheduler]
        REALTIME[Realtime Events]
    end
    
    subgraph "External Services"
        EMAIL[Email Services<br/>SMTP]
        OAUTH[OAuth Providers]
        WEBHOOKS[External Webhooks]
        INTEGRATIONS[3rd Party APIs]
    end
    
    WEB --> NGINX
    MOBILE --> NGINX
    API_CLIENT --> NGINX
    
    NGINX --> WSGI
    NGINX --> STATIC
    NGINX --> SOCKETIO
    
    WSGI --> HANDLER
    HANDLER --> API
    HANDLER --> AUTH
    
    API --> MODEL
    AUTH --> SESSION
    SESSION --> REDIS
    
    MODEL --> WORKFLOW
    MODEL --> PERMS
    MODEL --> HOOKS
    MODEL --> VALIDATION
    
    MODEL --> QB
    QB --> DB_ABSTRACT
    
    DB_ABSTRACT --> MARIADB
    DB_ABSTRACT --> POSTGRES
    DB_ABSTRACT --> SQLITE
    
    MARIADB --> DATABASE
    POSTGRES --> DATABASE
    SQLITE --> DATABASE
    
    MODEL --> REDIS
    MODEL --> FILES
    MODEL --> SEARCH
    
    WORKFLOW --> RQ
    HOOKS --> RQ
    SCHEDULER --> RQ
    
    SOCKETIO --> REALTIME
    REALTIME --> REDIS
    
    MODEL --> EMAIL
    AUTH --> OAUTH
    HOOKS --> WEBHOOKS
    MODEL --> INTEGRATIONS
    
    style WSGI fill:#e1f5ff
    style MODEL fill:#fff3e0
    style DATABASE fill:#f3e5f5
    style REDIS fill:#ffebee
```

## Core Components Architecture

### 1. Document Model Architecture

The document model is the heart of Frappe Framework, implementing a metadata-driven ORM pattern.

```mermaid
graph LR
    subgraph "Document Lifecycle"
        NEW[New Document]
        VALIDATE[Validate]
        SAVE[Save to DB]
        SUBMIT[Submit]
        CANCEL[Cancel]
        DELETE[Delete]
    end
    
    subgraph "Document Components"
        META[DocType Metadata]
        FIELDS[Field Definitions]
        PERMS[Permissions]
        HOOKS[Controller Hooks]
    end
    
    subgraph "Document Operations"
        GET[get_doc]
        CREATE[new_doc]
        UPDATE[save]
        QUERY[get_list/get_all]
    end
    
    NEW --> VALIDATE
    VALIDATE --> SAVE
    SAVE --> SUBMIT
    SUBMIT --> CANCEL
    SAVE --> DELETE
    
    META --> FIELDS
    FIELDS --> PERMS
    PERMS --> HOOKS
    
    GET --> META
    CREATE --> META
    UPDATE --> META
    QUERY --> META
```

**Key Classes:**
- `Document`: Base class for all documents
- `Meta`: Metadata container for DocTypes
- `BaseDocument`: Core document functionality
- `DocField`: Field definitions and validations

### 2. Database Architecture

Multi-database support with a unified abstraction layer.

```mermaid
graph TB
    subgraph "Query Builder Layer"
        PYPIKA[PyPika Query Builder]
        FRAPPE_QB[Frappe Query Extensions]
    end
    
    subgraph "Database Abstraction"
        DB_BASE[Database Base Class]
        MARIADB_DB[MariaDB Implementation]
        POSTGRES_DB[PostgreSQL Implementation]
        SQLITE_DB[SQLite Implementation]
    end
    
    subgraph "Schema Management"
        SCHEMA[Schema Manager]
        MIGRATIONS[Migration System]
        DDL[DDL Operations]
    end
    
    subgraph "Transaction Management"
        TX[Transaction Context]
        COMMIT[Commit]
        ROLLBACK[Rollback]
        SAVEPOINT[Savepoints]
    end
    
    PYPIKA --> FRAPPE_QB
    FRAPPE_QB --> DB_BASE
    
    DB_BASE --> MARIADB_DB
    DB_BASE --> POSTGRES_DB
    DB_BASE --> SQLITE_DB
    
    DB_BASE --> SCHEMA
    SCHEMA --> MIGRATIONS
    MIGRATIONS --> DDL
    
    DB_BASE --> TX
    TX --> COMMIT
    TX --> ROLLBACK
    TX --> SAVEPOINT
```

**Key Components:**
- `Database`: Base database abstraction
- `MariaDBDatabase`: MariaDB-specific implementation
- `PostgresDatabase`: PostgreSQL-specific implementation
- `Schema`: Schema management and migrations
- `DBQuery`: Advanced query builder

### 3. API Architecture

Versioned REST API with automatic resource generation.

```mermaid
graph TB
    subgraph "API Entry Points"
        REQUEST[HTTP Request]
        API_HANDLER[API Handler]
        VERSION_ROUTER[Version Router]
    end
    
    subgraph "API v1"
        V1_METHOD[/api/v1/method/*]
        V1_RESOURCE[/api/v1/resource/*]
        V1_DOC[/api/v1/resource/:doctype/:name]
    end
    
    subgraph "API v2"
        V2_METHOD[/api/v2/method/*]
        V2_RESOURCE[/api/v2/resource/*]
        V2_DOC[/api/v2/resource/:doctype/:name]
    end
    
    subgraph "API Operations"
        WHITELIST[Whitelist Check]
        AUTH_CHECK[Authorization]
        EXECUTE[Execute Method]
        SERIALIZE[Serialize Response]
    end
    
    subgraph "Resource Operations"
        GET_OP[GET - Read]
        POST_OP[POST - Create]
        PUT_OP[PUT - Update]
        DELETE_OP[DELETE - Remove]
        LIST_OP[LIST - Query]
    end
    
    REQUEST --> API_HANDLER
    API_HANDLER --> VERSION_ROUTER
    
    VERSION_ROUTER --> V1_METHOD
    VERSION_ROUTER --> V1_RESOURCE
    VERSION_ROUTER --> V1_DOC
    
    VERSION_ROUTER --> V2_METHOD
    VERSION_ROUTER --> V2_RESOURCE
    VERSION_ROUTER --> V2_DOC
    
    V1_METHOD --> WHITELIST
    V1_RESOURCE --> AUTH_CHECK
    V1_DOC --> AUTH_CHECK
    
    WHITELIST --> EXECUTE
    AUTH_CHECK --> EXECUTE
    EXECUTE --> SERIALIZE
    
    V1_DOC --> GET_OP
    V1_DOC --> POST_OP
    V1_DOC --> PUT_OP
    V1_DOC --> DELETE_OP
    V1_RESOURCE --> LIST_OP
```

**API Features:**
- Automatic REST endpoint generation
- Versioning (v1, v2)
- Whitelist-based security
- Filter and pagination support
- Custom method exposure

### 4. Authentication & Authorization Architecture

```mermaid
graph TB
    subgraph "Authentication Layer"
        LOGIN[Login Request]
        CREDS[Credential Check]
        TWO_FA[2FA Validation]
        SESSION_CREATE[Create Session]
        TOKEN[Generate Token]
    end
    
    subgraph "Session Management"
        SESSION_STORE[Session Store<br/>Redis]
        COOKIE[Session Cookie]
        CSRF[CSRF Token]
        EXPIRY[Session Expiry]
    end
    
    subgraph "Authorization Layer"
        ROLE_CHECK[Role Check]
        PERM_CHECK[Permission Check]
        DOC_PERMS[Document Permissions]
        FIELD_PERMS[Field-Level Perms]
    end
    
    subgraph "Identity Providers"
        LOCAL_AUTH[Local Database]
        OAUTH_PROVIDER[OAuth 2.0]
        LDAP[LDAP/AD]
        SAML[SAML 2.0]
    end
    
    LOGIN --> CREDS
    CREDS --> LOCAL_AUTH
    CREDS --> OAUTH_PROVIDER
    CREDS --> LDAP
    CREDS --> SAML
    
    CREDS --> TWO_FA
    TWO_FA --> SESSION_CREATE
    SESSION_CREATE --> SESSION_STORE
    SESSION_CREATE --> TOKEN
    
    SESSION_STORE --> COOKIE
    SESSION_STORE --> CSRF
    SESSION_STORE --> EXPIRY
    
    TOKEN --> ROLE_CHECK
    ROLE_CHECK --> PERM_CHECK
    PERM_CHECK --> DOC_PERMS
    PERM_CHECK --> FIELD_PERMS
```

**Security Features:**
- JWT-based authentication
- OAuth 2.0 support
- Two-factor authentication (OTP)
- LDAP integration
- CSRF protection
- Role-based access control (RBAC)
- Document-level permissions
- Field-level security

### 5. Real-time Communication Architecture

```mermaid
graph LR
    subgraph "Client Side"
        BROWSER[Browser Client]
        SOCKETIO_CLIENT[Socket.IO Client]
    end
    
    subgraph "Server Side"
        SOCKETIO_SERVER[Socket.IO Server]
        REALTIME[Realtime Module]
        PUBSUB[Redis Pub/Sub]
    end
    
    subgraph "Event System"
        EMIT[Emit Event]
        SUBSCRIBE[Subscribe]
        BROADCAST[Broadcast]
        ROOM[Room Management]
    end
    
    BROWSER --> SOCKETIO_CLIENT
    SOCKETIO_CLIENT --> SOCKETIO_SERVER
    SOCKETIO_SERVER --> REALTIME
    REALTIME --> PUBSUB
    
    REALTIME --> EMIT
    REALTIME --> SUBSCRIBE
    REALTIME --> BROADCAST
    REALTIME --> ROOM
```

### 6. Background Job Architecture

```mermaid
graph TB
    subgraph "Job Enqueueing"
        APP[Application Code]
        ENQUEUE[frappe.enqueue]
        SCHEDULER[Scheduled Jobs]
    end
    
    subgraph "RQ (Redis Queue)"
        REDIS_QUEUE[Redis Queue]
        DEFAULT_Q[default queue]
        SHORT_Q[short queue]
        LONG_Q[long queue]
    end
    
    subgraph "Workers"
        WORKER1[Worker 1]
        WORKER2[Worker 2]
        WORKERN[Worker N]
    end
    
    subgraph "Job Execution"
        EXECUTE[Execute Job]
        SUCCESS[Success Handler]
        FAILURE[Failure Handler]
        RETRY[Retry Logic]
    end
    
    APP --> ENQUEUE
    SCHEDULER --> ENQUEUE
    
    ENQUEUE --> REDIS_QUEUE
    REDIS_QUEUE --> DEFAULT_Q
    REDIS_QUEUE --> SHORT_Q
    REDIS_QUEUE --> LONG_Q
    
    DEFAULT_Q --> WORKER1
    SHORT_Q --> WORKER2
    LONG_Q --> WORKERN
    
    WORKER1 --> EXECUTE
    WORKER2 --> EXECUTE
    WORKERN --> EXECUTE
    
    EXECUTE --> SUCCESS
    EXECUTE --> FAILURE
    FAILURE --> RETRY
```

## Data Flow Architecture

### Request-Response Flow

```mermaid
sequenceDiagram
    participant Client
    participant NGINX
    participant WSGI
    participant Handler
    participant Auth
    participant API
    participant Model
    participant Database
    participant Cache
    
    Client->>NGINX: HTTP Request
    NGINX->>WSGI: Forward Request
    WSGI->>Handler: Route Request
    Handler->>Auth: Authenticate
    Auth->>Cache: Check Session
    Cache-->>Auth: Session Data
    Auth-->>Handler: Auth Context
    Handler->>API: Execute API Call
    API->>Model: Document Operation
    Model->>Cache: Check Cache
    Cache-->>Model: Cache Miss
    Model->>Database: Query Data
    Database-->>Model: Result Set
    Model->>Cache: Store in Cache
    Model-->>API: Document Data
    API-->>Handler: Response Data
    Handler->>WSGI: Build Response
    WSGI->>NGINX: HTTP Response
    NGINX->>Client: Return Response
```

### Document Lifecycle Flow

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Document
    participant Validator
    participant Hooks
    participant Workflow
    participant Database
    participant Events
    
    User->>API: Create/Update Document
    API->>Document: Initialize/Load
    Document->>Validator: Validate Fields
    Validator-->>Document: Validation OK
    Document->>Hooks: Before Save
    Hooks-->>Document: Continue
    Document->>Workflow: Check Workflow
    Workflow-->>Document: State Valid
    Document->>Database: Save Transaction
    Database-->>Document: Commit OK
    Document->>Hooks: After Save
    Document->>Events: Emit Events
    Events->>Background: Queue Jobs
    Document-->>API: Success
    API-->>User: Response
```

## Technology Stack Details

### Backend Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.10+ | Core application logic |
| Web Framework | Werkzeug | WSGI application server |
| ORM | Custom Document Model | Metadata-driven data access |
| Query Builder | PyPika | SQL query construction |
| Database Drivers | mysqlclient, psycopg2, sqlite3 | Database connectivity |
| Validation | RestrictedPython | Safe Python execution |
| Template Engine | Jinja2 | Server-side templating |
| Task Queue | RQ (Redis Queue) | Background job processing |
| Caching | Redis | Session, cache, pub/sub |
| Search | Whoosh | Full-text search indexing |
| PDF Generation | WeasyPrint | Report generation |
| Authentication | PyJWT, OAuth | Security |

### Frontend Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | Vue 3 | UI framework |
| State Management | Pinia, Vuex | Application state |
| UI Components | Bootstrap 4.6 | UI toolkit |
| Charts | Frappe Charts | Data visualization |
| Data Tables | Frappe DataTable | Grid component |
| Editor | Quill, EditorJS | Rich text editing |
| Build Tool | esbuild | Asset bundling |
| Real-time | Socket.IO Client | WebSocket communication |

### Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Server | NGINX/Gunicorn | HTTP server |
| Database | MariaDB 10.3+ | Primary database |
| Cache | Redis 6.0+ | Caching layer |
| Queue | Redis Queue | Background jobs |
| Process Manager | Supervisor/systemd | Service management |
| Container | Docker | Containerization |

## Key Design Patterns

### 1. Metadata-Driven Development
- **Pattern**: DocType definitions drive UI, API, and database schema
- **Benefit**: Rapid application development without code
- **Implementation**: JSON-based DocType definitions

### 2. Document-Oriented ORM
- **Pattern**: Documents as first-class objects with lifecycle hooks
- **Benefit**: Consistent data access patterns
- **Implementation**: `Document` base class with hooks

### 3. Plugin Architecture
- **Pattern**: Apps extend framework functionality
- **Benefit**: Modular, extensible architecture
- **Implementation**: Hooks and app structure

### 4. Event-Driven Processing
- **Pattern**: Hooks trigger on document lifecycle events
- **Benefit**: Decoupled business logic
- **Implementation**: `before_save`, `after_insert`, etc.

### 5. Multi-Tenancy
- **Pattern**: Site-based isolation
- **Benefit**: Multiple applications on single deployment
- **Implementation**: Site context management

## Security Architecture

### Defense in Depth

```mermaid
graph TB
    subgraph "Layer 1: Network Security"
        FIREWALL[Firewall]
        SSL[SSL/TLS]
        RATE_LIMIT[Rate Limiting]
    end
    
    subgraph "Layer 2: Application Security"
        CSRF_PROT[CSRF Protection]
        XSS_PROT[XSS Prevention]
        SQL_INJ[SQL Injection Prevention]
    end
    
    subgraph "Layer 3: Authentication"
        AUTH_LAYER[Authentication Layer]
        TWO_FA_LAYER[2FA]
        SESSION_SEC[Session Security]
    end
    
    subgraph "Layer 4: Authorization"
        RBAC[Role-Based Access]
        DOC_LEVEL[Document Permissions]
        FIELD_LEVEL[Field Permissions]
    end
    
    subgraph "Layer 5: Data Security"
        ENCRYPTION[Password Encryption]
        AUDIT[Audit Logging]
        BACKUP[Backups]
    end
    
    FIREWALL --> SSL
    SSL --> RATE_LIMIT
    RATE_LIMIT --> CSRF_PROT
    CSRF_PROT --> XSS_PROT
    XSS_PROT --> SQL_INJ
    SQL_INJ --> AUTH_LAYER
    AUTH_LAYER --> TWO_FA_LAYER
    TWO_FA_LAYER --> SESSION_SEC
    SESSION_SEC --> RBAC
    RBAC --> DOC_LEVEL
    DOC_LEVEL --> FIELD_LEVEL
    FIELD_LEVEL --> ENCRYPTION
    ENCRYPTION --> AUDIT
    AUDIT --> BACKUP
```

## Performance Optimization Strategies

1. **Caching Layers**
   - Redis-based distributed cache
   - Client-side cache
   - Query result caching
   - Metadata caching

2. **Database Optimization**
   - Query builder optimization
   - Indexing strategies
   - Connection pooling
   - Read replicas support

3. **Asset Optimization**
   - JavaScript/CSS bundling and minification
   - Image optimization
   - CDN support
   - Lazy loading

4. **Background Processing**
   - Async job execution
   - Queue-based processing
   - Scheduled task execution

## Scalability Architecture

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[Load Balancer]
    end
    
    subgraph "Application Tier"
        APP1[App Server 1]
        APP2[App Server 2]
        APPN[App Server N]
    end
    
    subgraph "Background Workers"
        WORKER1[Worker 1]
        WORKER2[Worker 2]
        WORKERN[Worker N]
    end
    
    subgraph "Cache Tier"
        REDIS_MASTER[Redis Master]
        REDIS_REPLICA[Redis Replica]
    end
    
    subgraph "Database Tier"
        DB_MASTER[DB Master]
        DB_SLAVE1[DB Replica 1]
        DB_SLAVE2[DB Replica 2]
    end
    
    LB --> APP1
    LB --> APP2
    LB --> APPN
    
    APP1 --> REDIS_MASTER
    APP2 --> REDIS_MASTER
    APPN --> REDIS_MASTER
    
    REDIS_MASTER --> REDIS_REPLICA
    
    APP1 --> DB_MASTER
    APP1 --> DB_SLAVE1
    APP2 --> DB_MASTER
    APP2 --> DB_SLAVE2
    APPN --> DB_MASTER
    
    WORKER1 --> REDIS_MASTER
    WORKER2 --> REDIS_MASTER
    WORKERN --> REDIS_MASTER
    
    WORKER1 --> DB_MASTER
    WORKER2 --> DB_MASTER
    WORKERN --> DB_MASTER
```

## Integration Boundaries

### External Service Integration Points

1. **Email Services**: SMTP, IMAP integration
2. **OAuth Providers**: Google, Facebook, GitHub, Custom
3. **Payment Gateways**: Stripe, PayPal, Razorpay
4. **Cloud Storage**: S3, Google Cloud Storage, Azure Blob
5. **SMS Gateways**: Twilio, custom providers
6. **Webhooks**: Outbound webhook support
7. **APIs**: RESTful API exposure and consumption
8. **LDAP/AD**: Enterprise authentication
9. **Search Engines**: External search integration

## Deployment Architecture

### Typical Production Deployment

```mermaid
graph TB
    subgraph "Internet"
        USERS[End Users]
    end
    
    subgraph "Edge Layer"
        CDN[CDN]
        DNS[DNS]
    end
    
    subgraph "Reverse Proxy Layer"
        NGINX_LB[NGINX Load Balancer]
    end
    
    subgraph "Application Layer"
        GUNICORN1[Gunicorn Worker 1]
        GUNICORN2[Gunicorn Worker 2]
        SOCKETIO_SRV[Socket.IO Server]
    end
    
    subgraph "Background Layer"
        RQ_WORKER1[RQ Worker 1]
        RQ_WORKER2[RQ Worker 2]
        SCHEDULER_SRV[Scheduler]
    end
    
    subgraph "Data Layer"
        MARIADB_MASTER[MariaDB Master]
        MARIADB_SLAVE[MariaDB Slave]
        REDIS_SRV[Redis]
        FILE_STORAGE[File Storage]
    end
    
    USERS --> CDN
    USERS --> DNS
    CDN --> NGINX_LB
    DNS --> NGINX_LB
    
    NGINX_LB --> GUNICORN1
    NGINX_LB --> GUNICORN2
    NGINX_LB --> SOCKETIO_SRV
    
    GUNICORN1 --> REDIS_SRV
    GUNICORN2 --> REDIS_SRV
    SOCKETIO_SRV --> REDIS_SRV
    
    GUNICORN1 --> MARIADB_MASTER
    GUNICORN2 --> MARIADB_MASTER
    GUNICORN1 --> MARIADB_SLAVE
    GUNICORN2 --> MARIADB_SLAVE
    
    RQ_WORKER1 --> REDIS_SRV
    RQ_WORKER2 --> REDIS_SRV
    SCHEDULER_SRV --> REDIS_SRV
    
    RQ_WORKER1 --> MARIADB_MASTER
    RQ_WORKER2 --> MARIADB_MASTER
    
    GUNICORN1 --> FILE_STORAGE
    GUNICORN2 --> FILE_STORAGE
    
    MARIADB_MASTER --> MARIADB_SLAVE
```

## Monitoring & Observability

### Key Metrics

1. **Application Metrics**
   - Request rate and latency
   - Error rates
   - Document operation rates
   - Background job metrics

2. **Database Metrics**
   - Query performance
   - Connection pool usage
   - Slow query log
   - Replication lag

3. **Cache Metrics**
   - Hit/miss ratio
   - Memory usage
   - Key eviction rate

4. **System Metrics**
   - CPU, memory, disk usage
   - Network I/O
   - Process counts

### Observability Tools

- **Logging**: Python logging, structured logs
- **Tracing**: Request ID tracking, distributed tracing support
- **Monitoring**: Prometheus, Grafana integration
- **Error Tracking**: Sentry integration

## Summary

Frappe Framework provides a comprehensive, production-ready platform for building enterprise applications. Its metadata-driven approach, combined with powerful ORM, REST API, and background processing capabilities, enables rapid development while maintaining scalability and security.

**Key Strengths:**
- Metadata-driven development
- Automatic API generation
- Built-in admin interface
- Comprehensive permission system
- Multi-database support
- Real-time capabilities
- Extensible plugin architecture

**Ideal Use Cases:**
- ERP systems
- CRM applications
- Custom business applications
- SaaS platforms
- Internal tools and dashboards
