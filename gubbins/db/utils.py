import random


def random_models(qs, count):
    objects = []
    total_count = qs.count()
    ids = set()
    if total_count > 0:
        while len(objects) < min(count, total_count):
            idx = random.randint(0, total_count - 1)
            obj = qs[idx]
            if obj.id in ids:
                continue
            objects.append(obj)
            ids.add(obj.id)

    return objects