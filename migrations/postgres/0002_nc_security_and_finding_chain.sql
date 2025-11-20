-- 0002_nc_security_and_finding_chain.sql
-- DM-003 security, finding, audit, and event tables plus partition & retention helpers

-- 6.2 user
CREATE TABLE IF NOT EXISTS nc."user" (
  id           text PRIMARY KEY,
  account_id   text NOT NULL REFERENCES nc.account(id),
  email        text NOT NULL,
  display_name text,
  auth_provider nc.auth_provider NOT NULL,
  status       nc.status_user NOT NULL DEFAULT 'INVITED',
  mfa_enabled  boolean NOT NULL DEFAULT false,
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now(),
  is_deleted   boolean NOT NULL DEFAULT false
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_user_email ON nc."user"(account_id, lower(email));
ALTER TABLE nc."user" ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_user_tenant ON nc."user" USING (account_id = nc.current_account_id());

-- 6.3 role
CREATE TABLE IF NOT EXISTS nc.role (
  id           text PRIMARY KEY,
  account_id   text NOT NULL REFERENCES nc.account(id),
  name         text NOT NULL,
  permissions  jsonb NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_role_name ON nc.role(account_id, name);
ALTER TABLE nc.role ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_role_tenant ON nc.role USING (account_id = nc.current_account_id());

-- 6.4 role_assignment
CREATE TABLE IF NOT EXISTS nc.role_assignment (
  id           text PRIMARY KEY,
  account_id   text NOT NULL REFERENCES nc.account(id),
  user_id      text NOT NULL REFERENCES nc."user"(id),
  role_id      text NOT NULL REFERENCES nc.role(id),
  created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_role_assignment ON nc.role_assignment(account_id, user_id, role_id);
ALTER TABLE nc.role_assignment ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_role_assignment_tenant ON nc.role_assignment USING (account_id = nc.current_account_id());

-- 6.5 cloud_account (SCD2)
CREATE TABLE IF NOT EXISTS nc.cloud_account (
  id           text PRIMARY KEY,
  account_id   text NOT NULL REFERENCES nc.account(id),
  provider     nc.provider NOT NULL,
  external_ref text NOT NULL,
  name         text,
  linked_at    timestamptz NOT NULL,
  valid_from   timestamptz NOT NULL,
  valid_to     timestamptz,
  is_current   boolean NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_cloud_acct_current
  ON nc.cloud_account(account_id, provider, external_ref) WHERE is_current = true;
CREATE INDEX IF NOT EXISTS ix_cloud_acct_hist
  ON nc.cloud_account(account_id, provider, external_ref, valid_from);
ALTER TABLE nc.cloud_account ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_cloud_account_tenant ON nc.cloud_account USING (account_id = nc.current_account_id());

-- 6.7 asset (SCD2)
CREATE TABLE IF NOT EXISTS nc.asset (
  id               text PRIMARY KEY,
  account_id       text NOT NULL REFERENCES nc.account(id),
  cloud_account_id text REFERENCES nc.cloud_account(id),
  urn              text NOT NULL,
  type             text NOT NULL,
  region           text,
  tags             jsonb,
  state            text NOT NULL CHECK (state IN ('ACTIVE','DELETED')),
  discovered_at    timestamptz NOT NULL,
  valid_from       timestamptz NOT NULL,
  valid_to         timestamptz,
  is_current       boolean NOT NULL,
  created_at       timestamptz NOT NULL DEFAULT now(),
  updated_at       timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_asset_current ON nc.asset(account_id, urn) WHERE is_current = true;
CREATE INDEX IF NOT EXISTS ix_asset_lookup ON nc.asset(account_id, type, is_current, region);
ALTER TABLE nc.asset ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_asset_tenant ON nc.asset USING (account_id = nc.current_account_id());

-- 6.13 control (SCD2)
CREATE TABLE IF NOT EXISTS nc.control (
  id          text PRIMARY KEY,
  key         text NOT NULL,
  title       text NOT NULL,
  description text NOT NULL,
  severity    nc.severity NOT NULL,
  category    text NOT NULL,
  rationale   text,
  "references"  jsonb,
  valid_from  timestamptz NOT NULL,
  valid_to    timestamptz,
  is_current  boolean NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_control_current ON nc.control(key) WHERE is_current = true;

-- 6.14 policy (SCD2 with embedded controls)
CREATE TABLE IF NOT EXISTS nc.policy (
  id            text PRIMARY KEY,
  account_id    text NOT NULL REFERENCES nc.account(id),
  name          text NOT NULL,
  controls      jsonb NOT NULL,  -- array of { key, weight, params }
  version_label text NOT NULL,
  valid_from    timestamptz NOT NULL,
  valid_to      timestamptz,
  is_current    boolean NOT NULL,
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_policy_name_current
  ON nc.policy(account_id, name) WHERE is_current = true;
ALTER TABLE nc.policy ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_policy_tenant ON nc.policy USING (account_id = nc.current_account_id());

-- 6.12 scan
CREATE TABLE IF NOT EXISTS nc.scan (
  id             text PRIMARY KEY,
  account_id     text NOT NULL REFERENCES nc.account(id),
  scope          jsonb NOT NULL,
  status         nc.status_scan NOT NULL DEFAULT 'QUEUED',
  started_at     timestamptz,
  ended_at       timestamptz,
  control_set_id text REFERENCES nc.policy(id),
  created_at     timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_scan_status ON nc.scan(account_id, status, started_at);
ALTER TABLE nc.scan ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_scan_tenant ON nc.scan USING (account_id = nc.current_account_id());

-- 6.15 finding
CREATE TABLE IF NOT EXISTS nc.finding (
  id             text PRIMARY KEY,
  account_id     text NOT NULL REFERENCES nc.account(id),
  scan_id        text NOT NULL,
  control_key    text NOT NULL,
  asset_id       text REFERENCES nc.asset(id),
  status         nc.status_finding NOT NULL DEFAULT 'OPEN',
  severity       nc.severity NOT NULL,
  evidence_score numeric(5,2),
  summary        text NOT NULL,
  details        jsonb,
  first_seen_at  timestamptz NOT NULL,
  last_seen_at   timestamptz NOT NULL,
  created_at     timestamptz NOT NULL DEFAULT now()
);
-- Zero downtime FK pattern
ALTER TABLE nc.finding
  ADD CONSTRAINT fk_finding_scan
  FOREIGN KEY (scan_id) REFERENCES nc.scan(id) NOT VALID;
ALTER TABLE nc.finding VALIDATE CONSTRAINT fk_finding_scan;

CREATE INDEX IF NOT EXISTS ix_finding_open
  ON nc.finding(account_id, status, severity, last_seen_at DESC);
CREATE INDEX IF NOT EXISTS ix_finding_asset ON nc.finding(asset_id);
ALTER TABLE nc.finding ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_finding_tenant ON nc.finding USING (account_id = nc.current_account_id());

-- 6.16 evidence
CREATE TABLE IF NOT EXISTS nc.evidence (
  id           text PRIMARY KEY,
  account_id   text NOT NULL REFERENCES nc.account(id),
  finding_id   text NOT NULL REFERENCES nc.finding(id),
  content_uri  text NOT NULL,
  content_type text NOT NULL,
  hash_sha256  text NOT NULL,
  captured_at  timestamptz NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_evidence_finding ON nc.evidence(finding_id);
ALTER TABLE nc.evidence ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_evidence_tenant ON nc.evidence USING (account_id = nc.current_account_id());

-- 6.17 remediation
CREATE TABLE IF NOT EXISTS nc.remediation (
  id           text PRIMARY KEY,
  account_id   text NOT NULL REFERENCES nc.account(id),
  finding_id   text NOT NULL REFERENCES nc.finding(id),
  plan         jsonb NOT NULL,
  executor     nc.exec_type NOT NULL,
  status       nc.status_job NOT NULL DEFAULT 'QUEUED',
  started_at   timestamptz,
  completed_at timestamptz,
  created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_remediation_finding ON nc.remediation(finding_id, status);
ALTER TABLE nc.remediation ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_remediation_tenant ON nc.remediation USING (account_id = nc.current_account_id());

-- 6.18 ticket
CREATE TABLE IF NOT EXISTS nc.ticket (
  id           text PRIMARY KEY,
  account_id   text NOT NULL REFERENCES nc.account(id),
  finding_id   text NOT NULL REFERENCES nc.finding(id),
  provider     nc.ticket_provider NOT NULL,
  external_key text NOT NULL,
  url          text NOT NULL,
  status       text NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_ticket_ext ON nc.ticket(provider, external_key);
ALTER TABLE nc.ticket ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_ticket_tenant ON nc.ticket USING (account_id = nc.current_account_id());

-- 6.19 integration (SCD2)
CREATE TABLE IF NOT EXISTS nc.integration (
  id          text PRIMARY KEY,
  account_id  text NOT NULL REFERENCES nc.account(id),
  type        nc.integration_type NOT NULL,
  config      jsonb NOT NULL,
  status      nc.status_toggle NOT NULL DEFAULT 'ACTIVE',
  valid_from  timestamptz NOT NULL,
  valid_to    timestamptz,
  is_current  boolean NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_integration_current
  ON nc.integration(account_id, type) WHERE is_current = true;
ALTER TABLE nc.integration ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_integration_tenant ON nc.integration USING (account_id = nc.current_account_id());

-- 6.20 notification
CREATE TABLE IF NOT EXISTS nc.notification (
  id           text PRIMARY KEY,
  account_id   text NOT NULL REFERENCES nc.account(id),
  channel      nc.integration_type NOT NULL,
  template_key text NOT NULL,
  payload      jsonb NOT NULL,
  sent_at      timestamptz,
  created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_notification_time ON nc.notification(account_id, sent_at DESC);
ALTER TABLE nc.notification ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_notification_tenant ON nc.notification USING (account_id = nc.current_account_id());

-- 6.21 audit_log (monthly partitions)
CREATE TABLE IF NOT EXISTS nc.audit_log (
  id            text NOT NULL,
  account_id    text NOT NULL REFERENCES nc.account(id),
  actor_user_id text,
  action        text NOT NULL,
  target        jsonb NOT NULL,
  ip            text,
  occurred_at   timestamptz NOT NULL,
  PRIMARY KEY (id, occurred_at)
) PARTITION BY RANGE (occurred_at);

CREATE TABLE IF NOT EXISTS nc.audit_log_2025_10
  PARTITION OF nc.audit_log FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

CREATE INDEX IF NOT EXISTS ix_audit_log_time_2025_10
  ON nc.audit_log_2025_10(account_id, occurred_at DESC);

ALTER TABLE nc.audit_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_audit_log_tenant ON nc.audit_log USING (account_id = nc.current_account_id());

-- 6.22 job
CREATE TABLE IF NOT EXISTS nc.job (
  id         text PRIMARY KEY,
  account_id text NOT NULL REFERENCES nc.account(id),
  type       text NOT NULL,
  status     nc.status_job NOT NULL DEFAULT 'QUEUED',
  payload    jsonb NOT NULL,
  result     jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_job_status ON nc.job(account_id, status, created_at DESC);
ALTER TABLE nc.job ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_job_tenant ON nc.job USING (account_id = nc.current_account_id());

-- 6.23 event (monthly partitions)
CREATE TABLE IF NOT EXISTS nc.event (
  id              text NOT NULL,
  account_id      text NOT NULL REFERENCES nc.account(id),
  type            text NOT NULL,
  schema_version  int  NOT NULL,
  event_version   int  NOT NULL,
  occurred_at     timestamptz NOT NULL,
  payload         jsonb NOT NULL,
  checksum_sha256 text NOT NULL,
  PRIMARY KEY (id, occurred_at)
) PARTITION BY RANGE (occurred_at);

CREATE TABLE IF NOT EXISTS nc.event_2025_10
  PARTITION OF nc.event FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

CREATE INDEX IF NOT EXISTS ix_event_time_2025_10
  ON nc.event_2025_10(account_id, type, occurred_at DESC);

ALTER TABLE nc.event ENABLE ROW LEVEL SECURITY;
CREATE POLICY p_event_tenant ON nc.event USING (account_id = nc.current_account_id());

-- 8. Partition management
CREATE OR REPLACE PROCEDURE nc.ensure_month_partitions(month_start date)
LANGUAGE plpgsql AS $$
DECLARE next_start date := (month_start + INTERVAL '1 month')::date;
BEGIN
  EXECUTE format(
    'CREATE TABLE IF NOT EXISTS nc.audit_log_%s PARTITION OF nc.audit_log FOR VALUES FROM (%L) TO (%L)',
    to_char(month_start,'YYYY_MM'), month_start, next_start
  );
  EXECUTE format(
    'CREATE INDEX IF NOT EXISTS ix_audit_log_time_%s ON nc.audit_log_%s(account_id, occurred_at DESC)',
    to_char(month_start,'YYYY_MM'), to_char(month_start,'YYYY_MM')
  );

  EXECUTE format(
    'CREATE TABLE IF NOT EXISTS nc.event_%s PARTITION OF nc.event FOR VALUES FROM (%L) TO (%L)',
    to_char(month_start,'YYYY_MM'), month_start, next_start
  );
  EXECUTE format(
    'CREATE INDEX IF NOT EXISTS ix_event_time_%s ON nc.event_%s(account_id, type, occurred_at DESC)',
    to_char(month_start,'YYYY_MM'), to_char(month_start,'YYYY_MM')
  );
END$$;

-- 14. Retention enforcement jobs
CREATE OR REPLACE PROCEDURE nc.purge_rc3_90d()
LANGUAGE plpgsql AS $$
BEGIN
  DELETE FROM nc.document_chunk dc
  USING nc.source_document sd
  WHERE dc.source_document_id = sd.id
    AND sd.retention_class = 'RC3'
    AND sd.collected_at < now() - INTERVAL '90 days';

  DELETE FROM nc.source_document sd
  WHERE sd.retention_class = 'RC3'
    AND sd.collected_at < now() - INTERVAL '90 days';
END$$;

CREATE OR REPLACE PROCEDURE nc.purge_rc2_2y()
LANGUAGE plpgsql AS $$
BEGIN
  DELETE FROM nc.scan s
  WHERE s.account_id IS NOT NULL
    AND s.created_at < now() - INTERVAL '730 days';

  DELETE FROM nc.asset a
  WHERE a.is_current = false
    AND a.valid_to < now() - INTERVAL '730 days';
END$$;

CREATE OR REPLACE PROCEDURE nc.purge_rc4_24h()
LANGUAGE plpgsql AS $$
BEGIN
  DELETE FROM nc.notification n
  WHERE n.sent_at IS NOT NULL
    AND n.sent_at < now() - INTERVAL '24 hours';

  DELETE FROM nc.job j
  WHERE j.created_at < now() - INTERVAL '24 hours'
    AND j.status IN ('COMPLETED','FAILED');
END$$;

-- Re-run tenant-context enforcement triggers to include all tenant tables
DO $$
DECLARE t regclass;
BEGIN
  FOR t IN
    SELECT c.oid
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'nc'
      AND c.relkind = 'r'
      AND c.relname IN ('user','role','role_assignment','cloud_account','data_source',
                        'asset','source_document','document_chunk','embedding_ref',
                        'ingestion_job','scan','policy','finding','evidence','remediation',
                        'ticket','integration','notification','audit_log','job','event')
  LOOP
    EXECUTE format('DROP TRIGGER IF EXISTS trg_tenant_guard ON %s', t);
    EXECUTE format($f$
      CREATE TRIGGER trg_tenant_guard
      BEFORE INSERT OR UPDATE ON %s
      FOR EACH ROW EXECUTE FUNCTION nc.enforce_tenant_context()
    $f$, t);
  END LOOP;
END$$;
