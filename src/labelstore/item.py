import json
from flask import Blueprint, abort, jsonify, request
from .model.store import Store

bp = Blueprint("item", __name__)
store = Store()


def make_item(id, item):
    return {"id": id, "label": item.label, "ts": item.create_ts.isoformat()}


@bp.errorhandler(400)
def client_error(e):
    return jsonify(error=str(e)), 400


@bp.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@bp.post("")
def create():
    req = request.get_json()
    try:
        label = req["label"]
    except KeyError:
        abort(400, description='Expected "label" key in request object')
    return make_item(*store.create(label)), 201


@bp.get("/all")
def fetch_all():
    return jsonify([make_item(id, item) for id, item in store.get_all()])


@bp.get("/random")
def fetch_random():
    # fortune(1) as a service, anyone?
    try:
        return make_item(*store.get_random())
    except IndexError:
        abort(404, description="No items available")


@bp.get("/<id>")
def fetch(id):
    try:
        item = store.get_by_id(id)
    except KeyError:
        abort(404)
    return make_item(id, item)
