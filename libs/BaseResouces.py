from sqlalchemy import inspect

from app.extensions import db
from app.utils.db import auto_commit
from flask_restplus_patched import Resource


class BaseListResource(Resource):
    """
    support the basic function
    """

    class Meta:
        model = None
        schema = None
        api = None

    def create_query(self):
        return self.Meta.model.query

    def add_extend_field(self, query, args):
        return query

    def add_filter(self, query, args):
        # set query
        mapper = inspect(self.Meta.model)

        attr_names = [c_attr.key for c_attr in mapper.mapper.column_attrs]
        # query_param = ()
        for k, v in args.items():
            if k in attr_names:
                if isinstance(v, list):
                    query = query.filter(getattr(self.Meta.model, k) >= v[0]).filter(
                        getattr(self.Meta.model, k) <= v[1])
                else:
                    query = query.filter(getattr(self.Meta.model, k) == v)
        #
        # query = query.filter(
        #     *query_param
        # )
        return query

    def add_pagination(self, query, args):
        # return
        return query.offset(args['offset']).limit(args['limit'])

    def add_sort(self, query, args):
        sorter = args.get("sorter")
        if not sorter:
            return query.order_by(self.Meta.model.id.desc())

        sorter = sorter.split('|')
        # return
        return query.order_by(getattr(getattr(self.Meta.model, sorter[0]), sorter[1])())

    def get(self, args):
        """
        List of users.

        Returns a list of users starting from ``offset`` limited by ``limit``
        parameter.
        """
        query = self.create_query()
        query = self.add_filter(query, args).distinct(self.Meta.model.id)
        total = query.count()

        # return
        query = self.add_sort(query, args)
        query = self.add_extend_field(query, args)
        data = self.add_pagination(query, args).all()
        return {"list": data, 'total': total, **args}

    @auto_commit(db.session)
    def post(self, item):
        """
        Add a new item.
        """

        db.session.add(item)

        return item


class BaseRecordResource(Resource):

    @auto_commit(db.session)
    def delete(self, item):
        db.session.delete(item)
        db.session.commit()

        return None

    @auto_commit(db.session)
    def patch(self, args, item=None):
        """
        Patch item details by ID.
        """
        db.session.merge(self.Meta.model(**args))

        return self.Meta.model.query.get(item.id)

    @auto_commit(db.session)
    def put(self, args, item):
        """
        Patch item details by ID.
        """
        db.session.merge(self.Meta.model(**args))
        db.session.commit()

        return self.Meta.model.query.get(item.id)
