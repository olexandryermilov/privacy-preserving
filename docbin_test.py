from spacy.tokens import DocBin
import spacy

nlp = spacy.blank("en")
doc_bin = DocBin().from_disk("summarization_doc_bins.gz")
docs = list(doc_bin.get_docs(nlp.vocab))
for entity in docs[0]:
    if entity.ent_type_:
        print(entity.text)
