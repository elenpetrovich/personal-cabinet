from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage

from cabinet.models import Account
from document.models import client, Document
from company.models import Collection, Role
import re
from django.utils import timezone
from bson import ObjectId


def save_doc(doc: dict, company, collection, pk: str = "Ref", **kwargs):
    result = client.get_database(company.mongo_db).get_collection(
        collection.mongo_collection).replace_one({pk: doc[pk]}, doc, True)
    if result.upserted_id:
        Document(id=str(result.upserted_id),
                 collection=collection,
                 public=kwargs.get("public", False)).save()
    return doc[pk], result.modified_count, str(result.upserted_id)


def save_user(user: dict, company):
    db_user = Account.objects.filter(username=user["username"]).first()
    if db_user is None:
        new_user = Account(
            username=user.get("username",
                              str(company.id) + get_random_string(8)),
            password=make_password(user.get("password", get_random_string(8))),
            first_name=user.get("first_name", ""),
            last_name=user.get("last_name", ""),
            email=user.get("email", ""),
        )
        new_user.save()
        return new_user, company.name, True
    else:
        if user.get("password"):
            db_user.password = make_password(user["password"])
        if user.get("first_name"):
            db_user.first_name = user["first_name"]
        if user.get("last_name"):
            db_user.last_name = user["password"]
        if user.get("email"):
            db_user.last_name = user["email"]
        db_user.save()
    # new_user.groups.add(group, group, ...)
    return db_user, company.name, False


def save_role(role: dict, company):
    db_role = Role.objects.filter(name=role["name"]).first()
    if db_role is None:
        db_role = Role(name=role.get("name"), company=company)
        db_role.save()
    else:
        if role.get("name"):
            db_role.name = role["name"]
        db_role.save()
    if role.get("collections_list", []):
        db_role.collections.add(
            Collection.objects.filter(company=company,
                                      name__in=role.get(
                                          "collections_list", [])).all())
    if role.get("username_list", []):
        db_role.collections.add(
            Account.objects.filter(
                username__in=role.get("username_list", [])).all())
    db_role.save()
    return db_role


def save_file(file_obj: dict, company):
    reg = re.compile('[^a-zA-ZА-я0-9_ ]')
    # request = DocumentFile.objects.filter(
    #     ref=file_obj["file_ref"],
    #     collection__name=file_obj['collection'],
    #     collection__company=company,
    # ).first()
    request = None
    if request:
        file_name = f"{reg.sub('', company.system_name)}/{reg.sub('', file_obj['collection'])}/{file_obj.file_data['name']}"
        file_path = default_storage.save(
            file_name,
            file_obj["file_data"],
        )
        file_url = default_storage.url(file_name)
        request.saved = True
        request.file_path = file_path
        request.saved_file_date = timezone.now()
        request.save()
    return file_path, file_url, request


def save_collection(collection_name: str, company, **kwargs) -> Collection:
    collection = Collection.objects.filter(company=company,
                                           name=collection_name).first()
    if collection is None:
        collection = Collection(name=collection_name,
                                mongo_collection=kwargs.get(
                                    "mongo", get_random_string(12)),
                                company=company)
        collection.save()
    return collection


def get_file_request(company):
    data = []
    # for request in DocumentFile.objects.filter(company=company,
    #                                            saved=False).all():
    #     data.append(request)
    return data
