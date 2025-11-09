# Frappe Framework - Formal Specifications & Architecture Documentation

This directory contains comprehensive technical architecture documentation and formal Z++ specifications for the Frappe Framework.

## Overview

The Frappe Framework is a full-stack, metadata-driven, low-code web framework written in Python and JavaScript. This documentation provides:

1. **Architecture Documentation** - High-level system architecture with Mermaid diagrams
2. **Formal Z++ Specifications** - Rigorous mathematical specifications of the system

## Contents

### Architecture Documentation

- **[architecture_overview.md](architecture_overview.md)** - Complete system architecture overview
  - System component diagrams
  - Data flow diagrams
  - Technology stack details
  - Design patterns
  - Security architecture
  - Deployment architecture
  - Performance and scalability considerations

### Formal Specifications (Z++)

The formal specifications are organized into modular files:

1. **[data_model.zpp](../formal-specs/data_model.zpp)** - Data Layer Formalization
   - DocType metadata schemas
   - Document instance schemas
   - Field definitions and validation
   - Naming rules
   - Link validation
   - Data integrity constraints

2. **[system_state.zpp](../formal-specs/system_state.zpp)** - System State Schemas
   - System configuration
   - Database connection state
   - Session management
   - Cache layer
   - Request context
   - Background job queues
   - Multi-site state
   - Performance metrics

3. **[operations.zpp](../formal-specs/operations.zpp)** - Operation Specifications
   - Authentication operations (Login, Logout, ValidateSession)
   - Document CRUD operations (Create, Read, Update, Delete)
   - Document lifecycle (Submit, Cancel)
   - Query operations (GetList, GetValue)
   - Transaction management (Begin, Commit, Rollback, Savepoints)
   - Background job operations (Enqueue, Execute)
   - API operations

4. **[integrations.zpp](../formal-specs/integrations.zpp)** - External Integration Contracts
   - REST API contracts (v1, v2)
   - Webhook integration
   - Email integration (SMTP/IMAP)
   - OAuth integration
   - External API calls
   - Real-time Socket.IO events

## Key Architectural Components

### Core Layers

```
┌─────────────────────────────────────────────────────┐
│              Presentation Layer                      │
│  (Web Browser, Mobile Client, API Clients)          │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│             Application Layer                        │
│  (WSGI, Request Handler, REST API, Auth)            │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│           Business Logic Layer                       │
│  (Document Model, Workflow, Permissions, Hooks)     │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│            Data Access Layer                         │
│  (Query Builder, Database Abstraction)              │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│          Storage & Cache Layer                       │
│  (MariaDB/Postgres, Redis, Files, Search)           │
└─────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.10+
- Werkzeug (WSGI)
- PyPika (Query Builder)
- MariaDB/PostgreSQL/SQLite
- Redis (Caching & Queue)
- RQ (Background Jobs)

**Frontend:**
- Vue 3
- Bootstrap 4.6
- Socket.IO
- esbuild

## Understanding the Formal Specifications

### Z++ Notation

The formal specifications use Z++ notation, an extension of Z specification language. Key concepts:

- **Schemas**: Define state spaces and operations
- **`Δ` (Delta)**: Indicates state change (before/after)
- **`Ξ` (Xi)**: Indicates read-only operation (no state change)
- **`?` suffix**: Input parameter
- **`!` suffix**: Output parameter
- **`where` clause**: Specifies constraints and invariants
- **`∈`**: Set membership
- **`⇒`**: Logical implication
- **`∧`**: Logical AND
- **`∨`**: Logical OR
- **`∀`**: Universal quantification (for all)
- **`∃`**: Existential quantification (there exists)

### Reading the Specifications

1. Start with **data_model.zpp** to understand the core data structures
2. Read **system_state.zpp** to understand the runtime state
3. Study **operations.zpp** to see how operations transform state
4. Review **integrations.zpp** to understand external contracts

### Example: Document Creation

From `operations.zpp`, the CreateDocument operation:

```z++
schema CreateDocument
  ΔSystemState                    // State changes
  doctype?: DocTypeName          // Input: document type
  field_values?: map[FieldName, Any]  // Input: field values
  owner?: UserName               // Input: owner
  
  document!: Document            // Output: created document
  success!: Bool                 // Output: success flag
  error!: Option[seq Char]       // Output: error message
where
  // Pre-conditions and post-conditions...
