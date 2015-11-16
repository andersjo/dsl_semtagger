# dsl_semtagger
## TODO
1. File converters to internal format (UD-based)
2. POS-tag and lemmatize training data (which comes out as bare form+supersense annotations from webanno)
  1. Export from UD_Danish to get POS tags
  2. Train POS-tagger on Rungsted (Form, suffixes, embeddings?)
  3. Lemmatize using STO and the lillelemma module we have used before
3. Feature extractor
  1. Embeddings?
5. Deployment scripts (install, train, predict)
