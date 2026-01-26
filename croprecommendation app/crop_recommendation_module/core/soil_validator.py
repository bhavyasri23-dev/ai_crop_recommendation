class SoilValidator:
    def validate_manual_inputs(self, ph, nitrogen, phosphorus, rainfall):
        """
        Validate manual soil inputs.
        Returns error message if invalid, None if valid.
        """
        try:
            # Check pH range
            if not (4.0 <= float(ph) <= 9.0):
                return "pH must be between 4.0 and 9.0"

            # Check nitrogen range
            if not (0 <= float(nitrogen) <= 200):
                return "Nitrogen must be between 0 and 200 kg/ha"

            # Check phosphorus range (increased to accommodate district data)
            if not (0 <= float(phosphorus) <= 200):
                return "Phosphorus must be between 0 and 200 kg/ha"

            # Check rainfall range
            if not (0 <= float(rainfall) <= 3000):
                return "Rainfall must be between 0 and 3000 mm"

            return None
        except (ValueError, TypeError):
            return "All soil parameters must be numeric values"

    def cross_validate_sources(self, manual_data, satellite_data=None, sensor_data=None):
        """
        Cross-validate soil data from multiple sources.
        Prioritizes sensor_data as primary input source.
        Returns (valid: bool, error: str, validated_data: dict)
        """
        try:
            # Start with sensor data if available, otherwise manual data
            if sensor_data:
                validated_data = {
                    "pH": float(sensor_data.get("pH", 7)),
                    "nitrogen": float(sensor_data.get("nitrogen", 50)),
                    "phosphorus": float(sensor_data.get("phosphorus", 30)),
                    "rainfall": float(sensor_data.get("rainfall", 900))
                }
            else:
                validated_data = {
                    "pH": float(manual_data.get("pH", 7)),
                    "nitrogen": float(manual_data.get("nitrogen", 50)),
                    "phosphorus": float(manual_data.get("phosphorus", 30)),
                    "rainfall": float(manual_data.get("rainfall", 900))
                }

            # Cross-validate with satellite data if available
            if satellite_data:
                try:
                    sat_ph = float(satellite_data.get("pH", validated_data["pH"]))
                    sat_n = float(satellite_data.get("nitrogen", validated_data["nitrogen"]))
                    sat_p = float(satellite_data.get("phosphorus", validated_data["phosphorus"]))
                    sat_r = float(satellite_data.get("rainfall", validated_data["rainfall"]))

                    # Use satellite data if within reasonable range of manual data
                    if abs(sat_ph - validated_data["pH"]) < 1.0:
                        validated_data["pH"] = (validated_data["pH"] + sat_ph) / 2
                    if abs(sat_n - validated_data["nitrogen"]) < 20:
                        validated_data["nitrogen"] = (validated_data["nitrogen"] + sat_n) / 2
                    if abs(sat_p - validated_data["phosphorus"]) < 10:
                        validated_data["phosphorus"] = (validated_data["phosphorus"] + sat_p) / 2
                    if abs(sat_r - validated_data["rainfall"]) < 200:
                        validated_data["rainfall"] = (validated_data["rainfall"] + sat_r) / 2
                except:
                    pass  # Ignore satellite data if invalid

            # Cross-validate with sensor data if available
            if sensor_data:
                try:
                    sen_ph = float(sensor_data.get("pH", validated_data["pH"]))
                    sen_n = float(sensor_data.get("nitrogen", validated_data["nitrogen"]))
                    sen_p = float(sensor_data.get("phosphorus", validated_data["phosphorus"]))
                    sen_r = float(sensor_data.get("rainfall", validated_data["rainfall"]))

                    # Use sensor data if within reasonable range of current validated data
                    if abs(sen_ph - validated_data["pH"]) < 0.5:
                        validated_data["pH"] = (validated_data["pH"] + sen_ph) / 2
                    if abs(sen_n - validated_data["nitrogen"]) < 10:
                        validated_data["nitrogen"] = (validated_data["nitrogen"] + sen_n) / 2
                    if abs(sen_p - validated_data["phosphorus"]) < 5:
                        validated_data["phosphorus"] = (validated_data["phosphorus"] + sen_p) / 2
                    if abs(sen_r - validated_data["rainfall"]) < 100:
                        validated_data["rainfall"] = (validated_data["rainfall"] + sen_r) / 2
                except:
                    pass  # Ignore sensor data if invalid

            return True, None, validated_data
        except Exception as e:
            return False, str(e), None

    def create_soil_fingerprint(self, ph, nitrogen, phosphorus, rainfall):
        """
        Create a unique fingerprint for soil conditions.
        """
        try:
            # Create a hash based on soil parameters
            import hashlib
            data = f"{ph:.2f}_{nitrogen:.1f}_{phosphorus:.1f}_{rainfall:.1f}"
            return hashlib.md5(data.encode()).hexdigest()[:8]
        except:
            return "unknown"
