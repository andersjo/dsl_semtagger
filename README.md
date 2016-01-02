# dsl_semtagger
## Installing
1. install python 3.4 from Anaconda
2. install Rungsted 
3. cd src
4. sh deploy.sh (downloads embeddings, trains SST on semdax_full and predicts on data/samples/0008.txt
5. 

## Evaluation
A classification report without BI prefixes, testing on the following files (and training on the rest of semdax):
             precision    recall  f1-score   support

          O       0.94      0.96      0.95      9179
    adj.all       0.66      0.62      0.64       294
 adj.mental       0.54      0.57      0.56        68
   adj.phys       0.50      0.61      0.55       114
 adj.social       0.79      0.62      0.69        99
   adj.time       0.81      0.75      0.78        97
   noun.TOP       0.00      0.00      0.00         1
noun.abstract       0.40      0.56      0.47       106
   noun.act       0.49      0.53      0.51       137
noun.animal       0.54      0.58      0.56        12
noun.artifact       0.58      0.32      0.41       292
noun.attribute       0.37      0.35      0.36        37
  noun.body       0.68      0.60      0.64        53
noun.building       0.63      0.67      0.65        73
noun.cognition       0.54      0.37      0.44       112
noun.communication       0.60      0.56      0.58       508
noun.container       0.29      0.67      0.40         3
noun.disease       0.29      0.50      0.36         4
noun.domain       0.53      0.30      0.38        27
 noun.event       0.40      0.34      0.37        50
noun.feeling       0.61      0.77      0.68        26
  noun.food       0.83      0.71      0.77        35
 noun.group       0.67      0.13      0.22        15
noun.institution       0.62      0.64      0.63       180
noun.location       0.54      0.79      0.64       106
noun.motive       0.40      0.33      0.36         6
noun.object       0.33      0.20      0.25        15
noun.person       0.75      0.83      0.79       803
noun.phenomenon       0.20      0.31      0.25        29
 noun.plant       0.35      0.60      0.44        10
noun.possession       0.25      0.12      0.16        17
noun.quantity       0.58      0.70      0.63        74
noun.relation       0.22      0.19      0.20        27
 noun.shape       0.80      0.40      0.53        10
 noun.state       0.33      0.16      0.22        37
noun.substance       0.18      0.29      0.22         7
  noun.time       0.85      0.92      0.88       226
noun.vehicle       0.50      0.46      0.48        26
  verb.COLL       0.50      0.21      0.30       205
verb.PARTICLE       0.67      0.52      0.58        93
verb.REFLPRON       0.71      0.71      0.71        38
verb.TOP       1.00      1.00      1.00         1
verb.act       0.49      0.62      0.55       206
verb.aspectual       0.80      0.41      0.55        29
verb.body       0.00      0.00      0.00         5
verb.change       0.45      0.33      0.38        82
verb.cognition       0.67      0.52      0.58       214
verb.communication       0.71      0.72      0.71       227
verb.competition       0.67      0.60      0.63        10
verb.consumption       1.00      0.33      0.50         9
verb.contact       0.75      0.33      0.46         9
verb.creation       0.56      0.42      0.48        33
verb.emotion       0.47      0.24      0.31        93
verb.motion       0.46      0.56      0.50        95
verb.perception       0.64      0.43      0.51        49
verb.phenomenon       0.31      0.44      0.36        61
verb.possession       0.46      0.70      0.56        93
verb.social       0.73      0.16      0.27        68
verb.stative       0.77      0.85      0.81       481

avg / total       0.82      0.82      0.82     15016
