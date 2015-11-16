# dsl_semtagger
## TODO
1. File converters to internal format (UD-based)
  1. dsl2ud -- in particular to set punctuations as tokens
  2. ud2dsl -- to make sure the output is korpusdk-compliant (`<s>` tags, punctuations in their own column, etc)
2. POS-tag and lemmatize training data (which comes out as bare form+supersense annotations from webanno)
  1. Export from UD_Danish to get POS tags
  2. Train POS-tagger on Rungsted (Form, suffixes, embeddings?)
  3. Lemmatize using STO and the lillelemma module we have used before
  4. Data to predict from korpus2010 must also be re-postagged but we can keep the original lemmas if we decide to do so.
3. Feature extractor
  1. Embeddings? If so, where from, ClarinDK?
  2. Brown clusters.
5. Deployment scripts (install, train, predict)
