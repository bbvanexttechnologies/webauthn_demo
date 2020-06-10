from flask import Flask
from flask import jsonify,request, make_response
import webauthn
import util
from flask_cors import CORS
import database
from app import app
import base64
import math
import json
import os
import binascii
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request, set_access_cookies
)
import datetime


RP_ID = 'localhost'
RP_NAME = 'BBVA NEXT SECLAB FIDO DEMO'
ORIGIN = 'http://localhost:8080'
TRUST_ANCHOR_DIR = 'trusted_attestation_roots'
try:
    database.init_db()
except:
    print('already exits')


'''
STEP 1 ->
The server sends a challenge along with the user information and its own information to the JavaScript program running
on the Browser. The protocol it's not defined so we are going to use REST over HTTP or HTTPS.
The challenge must be an information buffer with at least 16 bytes. In this example we are creating a 32 bytes buffer.
'''
@app.route('/registration/init', methods=['POST'])
def webauthn_begin_activate():
    jsonData = request.get_json()
    name = jsonData['name']
    surname = jsonData['surname']
    email = jsonData['email']
    username = email
    display_name = name + " " + surname
    challenge = util.generate_challenge(32)
    id = util.generate_ukey()
    '''
     PublicKeyCredentialCreationOptions
     rp-> Relying Party: It's the server where you want to authenticate.
            RP_NAME: name
            RP_ID: The RP ID must be equal to the origin's effective domain, or a registrable domain suffix of
                   the origin's effective domain.
                   The origin's scheme must be https.
                   The origin's port is unrestricted.
     user information->
            Information about the user registering
            Helps to choose from multiple credentials.
            username: it is a human-palatable identifier for a user account.
                    It is intended only for display, i.e., aiding the user in determining
                    the difference between user accounts with similar displayNames.
                    For example, "alexm", "alex.p.mueller@example.com" or "+14255551234".
            display_name: A human-palatable name for the user account, intended only for display. For example, "Alex P. Müller" or "田中 倫".
                         The Relying Party SHOULD let the user choose this, and SHOULD NOT restrict the choice more than necessary.
            id: The user handle of the user account entity.
                A user handle is an opaque byte sequence with a maximum size of 64 bytes,
                and is not meant to be displayed to the user.
    '''
    make_credential_options = webauthn.WebAuthnMakeCredentialOptions(
        challenge, RP_NAME, RP_ID, id, username, display_name,
        'http://localhost')
    challenge = challenge.rstrip("=")
    insert = database.insert_db("insert into PublicKeyCredentialCreationOptions VALUES (?,?,?,?,?,?)",[RP_NAME, RP_ID,id,display_name,username,challenge])
    return jsonify(make_credential_options.registration_dict)

'''
    STEP 6
    The server validates and finishes the register.
    It verifies that the challenge is equal to the previos one.
    It validates the origin, te signtarure and the hash.
'''
@app.route('/registration/end', methods=['POST'])
def webauthn_end_activate():
    jsonData = request.get_json()
    AuthenticatorAttestationResponse = jsonData['AuthenticatorAttestationResponse']
    clientDataJSON = AuthenticatorAttestationResponse['clientDataJSON']
    clientDataJSON_padding = clientDataJSON.ljust((int)(math.ceil(len(clientDataJSON) / 4)) * 4, '=')
    clientDataJSON = base64.b64decode(clientDataJSON_padding).decode('utf8')
    clientDataJSONparsed = json.loads(clientDataJSON)
    retrievedChallenge = clientDataJSONparsed['challenge']
    try:
        data = database.query_db("select * from PublicKeyCredentialCreationOptions where challenge=?",[retrievedChallenge])[0]
    except:
        return jsonify({"Error:","Could not find challenge"}),500
    trusted_attestation_cert_required = True
    self_attestation_permitted = True
    none_attestation_permitted = True

    registration_response = {'clientData':AuthenticatorAttestationResponse['clientDataJSON'],'attObj':AuthenticatorAttestationResponse['attestationObject']}
    trust_anchor_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), TRUST_ANCHOR_DIR)
    webauthn_registration_response = webauthn.WebAuthnRegistrationResponse(
        RP_ID,
        ORIGIN,
        registration_response,
        data[5],
        trust_anchor_dir,
        trusted_attestation_cert_required,
        self_attestation_permitted,
        none_attestation_permitted,
        uv_required=False)  # User Verification

    try:
        webauthn_credential = webauthn_registration_response.verify()
    except (RuntimeError, TypeError, NameError):
        print(RuntimeError)
        return jsonify({'fail': 'Registration failed. Error: {}'.format(RuntimeError)})
    credential_id=webauthn_credential.credential_id.decode("utf-8")
    duplicatedId = database.query_db("select credential_id from Users where credential_id=?",[credential_id])
    if len(duplicatedId)!=0:
        return jsonify({"Error":"Error with register, try again"}),500

    existing_user = database.query_db("select user_id from Users where username=?",[data[4]])
    if len(existing_user)!=0:
        return jsonify({"Error":"Error with register, try again"}),500
    #Add user to database
    database.insert_db("insert into Users VALUES (?,?,?,?,?,?,?,?)",[data[2],data[4],data[3],webauthn_credential.public_key,credential_id,webauthn_credential.sign_count,'http://localhost',data[1]])
    #Remove from PublicKeyCredentialCreationOptions
    database.delete_db("delete from PublicKeyCredentialCreationOptions where challenge=?",[retrievedChallenge])
    return jsonify({'success': 'User successfully registered.'})


