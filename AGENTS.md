{
    "@context": {
        "@vocab": "http://example.com/build-ontology#",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "label": "http://www.w3.org/2000/01/rdf-schema#label",
        "prov": "http://www.w3.org/ns/prov#",
        "subClassOf": "http://www.w3.org/2000/01/rdf-schema#subClassOf"
    },
    "@graph": [
        {
            "@id": "http://example.com/build-ontology#.",
            "@type": "InferentialStep",
            "hasConclusion": {
                "@id": "http://example.com/build-ontology#app_artifact"
            },
            "hasPremise": [
                {
                    "@id": "http://example.com/build-ontology#core"
                },
                {
                    "@id": "http://example.com/build-ontology#critic"
                },
                {
                    "@id": "http://example.com/build-ontology#compliance"
                }
            ],
            "label": "Proof Step for .",
            "prov:used": [
                {
                    "@id": "http://example.com/build-ontology#core_library"
                },
                {
                    "@id": "http://example.com/build-ontology#critic_artifact"
                },
                {
                    "@id": "http://example.com/build-ontology#compliance_artifact"
                }
            ],
            "requiresResource": [
                {
                    "@id": "http://example.com/build-ontology#core_library"
                },
                {
                    "@id": "http://example.com/build-ontology#critic_artifact"
                },
                {
                    "@id": "http://example.com/build-ontology#compliance_artifact"
                }
            ]
        },
        {
            "@id": "http://example.com/build-ontology#compliance",
            "@type": "AxiomaticStep",
            "hasConclusion": {
                "@id": "http://example.com/build-ontology#compliance_artifact"
            },
            "label": "Proof Step for compliance"
        },
        {
            "@id": "http://example.com/build-ontology#AxiomaticStep",
            "subClassOf": {
                "@id": "http://example.com/build-ontology#ProofStep"
            }
        },
        {
            "@id": "http://example.com/build-ontology#core_library",
            "@type": "BuildArtifact",
            "hasType": "!Library",
            "label": "A core library containing essential business logic.",
            "prov:wasDerivedFrom": {
                "@id": "http://example.com/build-ontology#core"
            },
            "prov:wasGeneratedBy": {
                "@id": "http://example.com/build-ontology#core"
            }
        },
        {
            "@id": "http://example.com/build-ontology#hasSequent",
            "@type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
        },
        {
            "@id": "http://example.com/build-ontology#core",
            "@type": "AxiomaticStep",
            "hasConclusion": {
                "@id": "http://example.com/build-ontology#core_library"
            },
            "label": "Proof Step for core"
        },
        {
            "@id": "http://example.com/build-ontology#Sequent",
            "@type": "http://www.w3.org/2000/01/rdf-schema#Class"
        },
        {
            "@id": "http://example.com/build-ontology#BuildArtifact",
            "@type": "http://www.w3.org/2000/01/rdf-schema#Class",
            "subClassOf": {
                "@id": "prov:Entity"
            }
        },
        {
            "@id": "http://example.com/build-ontology#compliance_artifact",
            "@type": "BuildArtifact",
            "hasType": "Placeholder",
            "label": "This module has no defined succedent. It may be a container for other modules.",
            "prov:wasDerivedFrom": {
                "@id": "http://example.com/build-ontology#compliance"
            },
            "prov:wasGeneratedBy": {
                "@id": "http://example.com/build-ontology#compliance"
            }
        },
        {
            "@id": "http://example.com/build-ontology#ProofStep",
            "@type": "http://www.w3.org/2000/01/rdf-schema#Class",
            "subClassOf": {
                "@id": "prov:Activity"
            }
        },
        {
            "@id": "http://example.com/build-ontology#hasConclusion",
            "@type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
        },
        {
            "@id": "http://example.com/build-ontology#requiresResource",
            "@type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
        },
        {
            "@id": "http://example.com/build-ontology#hasPremise",
            "@type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
        },
        {
            "@id": "http://example.com/build-ontology#InferentialStep",
            "subClassOf": {
                "@id": "http://example.com/build-ontology#ProofStep"
            }
        },
        {
            "@id": "http://example.com/build-ontology#critic_artifact",
            "@type": "BuildArtifact",
            "hasType": "Placeholder",
            "label": "This module has no defined succedent. It may be a container for other modules.",
            "prov:wasDerivedFrom": {
                "@id": "http://example.com/build-ontology#critic"
            },
            "prov:wasGeneratedBy": {
                "@id": "http://example.com/build-ontology#critic"
            }
        },
        {
            "@id": "http://example.com/build-ontology#critic",
            "@type": "AxiomaticStep",
            "hasConclusion": {
                "@id": "http://example.com/build-ontology#critic_artifact"
            },
            "label": "Proof Step for critic"
        },
        {
            "@id": "http://example.com/build-ontology#app_artifact",
            "@type": "BuildArtifact",
            "hasType": "Placeholder",
            "label": "This module has no defined succedent. It may be a container for other modules.",
            "prov:wasGeneratedBy": {
                "@id": "http://example.com/build-ontology#."
            }
        }
    ]
}