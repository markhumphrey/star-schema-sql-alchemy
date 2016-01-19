from datetime import date

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

import config
from parsers.sales import Parser, Fields

from models.normalized import (Base, Country, Date, Product, ProductLine,
                               ProductType, OrderType, RetailerType, Sale)


engine = create_engine(config.DATABASE_URI, echo=config.SQLALCHEMY_ENGINE_ECHO)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

def load_models():
    Base.metadata.drop_all()
    Base.metadata.create_all()

    parser = Parser(config.DATA_FILENAME)
    BATCH_SIZE = 1000
    count = 0
    for sale in parser.parse_sale():
        print sale

        load_country(session, sale)
        date = load_date(session, sale)
        product = load_product(session, sale)
        load_product_line(session, sale)
        load_product_type(session, sale)
        load_order_type(session, sale)
        load_retailer_type(session, sale)
        load_sale(session, sale, product, date)

        count += 1
        if count == BATCH_SIZE:
            # commit this batch of models
            session.commit()
            count = 0


    # commit any left over models
    session.commit()


def load_sale(session, sale, product, date):
    model = Sale(product=product,
                 date=date,
                 revenue=sale[Fields.revenue],
                 quantity=sale[Fields.quantity],
                 gross_margin=sale[Fields.gross_margin])
    session.add(model)

def load_date(session, sale):
    # TODO: mode this logic into parser
    model = Date(year=date(int(sale[Fields.year]), 1, 1),
                 quarter=sale[Fields.quarter][1])  # eg. Q1 2012


    result = session.query(Date).filter(Date.year == model.year,
                                        Date.quarter == model.quarter).one_or_none()

    if result is None:
        session.add(model)
        return model
    else:
        return result

def load_lookup_table(session, sale, model_cls, field):
    model = model_cls(name=sale[field])
    result = session.query(model_cls).filter(model_cls.name == model.name).one_or_none()
    if result is None:
        session.add(model)
        return model
    else:
        return result

def load_country(session, sale):
    return load_lookup_table(session, sale, Country, Fields.retailer_country)

def load_product(session, sale):
    return load_lookup_table(session, sale, Product, Fields.product)

def load_product_line(session, sale):
    return load_lookup_table(session, sale, ProductLine, Fields.product_line)

def load_product_type(session, sale):
    return load_lookup_table(session, sale, ProductType, Fields.product_type)

def load_order_type(session, sale):
    return load_lookup_table(session, sale, OrderType, Fields.order_method_type)

def load_retailer_type(session, sale):
    return load_lookup_table(session, sale, RetailerType, Fields.retailer_type)

if __name__ == "__main__":
    load_models()
