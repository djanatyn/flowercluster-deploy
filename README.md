flowercluster setup
-------------------

deploys are run using [Fabric](http://www.fabfile.org/).

secrets are stored using [HashiCorp Vault](https://www.vaultproject.io/).

---

you need a few secrets to successfully deploy:

- an ssh key in your agent to access the server (and run sudo)
- the unseal keys for the vault (or someone else to unseal the vault with you)
- a token with permissions to create AppRole secret IDs

## Container Authentication + Secrets

We use Vault with the `AppRole` authentication backend to give our containers tokens that can be used to access secrets. The tokens the containers are given are only usable once, and are used to get a more permanent, recycable token that isn't stored in the container image.

AppRoles can have specific ACL policies associated with them, along with TTLs for token lifecycles and maximum-TTLs for token renewal lifecycles. To get a token from an AppRole, you also need to generate a SecretID. SecretIDs are generated from an AppRole, and can only be used to fetch an AppRole-authenticated token a set number of times.

Vault also has a nifty feature for [wrapping responses](https://www.vaultproject.io/docs/concepts/response-wrapping.html) in [cubbyholes](https://www.hashicorp.com/blog/vault-cubbyhole-principles.html), which has access scoped to a particular token. This means we can send a request for a new SecretID, and get a token (usable one time only!) to get back the response with the SecretID.
