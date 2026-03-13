"""
Knowledge Graph Engine — Implements the 4 pillars of the Glean Knowledge Graph:
1. Content Integration  2. People Intelligence  3. Activity Tracking  4. Collective Intelligence

This serves as the core intelligence layer for the IDP portal.
"""

import json
import re
from datetime import datetime, timedelta
from collections import defaultdict


class KnowledgeObject:
    """A single indexed item in the Knowledge Graph."""

    def __init__(self, doc_id, source, title, content, author,
                 doc_type="document", metadata=None, acl=None, timestamp=None):
        self.id = doc_id
        self.source = source
        self.title = title
        self.content = content
        self.author = author
        self.doc_type = doc_type
        self.metadata = metadata or {}
        self.acl = acl or ["Public"]
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.view_count = 0
        self.search_hit_count = 0

    def to_dict(self):
        return {
            "id": self.id, "source": self.source, "title": self.title,
            "content": self.content, "author": self.author, "doc_type": self.doc_type,
            "metadata": self.metadata, "acl": self.acl, "timestamp": self.timestamp,
            "view_count": self.view_count, "search_hit_count": self.search_hit_count,
        }


class PersonProfile:
    """People Intelligence — A unified identity across all data sources."""

    def __init__(self, person_id, name, email, team, role, manager=None):
        self.id = person_id
        self.name = name
        self.email = email
        self.team = team
        self.role = role
        self.manager = manager
        self.expertise = []
        self.authored_docs = []
        self.collaborators = set()
        self.activity_score = 0

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "email": self.email,
            "team": self.team, "role": self.role, "manager": self.manager,
            "expertise": self.expertise, "authored_docs": len(self.authored_docs),
            "collaborators": list(self.collaborators), "activity_score": self.activity_score,
        }


