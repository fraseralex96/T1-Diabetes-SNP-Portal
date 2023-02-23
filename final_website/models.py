from db_init import Base, metadata, engine
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


class Variants(Base):

    __tablename__ = 'Variants'

    id = Column('variant_id', Integer, primary_key = True)
    variant_name = Column('variant_name', String)
    allele = Column('allele', String)
    p_value = Column('p_value', Float)
    chromosome = Column('chromosome', Integer)
    location_on_chromosome= Column('location_on_chromosome', Integer)
    rel1 = relationship('Clinical_significance')
    rel2 = relationship('RAFs')
    rel3 = relationship('Variant_gene_relationship')


    def __init__(self, id=None, 
        variant_name=None, p_value=None, 
        chromosome=None, location_on_chromosome=None):
        self.id = id    
        self.variant_name = variant_name
        self.allele = allele
        self.p_value = p_value
        self.chromosome = chromosome
        self.location_on_chromosome = location_on_chromosome

class Clinical_significance(Base):

    __tablename__ = 'Clinical_significance'

    id = Column('variant_ID', Integer, primary_key = True)
    variant_name = Column('variant_name', String, ForeignKey('Variants.variant_name'))
    variant_consequence = Column('variant_consequence', String)
    clinical_significance = Column('clinical_significance', String)
    polyPhen_prediction = Column('polyPhen_prediction', String)
    polyPhen_score = Column('polyPhen_score', Integer)
    sift_prediction = Column('sift_prediction', String)
    sift_score = Column('sift_score', Integer)


    def __init__(self, id=None, 
        variant_name=None, variant_consequence=None, 
        clinical_significance=None):
        self.id = id    
        self.variant_name = variant_name
        self.variant_consequence = variant_consequence
        self.clinical_significance = clinical_significance
        self.polyPhen_prediction = polyPhen_prediction   
        self.polyPhen_score = polyPhen_score
        self.sift_prediction = sift_prediction
        self.sift_score = sift_score


class RAFs(Base):

    __tablename__ = 'RAFs'

    id = Column('Variant_ID', Integer, primary_key = True)
    variant_name = Column('Variant_name', String, ForeignKey('Variants.variant_name'))
    han_raf = Column('Han_raf', Float)
    yoruba_raf = Column('Yoruba_raf', Float)
    gbr_raf= Column('GBR_raf', Float)

    def __init__(self, id=None, 
        variant_name=None, han_raf=None, 
        yoruba_raf=None, gbr_raf=None):
        self.id = id    
        self.variant_name = variant_name
        self.han_raf = han_raf
        self.yoruba_raf = yoruba_raf
        self.gbr_raf = gbr_raf


class Variant_gene_relationship(Base):

    __tablename__ = 'Variant_gene_relationship'

    variant_name = Column('Variant_name', String, ForeignKey('Variants.variant_name'))
    gene_name = Column('Gene_name', String)
    __table_args__ = (
    PrimaryKeyConstraint(variant_name, gene_name),
    {})
    rel = relationship('GO_terms')

    def __init__(self, variant_name=None, 
        gene_name=None):
        self.variant_name = variant_name    
        self.gene_name = gene_name

class GO_terms(Base):

    __tablename__ = 'GO_terms'

    id = Column('Gene_ID', Integer, primary_key = True)
    gene_name = Column('Gene_name', String, ForeignKey('Variant_gene_relationship.Gene_name'))
    go_domain = Column('GO_domain', String)
    go_term_name = Column('GO_term_name', String)
    go_term_definition = Column('GO_term_definition', String)
    go_term_accession = Column('GO_term_accession', String)


    def __init__(self, id=None, 
        gene_name=None, go_term=None):
        self.id = id    
        self.gene_name = gene_name
        self.go_domain = go_domain
        self.go_term_name = go_term_name
        self.go_term_definition = go_term_definition
        self.go_term_accession = go_term_accession

chr6_GBR_r = Table('chr6_GBR_r', metadata, autoload=True, autoload_with=engine)
chr6_Han_r = Table('chr6_Han_r', metadata, autoload=True, autoload_with=engine)
chr6_Yoruba_r = Table('chr6_Yoruba_r', metadata, autoload=True, autoload_with=engine)

