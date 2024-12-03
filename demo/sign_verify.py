import oqs
import os


def generate_keypair(sign_alg):
    signer = oqs.Signature(sign_alg)
    public_key = signer.generate_keypair()
    secret_key = signer.export_secret_key()
    return public_key, secret_key


def sign(sign_alg, message, secret_key, names):
    encrypter = oqs.Signature(sign_alg, secret_key)         # initialize the encrypter
    signature = len(names).to_bytes(1, byteorder='big')     # record the number of people who signed the document

    for name in names:
        encrypted_name = encrypter.sign(name.encode("utf-8"))
        signature += encrypted_name                         # append the encrypted names to the signature

    signature += encrypter.sign(message)                    # append the encrypted document to the signature

    return signature


def verify_document(sign_alg, message, signature, public_key):
    verifier = oqs.Signature(sign_alg)                              # initialize the verifier
    header = signature[:1]
    number_of_signers = int.from_bytes(header, byteorder='big')     # get the number of signers

    body = signature[1 + 4627 * number_of_signers:]                 # extract encrypted document body

    return verifier.verify(message, body, public_key)


def verify_signer(sign_alg, name, signature, public_key):
    verifier = oqs.Signature(sign_alg)  # initialize the verifier
    header = signature[:1]
    number_of_signers = int.from_bytes(header, byteorder='big')  # get the number of signers

    encrypted_signers = []
    for i in range(number_of_signers):
        encrypted_signers.append(signature[1 + i * 4627: 1 + (i+1) * 4627])

    for encrypted_signer in encrypted_signers:
        if verifier.verify(name.encode("utf-8"), encrypted_signer, public_key):
            return True

    return False


if __name__ == "__main__":

    method = "ML-DSA-87"
    encryption_length = 4627  # The length of the encryption result of the ML-DSA-87 algorithm is 4627
    document_file_name = 'sample_document'  # Assume that this is the document that has been signed by 3 people
    name_list = ["Bob", "Alex", "David"]    # Assume they are the guys that signed the document

    # clear the files
    if os.path.exists('mldsa.pub'):
        os.remove('mldsa.pub')
    if os.path.exists('mldsa.key'):
        os.remove('mldsa.key')
    if os.path.exists('mldsa.sig'):
        os.remove('mldsa.sig')

    # =================== generate keys =========================
    pub_key, sec_key = generate_keypair(method)

    # save keys
    with open('mldsa.pub', 'wb') as file:
        file.write(pub_key)
    with open('mldsa.key', 'wb') as file:
        file.write(sec_key)

    # =================== sign the documents =======================
    with open(document_file_name, 'rb') as file:
        document = file.read()              # read the document


    sig = sign(method, document, sec_key, name_list)   # sign with secret key

    with open('mldsa.sig', 'wb') as file:   # save signature
        file.write(sig)

    # ============================= Verification ============================
    # verify the document
    print("Document verification results:", verify_document(method, document, sig, pub_key))

    # verify all the signers
    for name in name_list:
        print("Verifying Signer", name, "Result:", verify_signer(method, name, sig, pub_key))

    # test for a fake signer
    faker = "Bobx"
    print("Verifying a fake Signer", faker, "Result:", verify_signer(method, faker, sig, pub_key))


