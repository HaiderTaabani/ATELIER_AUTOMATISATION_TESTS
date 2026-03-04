# API Choice

- Étudiant : [Votre Nom]
- API choisie : CountAPI
- URL base : https://api.countapi.xyz
- Documentation officielle / README : https://countapi.xyz
- Auth : None
- Endpoints testés :
  - GET /hit/demo/key (Increment and get)
  - GET /get/demo/key (Get current value)
  - GET /info/demo/key (Get key info)
- Hypothèses de contrat (champs attendus, types, codes) :
  - hit: { "value": integer }, 200 OK
  - get: { "value": integer }, 200 OK
  - info: { "namespace": string, "key": string, "value": integer, ... }, 200 OK
  - Invalid namespace/key -> 404 Not Found
- Limites / rate limiting connu : 10 requests per second or IP based limits.
- Risques (instabilité, downtime, CORS, etc.) : Service sometimes unstable or returning 5xx under high load.

