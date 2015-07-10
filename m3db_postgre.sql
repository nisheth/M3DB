--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: hadoop_fdw; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS hadoop_fdw WITH SCHEMA public;


--
-- Name: EXTENSION hadoop_fdw; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION hadoop_fdw IS 'Hadoop Foreign Data Wrapper';


--
-- Name: hadoop_server; Type: SERVER; Schema: -; Owner: 
--

CREATE SERVER hadoop_server FOREIGN DATA WRAPPER hadoop_fdw OPTIONS (
    address '127.0.0.1',
    port '10000'
);


ALTER SERVER hadoop_server OWNER TO postgres;

--
-- Name: USER MAPPING public SERVER hadoop_server; Type: USER MAPPING; Schema: -; Owner: 
--

CREATE USER MAPPING FOR public SERVER hadoop_server;


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: abundance_profile; Type: TABLE; Schema: public; Owner: ; Tablespace: 
--

CREATE TABLE abundance_profile (
    profile_id integer NOT NULL,
    exp_id integer,
    sample_id integer,
    analysis_id integer,
    taxonomy_id integer,
    taxonomy_level character varying,
    taxonomy_name character varying,
    num_reads integer,
    score real,
    abundance real,
    avg real,
    status character varying(2),
    miscellaneous character varying
);


ALTER TABLE abundance_profile OWNER TO postgres ;

--
-- Name: abundance_profile_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: 
--

CREATE SEQUENCE abundance_profile_profile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE abundance_profile_profile_id_seq OWNER TO postgres ;

--
-- Name: abundance_profile_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: 
--

ALTER SEQUENCE abundance_profile_profile_id_seq OWNED BY abundance_profile.profile_id;


--
-- Name: analysis; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE analysis (
    analysis_id smallint NOT NULL,
    name character varying,
    description character varying,
    parameters character varying,
    comments character varying,
    refdb_id integer NOT NULL
);


ALTER TABLE analysis OWNER TO postgres;

--
-- Name: analysis_analysis_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE analysis_analysis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE analysis_analysis_id_seq OWNER TO postgres;

--
-- Name: analysis_analysis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE analysis_analysis_id_seq OWNED BY analysis.analysis_id;


--
-- Name: analysis_refdb_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE analysis_refdb_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE analysis_refdb_id_seq OWNER TO postgres;

--
-- Name: analysis_refdb_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE analysis_refdb_id_seq OWNED BY analysis.refdb_id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO postgres;

--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO postgres;

--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO postgres;

--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO postgres;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text NOT NULL,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL
);


ALTER TABLE django_admin_log OWNER TO postgres;

--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO postgres;

