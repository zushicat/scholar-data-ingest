--
-- PostgreSQL database dump
--

-- Dumped from database version 11.10
-- Dumped by pg_dump version 12.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

--
-- Name: author; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.author (
    id integer NOT NULL,
    author_id text NOT NULL,
    name text NOT NULL,
    also_referring_ids text
);


--
-- Name: author_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.author_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: author_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.author_id_seq OWNED BY public.author.id;


--
-- Name: paper; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.paper (
    id integer NOT NULL,
    paper_id text NOT NULL,
    year_published integer,
    all_author_ids text NOT NULL,
    text_id text NOT NULL,
    research_fields text,
    is_cited_ids text,
    has_cited_ids text,
    first_author_id text NOT NULL,
    last_author_id text,
    co_authors_ids text,
    number_authors integer NOT NULL
);


--
-- Name: paper_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.paper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: paper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.paper_id_seq OWNED BY public.paper.id;


--
-- Name: text; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.text (
    id integer NOT NULL,
    text_id text NOT NULL,
    paper_id text NOT NULL,
    title text NOT NULL,
    abstract text,
    language text
);


--
-- Name: text_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.text_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: text_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.text_id_seq OWNED BY public.text.id;


--
-- Name: author id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.author ALTER COLUMN id SET DEFAULT nextval('public.author_id_seq'::regclass);


--
-- Name: paper id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper ALTER COLUMN id SET DEFAULT nextval('public.paper_id_seq'::regclass);


--
-- Name: text id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.text ALTER COLUMN id SET DEFAULT nextval('public.text_id_seq'::regclass);


--
-- Name: author author_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT author_pkey PRIMARY KEY (id);


--
-- Name: paper paper_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paper
    ADD CONSTRAINT paper_pkey PRIMARY KEY (id);


--
-- Name: text text_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.text
    ADD CONSTRAINT text_pkey PRIMARY KEY (id);


--
-- Name: author_author_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX author_author_id_idx ON public.author USING btree (author_id);


--
-- Name: paper_paper_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX paper_paper_id_idx ON public.paper USING btree (paper_id);


--
-- Name: text_paper_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX text_paper_id_idx ON public.text USING btree (paper_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

GRANT USAGE ON SCHEMA public TO admin;


--
-- Name: TABLE author; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.author TO admin;


--
-- Name: TABLE paper; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.paper TO admin;


--
-- Name: TABLE text; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT ON TABLE public.text TO admin;


--
-- PostgreSQL database dump complete
--

