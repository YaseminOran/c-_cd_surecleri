#!/usr/bin/env python3
"""
Basit Flask API - CI/CD Örneği
Bu uygulama CI/CD pipeline'ını test etmek için kullanılır.
"""

from flask import Flask, request, jsonify
import os
import logging
from datetime import datetime
from model import SimpleModel
from utils import validate_input, format_response

# Flask uygulamasını oluştur
app = Flask(__name__)

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model instance
model = SimpleModel()


@app.route("/", methods=["GET"])
def home():
    """Ana sayfa - API bilgileri"""
    return jsonify(
        {
            "service": "CI/CD Example API",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "GET /": "API bilgileri",
                "GET /health": "Sağlık kontrolü",
                "POST /predict": "ML tahmin",
                "GET /metrics": "API metrikleri",
            },
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/health", methods=["GET"])
def health_check():
    """Sağlık kontrolü endpoint'i"""
    try:
        # Basit sağlık kontrolleri
        model_status = model.is_healthy()

        health_status = {
            "status": "healthy" if model_status else "unhealthy",
            "model_loaded": model_status,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
        }

        return jsonify(health_status), 200 if model_status else 503

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            503,
        )


@app.route("/predict", methods=["POST"])
def predict():
    """ML tahmin endpoint'i"""
    try:
        # Request verilerini al
        if not request.is_json:
            return (
                jsonify(
                    {"error": "Content-Type application/json olmalı", "status": "error"}
                ),
                400,
            )

        data = request.get_json()

        # Input validasyonu
        validation_result = validate_input(data)
        if not validation_result["valid"]:
            return (
                jsonify({"error": validation_result["message"], "status": "error"}),
                400,
            )

        # Model ile tahmin yap
        prediction = model.predict(data)

        # Response formatla
        response = format_response(prediction, data)

        logger.info(f"Prediction made: {prediction}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return (
            jsonify(
                {
                    "error": "İç server hatası",
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )


@app.route("/metrics", methods=["GET"])
def metrics():
    """API metrikleri"""
    return jsonify(
        {
            "total_predictions": model.get_prediction_count(),
            "uptime_seconds": model.get_uptime(),
            "last_prediction": model.get_last_prediction_time(),
            "model_version": model.get_version(),
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.errorhandler(404)
def not_found(error):
    """404 hata işleyicisi"""
    return (
        jsonify(
            {
                "error": "Endpoint bulunamadı",
                "status": "error",
                "available_endpoints": ["/", "/health", "/predict", "/metrics"],
            }
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    """500 hata işleyicisi"""
    return (
        jsonify(
            {
                "error": "İç server hatası",
                "status": "error",
                "timestamp": datetime.now().isoformat(),
            }
        ),
        500,
    )


def main():
    """Ana fonksiyon"""
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "False").lower() == "true"

    logger.info(f"Starting API on port {port}")
    logger.info(f"Debug mode: {debug}")

    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