--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_session (
    id integer NOT NULL,
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO postgres;

--
-- Name: django_session_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_session_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_session_id_seq OWNER TO postgres;

--
-- Name: django_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_session_id_seq OWNED BY django_session.id;


--
-- Name: django_site; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE django_site OWNER TO postgres;

--
-- Name: experiment; Type: TABLE; Schema: public; Owner: ; Tablespace: 
--

CREATE TABLE experiment (
    exp_id integer NOT NULL,
    project_id integer,
    name character varying,
    date date,
    platform character varying,
    gene_region character varying,
    username character varying
);


ALTER TABLE experiment OWNER TO postgres ;

--
-- Name: experiment_exp_id_seq; Type: SEQUENCE; Schema: public; Owner: 
--

CREATE SEQUENCE experiment_exp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE experiment_exp_id_seq OWNER TO postgres ;

--
-- Name: experiment_exp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: 
--

ALTER SEQUENCE experiment_exp_id_seq OWNED BY experiment.exp_id;


--
-- Name: metadata; Type: TABLE; Schema: public; Owner: ; Tablespace: 
--

CREATE TABLE metadata (
    id integer NOT NULL,
    sample_id integer,
    name character varying,
    value character varying
);


ALTER TABLE metadata OWNER TO postgres ;

--
-- Name: metadata_id_seq; Type: SEQUENCE; Schema: public; Owner: 
--

CREATE SEQUENCE metadata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE metadata_id_seq OWNER TO postgres ;

--
-- Name: metadata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: 
--

ALTER SEQUENCE metadata_id_seq OWNED BY metadata.id;


--
-- Name: project; Type: TABLE; Schema: public; Owner: ; Tablespace: 
--

CREATE TABLE project (
    project_id integer NOT NULL,
    name character varying,
    pi_name character varying,
    e_mail character varying,
    description character varying,
    username character varying,
    authorized character varying
);


ALTER TABLE project OWNER TO postgres;

--
-- Name: project_project_id_seq; Type: SEQUENCE; Schema: public; Owner: 
--

CREATE SEQUENCE project_project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE project_project_id_seq OWNER TO postgres ;

--
-- Name: project_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: 
--

ALTER SEQUENCE project_project_id_seq OWNED BY project.project_id;


--
-- Name: read_assignment; Type: FOREIGN TABLE; Schema: public; Owner: ; Tablespace: 
--

CREATE FOREIGN TABLE read_assignment (
    exp_id integer,
    sample_id integer,
    read_id character varying,
    taxonomy_id integer,
    taxonomy_name character varying,
    taxonomy_level character varying,
    score real,
    analysis_id integer,
    status character varying,
    misc character varying
)
SERVER hadoop_server
OPTIONS (
    "table" 'm3db.read_assignment'
);


ALTER FOREIGN TABLE read_assignment OWNER TO postgres;

--
-- Name: reads; Type: FOREIGN TABLE; Schema: public; Owner: ; Tablespace: 
--

CREATE FOREIGN TABLE reads (
    exp_id integer,
    sample_id integer,
    read_id character varying,
    mee real,
    avgq real,
    read_length integer,
    overlap_flag character varying,
    read_desc character varying,
    hq_flag character varying,
    sequence character varying,
    quality_seq character varying,
    forward_read character varying,
    forward_qual character varying,
    reverse_read character varying,
    reverse_qual character varying
)
SERVER hadoop_server
OPTIONS (
    "table" 'm3db.reads'
);


ALTER FOREIGN TABLE reads OWNER TO postgres;

--
-- Name: ref_db; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE ref_db (
    refdb_id smallint NOT NULL,
    name character varying,
    description character varying,
    url character varying,
    version character varying
);


ALTER TABLE ref_db OWNER TO postgres;

--
-- Name: ref_db_refdb_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ref_db_refdb_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ref_db_refdb_id_seq OWNER TO postgres;

--
-- Name: ref_db_refdb_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ref_db_refdb_id_seq OWNED BY ref_db.refdb_id;


--
-- Name: sample; Type: TABLE; Schema: public; Owner: ; Tablespace: 
--

CREATE TABLE sample (
    sample_id integer NOT NULL,
    exp_id integer,
    name character varying,
    index1 character varying(20),
    index2 character varying(20)
);


ALTER TABLE sample OWNER TO postgres ;

--
-- Name: sample_sample_id_seq; Type: SEQUENCE; Schema: public; Owner: 
--

CREATE SEQUENCE sample_sample_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sample_sample_id_seq OWNER TO postgres ;

--
-- Name: sample_sample_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: 
--

ALTER SEQUENCE sample_sample_id_seq OWNED BY sample.sample_id;


--
-- Name: sample_statistics; Type: TABLE; Schema: public; Owner: ; Tablespace: 
--

CREATE TABLE sample_statistics (
    sample_id integer NOT NULL,
    exp_id integer,
    total_reads integer,
    overlapping_reads integer,
    per_overlapping_reads real,
    non_overlapping_reads integer,
    per_non_overlapping_reads real,
    avg_read_length real,
    avg_quality real,
    avg_mee real,
    meep_cutoff real,
    hq_reads integer,
    per_hq_reads real,
    per_hq_overlap_reads real,
    hq_avg_length real,
    hq_avg_quality real,
    hq_avg_mee real
);


ALTER TABLE sample_statistics OWNER TO postgres ;

--
-- Name: taxonomy; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE taxonomy (
    tax_id integer NOT NULL,
    tax_name text,
    tax_level text,
    refdb_id integer NOT NULL,
    parent_id integer,
    external_id character varying(20)
);


ALTER TABLE taxonomy OWNER TO postgres;

--
-- Name: taxonomy_refdb_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE taxonomy_refdb_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taxonomy_refdb_id_seq OWNER TO postgres;

--
-- Name: taxonomy_refdb_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE taxonomy_refdb_id_seq OWNED BY taxonomy.refdb_id;


--
-- Name: taxonomy_tax_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE taxonomy_tax_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taxonomy_tax_id_seq OWNER TO postgres;

--
-- Name: taxonomy_tax_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE taxonomy_tax_id_seq OWNED BY taxonomy.tax_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: ; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    name character varying,
    e_mail character varying
);


