# API Choice

- Étudiant : [Votre Nom]
- API choisie : Agify
- URL base : https://api.agify.io
- Documentation officielle / README : https://agify.io
- Auth : None
- Endpoints testés :
  - GET /?name=michael (Predict age for one name)
  - GET /?name[]=michael&name[]=peter (Predict age for multiple names)
  - GET /?name=michael&country_id=FR (Predict age with country)
- Hypothèses de contrat (champs attendus, types, codes) :
  - Single: { "count": integer, "name": string, "age": integer }, 200 OK
  - List: [ { "count": integer, "name": string, "age": integer }, ... ], 200 OK
  - Missing name: { "error": string }, 422 Unprocessable Entity
- Limites / rate limiting connu : 1000 names per day for free tier (no key).
- Risques (instabilité, downtime, CORS, etc.) : Potential 429 if many students share the same IP.

