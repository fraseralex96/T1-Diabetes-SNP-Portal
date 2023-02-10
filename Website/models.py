from app import db
from sqlalchemy.schema import PrimaryKeyConstraint

class Variants(db.Model):

    __tablename__ = 'Variants'

    Variant_ID = db.Column('Variant_ID', db.Integer, primary_key = True)
    Variant_name = db.Column('Variant_name', db.String)
    P_Value = db.Column('P_value', db.Float)
    Chromosome = db.Column('Chromosome', db.Integer)
    Location_On_Chromosome= db.Column('Location_on_chromosome', db.Integer)

class Clinical_significance(db.Model):

    __tablename__ = 'Clinical_significance'

    Variant_ID = db.Column('Variant_ID', db.Integer, primary_key = True)
    Variant_name = db.Column('Variant_name', db.String)
    Variant_consequence = db.Column('Variant_consequence', db.String)
    Clinical_significance = db.Column('Clinical_significance', db.String)

class GO_terms(db.Model):

    __tablename__ = 'GO_terms'

    Gene_ID = db.Column('Gene_ID', db.Integer, primary_key = True)
    Gene_name = db.Column('Gene_name', db.String)
    GO_term = db.Column('GO_term', db.String)

class RAFs(db.Model):

    __tablename__ = 'RAFs'

    Variant_ID = db.Column('Variant_ID', db.Integer, primary_key = True)
    Variant_name = db.Column('Variant_name', db.String)
    Han_raf = db.Column('Han_raf', db.Float)
    Yoruba_raf = db.Column('Yoruba_raf', db.Float)
    GBR_raf= db.Column('GBR_raf', db.Float)

class Variant_gene_relationship(db.Model):

    __tablename__ = 'Variant_gene_relationship'

    Variant_name = db.Column('GO_term', db.String)
    Gene_name = db.Column('Gene_name', db.String)
    __table_args__ = (
    PrimaryKeyConstraint(Variant_name, Gene_name),
    {}
    )

