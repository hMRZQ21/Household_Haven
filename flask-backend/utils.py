import typing, sqlalchemy

def serialize_sqlalchemy_object_to_dictionary(
    sqlalchemy_object: typing.Any,
) -> typing.Dict:
    """ Serializes an SQLAlchemy object into a dictionary. """
    dictionary = {}

    for column in sqlalchemy_object.__table__.columns:
        # Stringify dates to serialize Python date types deterministically.
        if isinstance(column.type, sqlalchemy.sql.sqltypes.Date):
            dictionary[column.name] = str(getattr(sqlalchemy_object, column.name))
            continue

        dictionary[column.name] = getattr(sqlalchemy_object, column.name)

    for relationship in sqlalchemy_object.__mapper__.relationships.keys():
        dictionary[relationship] = []

        for related_sqlalchemy_object in getattr(sqlalchemy_object, relationship):
            related_sqlalchemy_object_dict = {}
            for column in related_sqlalchemy_object.__table__.columns:
                related_sqlalchemy_object_dict[column.name] = str(
                    getattr(related_sqlalchemy_object, column.name)
                )
            dictionary[relationship].append(related_sqlalchemy_object_dict)

    return dictionary

def serialize_sqlalchemy_objects_to_dictionary(
    sqlalchemy_objects: typing.List[typing.Any],
) -> typing.List[typing.Dict]:
    """ Serializes SQLAlchemy objects into a list of dictionaries. """
    serialized_objects = []

    for sqlalchemy_object in sqlalchemy_objects:
        serialized_objects.append(
            serialize_sqlalchemy_object_to_dictionary(sqlalchemy_object)
        )

    return serialized_objects