ALTER TABLE users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: 
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO postgres ;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: 
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: profile_id; Type: DEFAULT; Schema: public; Owner: 
--

ALTER TABLE ONLY abundance_profile ALTER COLUMN profile_id SET DEFAULT nextval('abundance_profile_profile_id_seq'::regclass);


--
-- Name: analysis_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY analysis ALTER COLUMN analysis_id SET DEFAULT nextval('analysis_analysis_id_seq'::regclass);


--
-- Name: refdb_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY analysis ALTER COLUMN refdb_id SET DEFAULT nextval('analysis_refdb_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_session ALTER COLUMN id SET DEFAULT nextval('django_session_id_seq'::regclass);


--
-- Name: exp_id; Type: DEFAULT; Schema: public; Owner: 
--

ALTER TABLE ONLY experiment ALTER COLUMN exp_id SET DEFAULT nextval('experiment_exp_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: 
--

ALTER TABLE ONLY metadata ALTER COLUMN id SET DEFAULT nextval('metadata_id_seq'::regclass);


--
-- Name: project_id; Type: DEFAULT; Schema: public; Owner: 
--

ALTER TABLE ONLY project ALTER COLUMN project_id SET DEFAULT nextval('project_project_id_seq'::regclass);


--
-- Name: refdb_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ref_db ALTER COLUMN refdb_id SET DEFAULT nextval('ref_db_refdb_id_seq'::regclass);


--
-- Name: sample_id; Type: DEFAULT; Schema: public; Owner: 
--

ALTER TABLE ONLY sample ALTER COLUMN sample_id SET DEFAULT nextval('sample_sample_id_seq'::regclass);


--
-- Name: tax_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY taxonomy ALTER COLUMN tax_id SET DEFAULT nextval('taxonomy_tax_id_seq'::regclass);


--
-- Name: refdb_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY taxonomy ALTER COLUMN refdb_id SET DEFAULT nextval('taxonomy_refdb_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: 
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Name: M3DB_uploadedfiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "M3DB_uploadedfiles"
    ADD CONSTRAINT "M3DB_uploadedfiles_pkey" PRIMARY KEY (id);


--
-- Name: abundance_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: ; Tablespace: 
--

ALTER TABLE ONLY abundance_profile
    ADD CONSTRAINT abundance_profile_pkey PRIMARY KEY (profile_id);


--
-- Name: analysis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY analysis
    ADD CONSTRAINT analysis_pkey PRIMARY KEY (analysis_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (id);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: experiment_name_key; Type: CONSTRAINT; Schema: public; Owner: ; Tablespace: 
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_name_key UNIQUE (name);


--
-- Name: experiment_pkey; Type: CONSTRAINT; Schema: public; Owner: ; Tablespace: 
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_pkey PRIMARY KEY (exp_id);


--
-- Name: metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: ; Tablespace: 
--

ALTER TABLE ONLY metadata
    ADD CONSTRAINT metadata_pkey PRIMARY KEY (id);


--
-- Name: project_name_key; Type: CONSTRAINT; Schema: public; Owner: ; Tablespace: 
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_name_key UNIQUE (name);


--
-- Name: project_pkey; Type: CONSTRAINT; Schema: public; Owner: ; Tablespace: 
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_pkey PRIMARY KEY (project_id);


--
-- Name: ref_db_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY ref_db
    ADD CONSTRAINT ref_db_pkey PRIMARY KEY (refdb_id);


--
-- Name: sample_pkey; Type: CONSTRAINT; Schema: public; Owner: ; Tablespace: 
--

ALTER TABLE ONLY sample
    ADD CONSTRAINT sample_pkey PRIMARY KEY (sample_id);


--
-- Name: sample_statistics_pkey; Type: CONSTRAINT; Schema: public; Owner: ; Tablespace: 
--

ALTER TABLE ONLY sample_statistics
    ADD CONSTRAINT sample_statistics_pkey PRIMARY KEY (sample_id);


--
-- Name: taxonomy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY taxonomy
    ADD CONSTRAINT taxonomy_pkey PRIMARY KEY (tax_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: ; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: analysis_refdb_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX analysis_refdb_id ON analysis USING btree (refdb_id);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_username_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: taxonomy_refdb_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX taxonomy_refdb_id ON taxonomy USING btree (refdb_id);


--
-- Name: abundance_profile_analysis_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY abundance_profile
    ADD CONSTRAINT abundance_profile_analysis_id_fkey FOREIGN KEY (analysis_id) REFERENCES analysis(analysis_id);


--
-- Name: abundance_profile_exp_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY abundance_profile
    ADD CONSTRAINT abundance_profile_exp_id_fkey FOREIGN KEY (exp_id) REFERENCES experiment(exp_id);


--
-- Name: abundance_profile_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY abundance_profile
    ADD CONSTRAINT abundance_profile_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES sample(sample_id);


--
-- Name: abundance_profile_taxonomy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY abundance_profile
    ADD CONSTRAINT abundance_profile_taxonomy_id_fkey FOREIGN KEY (taxonomy_id) REFERENCES taxonomy(tax_id);


--
-- Name: analysis_refdb_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY analysis
    ADD CONSTRAINT analysis_refdb_id_fkey FOREIGN KEY (refdb_id) REFERENCES ref_db(refdb_id);


--
-- Name: auth_group_permissions_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_93d2d1f8; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT content_type_id_refs_id_93d2d1f8 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_d043b34a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_d043b34a FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: experiment_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_project_id_fkey FOREIGN KEY (project_id) REFERENCES project(project_id);


--
-- Name: metadata_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY metadata
    ADD CONSTRAINT metadata_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES sample(sample_id);


--
-- Name: permission_id_refs_id_6ba0f519; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT permission_id_refs_id_6ba0f519 FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: refdb_id_refs_refdb_id_02b745bb; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY analysis
    ADD CONSTRAINT refdb_id_refs_refdb_id_02b745bb FOREIGN KEY (refdb_id) REFERENCES ref_db(refdb_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sample_exp_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY sample
    ADD CONSTRAINT sample_exp_id_fkey FOREIGN KEY (exp_id) REFERENCES experiment(exp_id);


--
-- Name: sample_statistics_exp_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY sample_statistics
    ADD CONSTRAINT sample_statistics_exp_id_fkey FOREIGN KEY (exp_id) REFERENCES experiment(exp_id);


--
-- Name: sample_statistics_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY sample_statistics
    ADD CONSTRAINT sample_statistics_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES sample(sample_id);


--
-- Name: taxonomy_refdb_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY taxonomy
    ADD CONSTRAINT taxonomy_refdb_id_fkey FOREIGN KEY (refdb_id) REFERENCES ref_db(refdb_id);


--
-- Name: username_exp_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT username_exp_fkey FOREIGN KEY (username) REFERENCES auth_user(username);


--
-- Name: username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY project
    ADD CONSTRAINT username_fkey FOREIGN KEY (username) REFERENCES auth_user(username);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