class KnowledgeGraphEngine:
    """
    The core Knowledge Graph engine implementing all 4 Glean pillars.
    """

    def __init__(self):
        # Pillar 1: Content Integration
        self.documents = {}  # doc_id → KnowledgeObject
        self.inverted_index = defaultdict(set)  # word → set of doc_ids
        self.facets = defaultdict(lambda: defaultdict(set))  # facet → value → doc_ids

        # Pillar 2: People Intelligence
        self.people = {}  # person_id → PersonProfile
        self.org_graph = {}  # person_id → manager_id
        self.collaboration_graph = defaultdict(set)

        # Pillar 3: Activity Tracking
        self.search_history = []
        self.view_history = []
        self.knowledge_gaps = defaultdict(int)  # query → miss count

        # Pillar 4: Collective Intelligence
        self.trending_docs = []
        self.popular_by_team = defaultdict(list)

    # ==============================
    # PILLAR 1: Content Integration
    # ==============================

    def index_document(self, ko: KnowledgeObject):
        """Index a Knowledge Object into the graph."""
        self.documents[ko.id] = ko

        # Build inverted index
        words = self._tokenize(ko.title + " " + ko.content)
        for word in words:
            self.inverted_index[word].add(ko.id)

        # Build facets
        self.facets["source"][ko.source].add(ko.id)
        self.facets["doc_type"][ko.doc_type].add(ko.id)
        self.facets["author"][ko.author].add(ko.id)
        for key, val in ko.metadata.items():
            self.facets[key][str(val)].add(ko.id)

        # Link to People Intelligence
        if ko.author in self.people:
            self.people[ko.author].authored_docs.append(ko.id)

    def search(self, query, user_groups=None, facet_filters=None, limit=10):
        """
        Permission-aware, activity-boosted search.
        Implements ACL checking (Pillar 1) + Activity boost (Pillar 3) + Collective boost (Pillar 4).
        """
        user_groups = user_groups or ["Public"]
        facet_filters = facet_filters or {}
        query_words = self._tokenize(query)

        # Find matching doc IDs from inverted index
        matching_ids = set()
        for word in query_words:
            matching_ids.update(self.inverted_index.get(word, set()))

        # Apply facet filters
        for facet_key, facet_val in facet_filters.items():
            facet_ids = self.facets.get(facet_key, {}).get(facet_val, set())
            matching_ids = matching_ids.intersection(facet_ids)

        # Score and filter by ACLs
        results = []
        for doc_id in matching_ids:
            doc = self.documents[doc_id]
            # ACL check
            if not any(g in doc.acl for g in user_groups):
                continue

            score = self._score(doc, query_words)
            results.append({"document": doc.to_dict(), "score": round(score, 2)})

        results.sort(key=lambda x: x["score"], reverse=True)

        # Track activity (Pillar 3)
        self._record_search(query, len(results))

        return results[:limit]

    def get_facets(self):
        """Return available facets and their value counts for faceted search."""
        return {
            facet: {val: len(ids) for val, ids in values.items()}
            for facet, values in self.facets.items()
        }

    def _score(self, doc, query_words):
        """Score a document: TF relevance + activity boost + collective boost."""
        text = (doc.title + " " + doc.content).lower()
        # Term frequency
        tf_score = sum(text.count(w) for w in query_words)
        # Title boost
        title_boost = sum(2 for w in query_words if w in doc.title.lower())
        # Activity boost (Pillar 3)
        activity_boost = doc.view_count * 0.1
        # Collective boost (Pillar 4)
        collective_boost = doc.search_hit_count * 0.05
        return tf_score + title_boost + activity_boost + collective_boost

    def _tokenize(self, text):
        return [w.lower() for w in re.findall(r'\w+', text) if len(w) > 2]

    # ==============================
    # PILLAR 2: People Intelligence
    # ==============================

    def add_person(self, profile: PersonProfile):
        """Add a person to the People Intelligence layer."""
        self.people[profile.id] = profile
        if profile.manager:
            self.org_graph[profile.id] = profile.manager

    def get_person(self, person_id):
        if person_id in self.people:
            return self.people[person_id].to_dict()
        return None

    def find_expert(self, topic):
        """Find the person most associated with a topic."""
        experts = []
        for pid, person in self.people.items():
            if topic.lower() in [e.lower() for e in person.expertise]:
                experts.append(person.to_dict())
        experts.sort(key=lambda x: x["activity_score"], reverse=True)
        return experts

    def build_collaboration_graph(self):
        """Build collaboration edges from shared document authorship."""
        doc_authors_by_source = defaultdict(set)
        for doc in self.documents.values():
            key = doc.metadata.get("project", doc.source)
            doc_authors_by_source[key].add(doc.author)

        for source, authors in doc_authors_by_source.items():
            authors = list(authors)
            for i in range(len(authors)):
                for j in range(i + 1, len(authors)):
                    if authors[i] in self.people and authors[j] in self.people:
                        self.people[authors[i]].collaborators.add(authors[j])
                        self.people[authors[j]].collaborators.add(authors[i])

    # ==============================
    # PILLAR 3: Activity Tracking
    # ==============================

    def _record_search(self, query, result_count):
        self.search_history.append({
            "query": query, "results": result_count,
            "timestamp": datetime.utcnow().isoformat()
        })
        if result_count == 0:
            self.knowledge_gaps[query] += 1

    def record_view(self, doc_id, user_id):
        if doc_id in self.documents:
            self.documents[doc_id].view_count += 1
            self.view_history.append({
                "doc_id": doc_id, "user": user_id,
                "timestamp": datetime.utcnow().isoformat()
            })

    def get_knowledge_gaps(self):
        """Return queries that returned 0 results — knowledge gaps."""
        return dict(sorted(self.knowledge_gaps.items(), key=lambda x: x[1], reverse=True))

    # ==============================
    # PILLAR 4: Collective Intelligence
    # ==============================

    def compute_trending(self, top_n=10):
        """Compute trending documents based on recent view activity."""
        sorted_docs = sorted(
            self.documents.values(),
            key=lambda d: d.view_count + d.search_hit_count,
            reverse=True
        )
        self.trending_docs = [d.to_dict() for d in sorted_docs[:top_n]]
        return self.trending_docs

    def get_stats(self):
        """Return Knowledge Graph statistics."""
        return {
            "total_documents": len(self.documents),
            "total_people": len(self.people),
            "total_searches": len(self.search_history),
            "knowledge_gaps": len(self.knowledge_gaps),
            "facets": len(self.facets),
            "sources": list(self.facets.get("source", {}).keys()),
        }


if __name__ == "__main__":
    kg = KnowledgeGraphEngine()

    # Add people
    kg.add_person(PersonProfile("alice", "Alice Chen", "alice@corp.com", "SRE", "Staff SRE", "bob"))
    kg.add_person(PersonProfile("bob", "Bob Kumar", "bob@corp.com", "Platform", "Director", None))
    kg.people["alice"].expertise = ["kubernetes", "incident-response", "payment-api"]

    # Index documents
    kg.index_document(KnowledgeObject(
        "RB-001", "Internal Wiki", "Payment API Runbook",
        "Step-by-step guide to diagnosing payment API failures including database rollback procedures.",
        "alice", "runbook", {"project": "INFRA", "priority": "P1"}, ["SRE", "DevOps"]
    ))
    kg.index_document(KnowledgeObject(
        "OKR-Q1", "OKR Tool", "Q1 Platform Reliability OKR",
        "Objective: Achieve 99.95% uptime. Key Result: Reduce MTTR to under 15 minutes.",
        "bob", "okr", {"quarter": "Q1", "team": "Platform"}, ["Platform", "Executives"]
    ))

    # Search
    results = kg.search("payment runbook", user_groups=["SRE"])
    print(json.dumps(results, indent=2))

    # Find expert
    experts = kg.find_expert("kubernetes")
    print("\nKubernetes experts:", json.dumps(experts, indent=2))

    print("\nKG Stats:", json.dumps(kg.get_stats(), indent=2))
