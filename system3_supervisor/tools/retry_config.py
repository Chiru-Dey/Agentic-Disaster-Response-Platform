from google.genai import types

RESILIENT_GENERATION_CONFIG = types.GenerateContentConfig(
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=5,
            initial_delay=1.0,
            max_delay=20.0,
            exp_base=2.0,
            http_status_codes=[429, 500, 503, 504],
        )
    )
)