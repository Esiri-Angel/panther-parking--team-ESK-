"""Business rules for Story 6: Manage lots."""
MAX_CAPACITY = 100_000


class PermissionDenied(Exception): pass
class LotNotFound(Exception): pass
class ValidationError(Exception): pass 


class LotService:
    def __init__(self):
        self.lots, self.next_id = {}, 1

    def _check(self, role, name, zone, capacity, lot_id=None):
        if role != "admin":
            raise PermissionDenied("Only admins can manage lots.")
        if lot_id is not None and lot_id not in self.lots:
            raise LotNotFound(f"No lot with id {lot_id}.")
        name, zone, cap = (name or "").strip(), (zone or "").strip(), str(capacity).strip()
        errors = []
        if not name:
            errors.append("Name is required.")
        elif len(name) > 100:
            errors.append("Name must be 100 characters or fewer.")
        elif any(l["name"].lower() == name.lower() for i, l in self.lots.items() if i != lot_id):
            errors.append("A lot with that name already exists.")
        if not zone:
            errors.append("Zone is required.")
        elif len(zone) > 50:
            errors.append("Zone must be 50 characters or fewer.")
        if not (cap.isascii() and cap.isdigit()):
            errors.append("Capacity must be a whole number.")
        elif not 1 <= int(cap) <= MAX_CAPACITY:
            errors.append("Capacity must be between 1 and 100,000.")
        if errors:
            raise ValidationError(errors)
        return {"name": name, "zone": zone, "capacity": int(cap)}

    def create_lot(self, role, name, zone, capacity):
        lot = {"id": self.next_id, **self._check(role, name, zone, capacity)}
        self.lots[lot["id"]] = lot
        self.next_id += 1
        return lot

    def edit_lot(self, role, lot_id, name, zone, capacity):
        data = self._check(role, name, zone, capacity, lot_id)
        self.lots[lot_id].update(data)
        return self.lots[lot_id]

    def list_lots(self):
        return sorted(self.lots.values(), key=lambda l: (l["zone"].lower(), l["name"].lower()))
