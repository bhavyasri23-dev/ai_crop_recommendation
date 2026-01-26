class SoilValidator:

    def validate_manual_inputs(self, ph, nitrogen, phosphorus, rainfall):
        if not (3 <= ph <= 9):
            return "Invalid pH value"
        if nitrogen < 0 or phosphorus < 0:
            return "Invalid nutrient values"
        if rainfall < 0:
            return "Invalid rainfall"
        return None

    def create_soil_fingerprint(self, ph, nitrogen, phosphorus, rainfall):
        return f"{ph}-{nitrogen}-{phosphorus}-{rainfall}"
