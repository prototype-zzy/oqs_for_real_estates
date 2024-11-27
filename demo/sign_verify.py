import oqs
import os


def generate_keypair(sign_alg):
    signer = oqs.Signature(sign_alg)
    public_key = signer.generate_keypair()
    secret_key = signer.export_secret_key()
    return public_key, secret_key


def sign(sign_alg, message, secret_key):
    signer = oqs.Signature(sign_alg, secret_key)
    signature = signer.sign(message)
    return signature


def verify(sign_alg, message, signature, public_key):
    verifier = oqs.Signature(sign_alg)
    return verifier.verify(message, signature, public_key)


if __name__ == "__main__":

    method = "ML-DSA-87"
    document_file_name = 'sample_document'

    if os.path.exists('mldsa.pub'):
        os.remove('mldsa.pub')
    if os.path.exists('mldsa.key'):
        os.remove('mldsa.key')
    if os.path.exists('mldsa.sig'):
        os.remove('mldsa.sig')

    pub_key, sec_key = generate_keypair(method)     # generate keys

    # save keys
    with open('mldsa.pub', 'wb') as file:
        file.write(pub_key)
    with open('mldsa.key', 'wb') as file:
        file.write(sec_key)

    with open(document_file_name, 'rb') as file:
        document = file.read()              # read the document

    sig = sign(method, document, sec_key)   # sign with secret key
    with open('mldsa.sig', 'wb') as file:   # save signature
        file.write(sig)

    # Verification
    print("Verification results:", verify(method, document, sig, pub_key))





