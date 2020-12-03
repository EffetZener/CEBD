CREATE TABLE LesSportifs_base
(
  numSp NUMBER(4),
  nomSp VARCHAR2(20),
  prenomSp VARCHAR2(20),
  pays VARCHAR2(20),
  categorieSp VARCHAR2(10),
  dateNaisSp DATE,
  CONSTRAINT SP_PK PRIMARY KEY(numSp),
  CONSTRAINT SP_CK1 CHECK(numSp > 0),
  CONSTRAINT SP_UN UNIQUE(nomSp, prenomSp),
  CONSTRAINT SP_CK2 CHECK(categorieSp IN ('feminin','masculin'))
);

CREATE TABLE LesEquipiers
(
  numEq NUMBER(4) NOT NULL,
  numSp NUMBER(4) NOT NULL,
  CONSTRAINT EQ_PK PRIMARY KEY(numEq, numSp),
  CONSTRAINT EQ_FK FOREIGN KEY(numSp) REFERENCES LesSportifs_base(numSp),
  CONSTRAINT EQ_CK1 CHECK(numEq > 0)
);

CREATE TABLE LesDisciplines
(
    nomDi VARCHAR2(20),
    CONSTRAINT EQ_PK PRIMARY KEY(nomDi)
);

CREATE TABLE LesEpreuves
(
  numEp NUMBER(3),
  nomEp VARCHAR2(20),
  formeEp VARCHAR2(13),
  categorieEp VARCHAR2(10),
  nbSportifsEp NUMBER(2),
  dateEp DATE,
  nomDi VARCHAR2 (20),
  CONSTRAINT EP_PK PRIMARY KEY (numEp),
  CONSTRAINT EP_CK1 CHECK (formeEp IN ('individuelle','par equipe','par couple')),
  CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
  CONSTRAINT EP_CK3 CHECK (numEp > 0),
  CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 0),
  CONSTRAINT EQ_FK FOREIGN KEY(nomDi) REFERENCES LesDisciplines(nomDi)
);

CREATE TABLE LesInscriptions
(
  numIn NUMBER(4) NOT NULL,
  numEp NUMBER(4) NOT NULL,
  CONSTRAINT I_PK PRIMARY KEY(numIn, numEp),
  CONSTRAINT I_FK FOREIGN KEY(numEp) REFERENCES LesEpreuves(numEp),
  CONSTRAINT I_CK1 CHECK (numIn > 0)
);

CREATE TABLE LesResultats
(
  numEp NUMBER(4),
  gold NUMBER(4),
  silver NUMBER(4),
  bronze NUMBER(4),
  CONSTRAINT RES_PK PRIMARY KEY (numEp),
  CONSTRAINT RES_FK1 FOREIGN KEY (gold, numEp) REFERENCES LesInscriptions(numIn,numEp),
  CONSTRAINT RES_FK2 FOREIGN KEY (silver, numEp) REFERENCES LesInscriptions(numIn,numEp),
  CONSTRAINT RES_FK3 FOREIGN KEY (bronze, numEp) REFERENCES LesInscriptions(numIn,numEp),
  CONSTRAINT RES_CK1 CHECK (gold<>silver AND silver<>bronze AND gold<>bronze)
);


CREATE VIEW LesSportifs AS
    SELECT numSp, nomSp, prenomSp, pays,categorieSp,dateNaisSp,date('now')-dateNaisSp AS age
    FROM LesSportifs_base;

CREATE VIEW LesEquipes AS
    SELECT numEq,count(numSp) AS nbEquipiersEq 
    FROM LesEquipiers 
    GROUP BY numEq;


CREATE VIEW LesClassements AS
    SELECT R.numEp AS numEp, S1.pays AS P1, S2.pays AS P2, S3.pays AS P3 
    FROM LesResultats R JOIN LesSportifs S1 JOIN LesSportifs S2 JOIN LesSportifs S3 
    ON S1.numSp = gold AND S2.numSp = silver AND S3.numSp = bronze
    UNION
    SELECT DISTINCT R.numEp AS numEp, S1.pays AS P1, S2.pays AS P2, S3.pays AS P3  
    FROM LesResultats R JOIN LesEquipiers  E1 JOIN LesEquipiers  E2 JOIN LesEquipiers E3 JOIN LesSportifs S1 JOIN LesSportifs S2 JOIN LesSportifs S3
    ON E1.numEq = gold AND E2.numEq = silver AND E3.numEq = bronze AND E1.numSp = S1.numsp AND E2.numSp = S2.numsp AND E3.numSp = S3.numsp;

CREATE VIEW paysOrs AS 
    SELECT count(numEp) AS nbOr,P1 AS pays FROM LesClassements GROUP BY P1;

CREATE VIEW paysArgents AS 
    SELECT count(numEp) AS nbArgent,P2 AS pays FROM LesClassements GROUP BY P2;

CREATE VIEW paysBronzes AS 
    SELECT count(numEp) AS nbBronze,P3 AS pays FROM LesClassements GROUP BY P3;


CREATE VIEW paysMed AS
    SELECT pays as pays ,nbOr as nbOr,0 as nbArgent,0 as nbBronze
    FROM paysOrs 
        UNION 
    SELECT pays,0,nbArgent,0 
    FROM paysArgents 
        UNION
    SELECT pays,0,0,nbBronze
    FROM paysBronzes;
-- TODO 1.2a : ajouter la définition de la vue LesSportifs
-- TODO 1.3a : ajouter la création de la table LesDisciplines et ajouter l'attribut discipline dans la table LesEpreuves
-- TODO 1.4a : ajouter la définition de la vue LesEquipes
