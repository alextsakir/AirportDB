# ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ ΑΕΡΟΔΡΟΜΙΟΥ

## ΧΕΙΜΩΝΑΣ 2023 - ΕΚΘΕΣΗ ΕΡΓΑΣΙΑΣ

                                 |
                                 |
                               .-'-.
                              ' ___ '
                      -------'  .-.  '-------
    _________________________'  '-'  '_________________________
     ''''''-|---|--/    \==][^',_m_,'^][==/    \--|---|-''''''
                   \    /  ||/   H   \||  \    /
                    '--'   OO   O|O   OO   '--'


Η Βάση αφορά το αεροδρόμιο και όχι τις αεροπορικές εταιρείες. Επομένως, δεν θα περιλαμβάνονται δεδομένα που
διαχειρίζονται οι εταιρείες, όπως οι κρατήσεις των επιβατών, τα προσωπικά τους στοιχεία, οι τιμές των εισιτηρίων
ή η πολιτική μεταφοράς αποσκευών για την κάθε πτήση.

Το κάθε αεροδρόμιο, μεταξύ του οποίου και του παρόντος διενεργούνται πτήσεις, περιγράφεται σαν οντότητα
Airport, με attributes όπως όνομα, κωδικός τριών χαρακτήρων βάσει IATA (INTERNATIONAL AIR TRANSPORT
ASSOCIATION), συντεταγμένες, χώρα και ζώνη ώρας.

Η Βάση περιλαμβάνει την οντότητα Αεροπλάνο (Airplane) μόνο με τύπο (μοντέλο) και την αεροπορική εταιρεία
στην οποία ανήκει. Δεν καταγράφονται δεδομένα όπως κινητήρες, αριθμός θέσεων, χωρητικότητα για αποσκευές,
καθώς είναι θέματα που απασχολούν μόνο την εταιρεία.

Η οντότητα Schedule υποδεικνύει τις πτήσεις που είναι προγραμματισμένες να γίνονται κάποιες μέρες της
εβδομάδας, την ίδια ώρα. Για παράδειγμα, μια πτήση από την Αθήνα στη Θεσσαλονίκη που γίνεται όλο τον χρόνο
στις 9 το πρωί (7.00 ώρα Greenwich), από Δευτέρα ως Παρασκευή, θεωρείται προγραμματισμένη. Κάθε οντότητα
Schedule έχει έναν κωδικό πτήσης.

Η οντότητα Flight αναπαριστά μία πτήση που θα γίνει συγκεκριμένη μέρα, ώρα, με προκαθορισμένη αφετηρία και
προορισμό, αεροπλάνο, όπως και διάρκεια. Όλες οι πτήσεις που γίνονται με βάση την ίδια προγραμματισμένη,
θεωρούμε πως μοιράζονται τον ίδιο κωδικό πτήσης, ο οποίος περιέχει πληροφορία και για την εταιρεία που τη
διενεργεί.

ΣΗΜΑΝΤΙΚΟ: Όλες οι ώρες άφιξης ή αναχώρησης που γράφονται στη Βάση, είναι μετρημένες στη ζώνη ώρας του
Greenwich. Έτσι αποφεύγεται η σύγχυση σε πτήσεις που αλλάζει η ζώνη ώρας, ή μεταξύ χωρών που η μία
χρησιμοποιεί θερινή ώρα και η άλλη όχι.

Καθώς όλες οι ώρες είναι εκφρασμένες σε ώρα Greenwich, η διάρκεια μιας πτήσης υπολογίζεται από τη διαφορά
ώρας άφιξης και αναχώρησης. Η τοπική ώρα στον προσανατολισμό μιας πτήσης που αναχωρεί από το παρόν
αεροδρόμιο, θα υπολογίζεται λαμβάνοντας υπ’ όψιν τη ζώνη ώρας του δικού της αεροδρομίου.

Η οντότητα Flight έχει ένα attribute που λέγεται State. Τα διαφορετικά States είναι [να γραφτούν].







