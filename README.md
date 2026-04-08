# NetRecon and SecureChat

This archive provides Linux-native implementations for:
1) SecureChat with TLS + client-auth and optional end-to-end AES-GCM.
2) NetRecon toolkit with CLI and a minimal Flask UI.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## SecureChat
```bash
cd secure-chat
./make-certs.sh          # generate CA, server, client certs
python server.py         # start TLS server on :8443
python client.py alice lobby pass123
python client.py bob   lobby pass123
```

## NetRecon CLI
```bash
cd netrecon
python ../netrecon/cli.py 127.0.0.1 -p 1-1024
```

## NetRecon Web
```bash
cd netrecon
python app.py
# open http://localhost:5000/
```