@app.route('/login/init', methods=['POST'])
def webauthn_begin_assertion():
    jsonData = request.get_json()
    username = jsonData['username']

    if not util.validate_username(username):
        return make_response(jsonify({'fail': 'Invalid username.'}), 401)

    user = database.query_db("select * from Users where username=?",[username])[0]
    if len(user) == 0:
        return make_response(jsonify({'fail': 'User does not exist.'}), 401)
    if not user[4]:
        return make_response(jsonify({'fail': 'Unknown credential ID.'}), 401)


    challenge = util.generate_challenge(32)

    # We strip the padding from the challenge stored in the session
    # for the reasons outlined in the comment in webauthn_begin_activate.
    toStoreChallenge = challenge.rstrip('=')
    try:
        insert = database.insert_db("insert into PublicKeyCredentialCreationOptions VALUES (?,?,?,?,?,?)",[None, None,user[0],None,username,toStoreChallenge])
    except:
        update = database.insert_db("update PublicKeyCredentialCreationOptions SET challenge=? where user_username=?",[toStoreChallenge,username])
    webauthn_user = webauthn.WebAuthnUser(
        user[0], user[1], user[2], user[6],
        user[4], user[3], user[5], user[7])

    webauthn_assertion_options = webauthn.WebAuthnAssertionOptions(
        webauthn_user, challenge)

    return jsonify(webauthn_assertion_options.assertion_dict)

@app.route('/login/end', methods=['POST'])
def verify_assertion():
    jsonData = request.get_json()
    AuthenticatorAttestationResponse = jsonData['AuthenticatorAttestationResponse']
    clientDataJSON = AuthenticatorAttestationResponse['clientDataJSON']
    clientDataJSON_padding = clientDataJSON.ljust((int)(math.ceil(len(clientDataJSON) / 4)) * 4, '=')
    clientDataJSON = base64.b64decode(clientDataJSON_padding).decode('utf8')
    clientDataJSONparsed = json.loads(clientDataJSON)
    retrievedChallenge = clientDataJSONparsed['challenge']
    try:
        data = database.query_db("select * from PublicKeyCredentialCreationOptions where challenge=?",[retrievedChallenge])[0]
    except:
        return jsonify({"Error:","Could not find challenge"}),500
    #DELETE from table
    database.delete_db("delete from PublicKeyCredentialCreationOptions where challenge=?",[retrievedChallenge])
    signature = AuthenticatorAttestationResponse['signature']
    assertion_response =  {'clientData':AuthenticatorAttestationResponse['clientDataJSON'],'authData':AuthenticatorAttestationResponse['authenticatorData'],'signature':signature,'userHandle':AuthenticatorAttestationResponse['userHandle']}

    credential_id = AuthenticatorAttestationResponse.get('id')
    user = database.query_db("select * from Users where credential_id=?",[credential_id])[0]
    if len(user)==0:
        return make_response(jsonify({'fail': 'User does not exist.'}), 401)
    webauthn_user = webauthn.WebAuthnUser(
        user[0], user[0], user[2], user[6],
        user[4], user[3], user[5], user[7])

    webauthn_assertion_response = webauthn.WebAuthnAssertionResponse(
        webauthn_user,
        assertion_response,
        retrievedChallenge,
        ORIGIN,
        uv_required=False)  # User Verification
    sign_count = webauthn_assertion_response.verify()
    try:
        sign_count = webauthn_assertion_response.verify()
    except Exception as e:
        print(e)
        return make_response(jsonify({'fail': 'Assertion failed'}),500)

    # Update counter.

    #Update database
    update = database.insert_db("update Users SET sign_count=? where username=?",[sign_count,user[1]])
    identityObj={'username':user[1],'id':user[0],'displayname':user[2]}
    expires = datetime.timedelta(hours=2)
    print(identityObj)
    jwt = create_access_token(identity=identityObj,expires_delta=expires)
    return jsonify({
        'success':
        'Successfully authenticated as {}'.format(user[1]),
        'jwt':jwt
    })