```

This specifies:
- Input parameters (doctype, field_values, owner)
- Output parameters (document, success, error)
- State transformation (ΔSystemState)
- Constraints and invariants in the `where` clause

## Key Invariants

### Data Integrity

1. **Unique Document Names**: Within a DocType, all document names are unique
2. **Referential Integrity**: Link fields reference existing documents
3. **Field Validation**: All field values match their field type definitions
4. **Required Fields**: Required fields must have non-null values
5. **Permission Checks**: Operations respect role-based permissions

### System State

1. **Session Validity**: Active sessions are not expired
2. **Database Connection**: Database is always connected during operations
3. **Transaction Atomicity**: Transactions are atomic (all or nothing)
4. **Cache Consistency**: Cache entries are consistent with database
5. **Queue Bounds**: Job queues respect size limits

## Design Patterns

### Metadata-Driven Development

DocType definitions drive:
- Database schema generation
- UI form generation
- API endpoint generation
- Permission rules
- Validation logic

### Event-Driven Architecture

Document lifecycle hooks:
- `before_insert`, `after_insert`
- `before_save`, `after_save`
- `before_submit`, `after_submit`
- `before_cancel`, `after_cancel`
- `before_delete`, `after_delete`

### Multi-Tenancy

Site-based isolation:
- Each site has its own database
- Shared codebase, separate data
- Site-specific configuration

## Security Architecture

### Defense Layers

1. **Network Security**: SSL/TLS, Rate limiting
2. **Application Security**: CSRF protection, XSS prevention, SQL injection prevention
3. **Authentication**: JWT, OAuth, 2FA
4. **Authorization**: Role-based access control (RBAC)
5. **Data Security**: Password encryption, audit logging

### Permission Model

```
User → Roles → Permissions → Documents
```

Permissions are evaluated at:
- DocType level (can read/write/create/delete)
- Document level (ownership, match conditions)
- Field level (read-only fields)

## Performance Considerations

### Caching Strategy

1. **Metadata Cache**: DocType definitions cached in Redis
2. **Session Cache**: User sessions cached for fast lookup
3. **Query Cache**: Frequently accessed data cached
4. **Client Cache**: Browser-side caching for static assets

### Database Optimization

1. **Query Builder**: Optimized SQL generation via PyPika
2. **Connection Pooling**: Reuse database connections
3. **Indexing**: Automatic index creation for link fields
4. **Batch Operations**: Bulk insert/update support

### Background Jobs

Long-running tasks executed asynchronously:
- Email sending
- Report generation
- Data import/export
- Scheduled tasks

## Integration Points

### Inbound

1. **REST API**: HTTP requests for CRUD operations
2. **Webhooks**: Incoming webhook events
3. **Email**: IMAP for email integration
4. **OAuth**: Third-party authentication

### Outbound

1. **REST API**: Calls to external services
2. **Webhooks**: Event notifications to external systems
3. **Email**: SMTP for sending emails
4. **Real-time**: Socket.IO for client updates

## Usage Guidelines

### For Developers

- Use these specifications to understand system contracts
- Refer to invariants when implementing new features
- Ensure operations maintain system invariants
- Follow established patterns for consistency

### For Architects

- Use architecture diagrams for system design
- Understand integration boundaries
- Plan scalability based on architecture
- Consider security layers in design

### For Auditors

- Verify implementation against specifications
- Check that invariants are maintained
- Validate security controls
- Review integration contracts

## Validation

The formal specifications can be used to:

1. **Verify Correctness**: Prove operations maintain invariants
2. **Test Generation**: Generate test cases from specifications
3. **Documentation**: Serve as precise documentation
4. **Code Review**: Reference during code reviews
5. **Refactoring**: Ensure behavior preservation

## Limitations

### Abstractions

The specifications abstract:
- Python implementation details
- Database-specific optimizations
- Network communication details
- UI rendering logic
- Specific error handling strategies

### Out of Scope

Not specified:
- Client-side UI components
- CSS styling
- Browser-specific behavior
- Development tools
- Deployment scripts

## Future Extensions

Potential additions:
- Workflow state machines (formal)
- Permission calculation algorithm (complete)
- Cache invalidation strategies (detailed)
- Query optimization rules (formal)
- Distributed transaction protocols

## References

### Frappe Documentation

- [Official Documentation](https://docs.frappe.io/framework)
- [GitHub Repository](https://github.com/frappe/frappe)
- [Frappe School](https://frappe.school)

### Z Notation

- *The Z Notation: A Reference Manual* by J.M. Spivey
- *Using Z: Specification, Refinement, and Proof* by Jim Woodcock and Jim Davies

### Related Technologies

- [PyPika Documentation](https://pypika.readthedocs.io/)
- [Werkzeug Documentation](https://werkzeug.palletsprojects.com/)
- [Redis Documentation](https://redis.io/documentation)
- [MariaDB Documentation](https://mariadb.com/kb/en/)

## Contributing

When updating these specifications:

1. Maintain consistency with actual implementation
2. Update all affected schemas when making changes
3. Ensure invariants remain valid
4. Add examples for complex operations
5. Document any deviations from implementation

## License

These specifications are derived from the Frappe Framework, which is licensed under MIT License.

---

**Generated**: November 2024  
**Version**: Based on Frappe Framework v16.0.0-dev  
**Status**: Complete formal specification of core architecture
