# Glossary (plain English)

**Hash (SHA-256)**: a fingerprint of some text. Put any text in, get 64 letters and digits out. The same text always gives the same fingerprint. Change even one character and the fingerprint is completely different. You cannot get the text back from the fingerprint.

**Blockchain**: a shared notebook that thousands of computers keep identical copies of. You can add new lines, but nobody can secretly change or remove old ones. That is why it is good for proving "this existed at this time".

**Testnet (Sepolia)**: a practice blockchain. It works like the real one (Ethereum) but its coins are free and worth nothing. We use Sepolia so mistakes cost nothing.

**Smart contract**: a tiny program stored on the blockchain. Once it is there, its code cannot be changed. Ours (`EvidenceAnchor`) only does two things: remember a hash with the time (`anchor`), and tell you if it knows a hash (`verify`).

**Anchoring**: writing the hash of our report into the smart contract, so the blockchain's clock proves the report existed in that exact form at that time.

**Wallet**: an account on the blockchain. It has a public address (like a bank account number, safe to share) and a **private key** (like the password to spend from it, NEVER share it). We use a throwaway wallet with test coins only.

**Gas / test ETH**: the small fee a blockchain charges for writing data. On Sepolia you get free test ETH from a "faucet".

**IOC (indicator of compromise)**: a clue that shows an attack, such as the attacker's IP address or a username they used.

**MITRE ATT&CK**: a public catalogue of how attackers behave, with an ID for every technique (for example `T1110` = brute force). Using the IDs lets security people instantly understand our findings.

**Brute force**: an attacker tries many passwords for ONE account until one works.

**Password spray**: an attacker tries one or two common passwords on MANY accounts. It stays under the "too many failed logins" alarm for each account.

**SIEM**: a big security system that collects logs from many machines and raises alerts. VulnPilot is a small, focused helper for one log, not a SIEM.

**Log**: a text file where a program writes down what happened, one line per event. Ours are SSH login logs.

**Evidence line**: the exact original log line that proves a finding. The AI must quote these and may not invent any.

**Hypothesis**: an educated guess that the log does not prove. We always label guesses so nobody mistakes them for facts.

**Pipeline**: the chain of steps the app runs one after another: read the log, detect attacks, score risk, ask the AI, build the report, hash it.

**Dummy**: a placeholder answer a function returns until someone writes the real code, so the whole app still works.

**Pull request (PR)**: a request on GitHub to add your change to the project. The lead reviews and merges it.

**Fork**: your own copy of a GitHub project, where you may change things freely before sending them back with a pull request.
