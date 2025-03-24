The citeseer dataset is a little bit weird

The id of appers that read something like `10.1.1.144.645` refers to a particular document crawled by citeseer. The documents are grouped by cluster which is a integer essentially. So you can find (always?) the cluster of a document in the papers table.

The citation information contained in the `citations` table will be structured so that the document citing is an actual document, so it is identifioed by paperid in the format `10.1.1.144.645`. But that tuple from the table is essentially a single citation at the end of that document. It cite the (previous) document with title by the `title` field which has been mapped (maybe?) to a particular cluster `cluster`. That cluster MAY appear in `papers`, but it also may not.


