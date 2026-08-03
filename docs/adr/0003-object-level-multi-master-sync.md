# Object-Level Multi-Master Sync

Finance Own will use object-level multi-master synchronization, with the .NET cloud service acting as a coordination center rather than the only source of truth. PC local SQLite can produce authoritative offline changes, mobile can queue lightweight offline entries, and PostgreSQL stores cloud replicas, versions, sync batches, and conflicts without silently overwriting clients.

The sync policy is bidirectional: non-conflicting object changes merge automatically, while true conflicts such as same-field edits or delete-versus-edit cases enter an explicit resolution flow rather than allowing PC, mobile, Web, or cloud to blindly overwrite another side.

Full conflict resolution belongs to PC and Web in the first version. Mobile shows conflict status and allows users to defer complex resolution.
